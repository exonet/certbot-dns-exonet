from logging import getLogger

import tldextract
from certbot.errors import PluginError
from exonetapi import Client
from exonetapi.structures import ApiResource
from requests.exceptions import HTTPError

LOGGER = getLogger(__name__)


class ExonetClient:
    """Encapsulates all communication with the Exonet API."""

    client: Client

    def __init__(self, token: str) -> None:
        """Exonet client constructor.

        Args:
            token: Exonet token.
        """
        self.client = Client("https://api.bwe.exodev.nl")
        self.client.authenticator.set_token(token)

    def post_api_resource(self, resource: ApiResource) -> ApiResource:
        try:
            return resource.post()
        except HTTPError as exception:
            error_message = f"Error adding TXT record using the Exonet API: {exception.response.text}"  # noqa: E501
            LOGGER.debug(error_message)
            raise PluginError(error_message) from exception

    def find_dns_zone_by_name(self, domain_name):
        # Convert to registered domain.
        domain = tldextract.extract(domain_name).registered_domain  # type: ignore[attr-defined] # noqa: E501

        # Get all available zones.
        zones = self.client.resource("dns_zones").filter("name", domain).get()

        # See if any zones match.
        matches = [zone for zone in zones if zone.attribute("name") == domain]

        # If a match is found, return it.
        if matches:
            zone = matches[0]
            LOGGER.debug(
                "Found DNS zone %s for domain %s", zone.attribute("name"), domain_name
            )
            return zone

        raise PluginError(
            f"Unable to find DNS zone for {domain_name}. Zone {domain} not found."
        )

    def add_txt_record(
        self, domain_name: str, record_name: str, record_content: str
    ) -> None:
        """Add a TXT record using the supplied information.

        Args:
            domain_name: The domain to use to associate the record with.
            record_name: The record name (typically beginning with '_acme-challenge.').
            record_content: The record content (typically the challenge validation).

        Raises:
            PluginError: If an error occurs while finding DNS zone.
            PluginError: If an error occurs while adding TXT record.
        """
        try:
            domain = self._find_zone(domain_name)
        except HTTPError as exception:
            hint = None

            if exception.response.status_code == 401:
                hint = "Did you provide a valid API token?"

            hint_message = f" ({hint})" if hint else ""
            error_message = f"Error finding DNS zone using the Exonet API: {exception}{hint_message}"  # noqa: E501
            LOGGER.debug(error_message)
            raise PluginError(error_message) from exception

        try:
            LOGGER.debug("Adding TXT record to DNS.")

            # Add the TXT record to the DNS.
            record = ApiResource("dns_records")
            record.attribute("type", "TXT")
            record.attribute("name", self._compute_record_name(domain, record_name))
            record.attribute("content", self._compute_record_content(record_content))
            record.attribute("ttl", 3600)
            record.relationship("zone", domain)
            created_record = record.post()

            LOGGER.debug(
                "Successfully added TXT record with id: %s", created_record.id()
            )
        except HTTPError as exception:
            error_message = f"Error adding TXT record using the Exonet API: {exception.response.text}"  # noqa: E501
            LOGGER.debug(error_message)
            raise PluginError(error_message) from exception

    def del_txt_record(
        self, domain_name: str, record_name: str, record_content: str
    ) -> None:
        """Delete a TXT record using the supplied information.

        Note that both the record's name and content are used to ensure that
        similar records created concurrently
        (e.g., due to concurrent invocations of this plugin) are not deleted.

        Failures are logged, but not raised.

        Args:
            domain_name: The domain to use to associate the record with.
            record_name: The record name (typically beginning with '_acme-challenge.'). # noqa: E501
            record_content: The record content (typically the challenge validation). # noqa: E501
        """
        try:
            domain = self._find_zone(domain_name)
        except HTTPError as exception:
            LOGGER.debug("Error finding domain using the Exonet API: %s", exception)
            return

        try:
            domain_records = domain.related("records").get()

            matching_records = [
                record
                for record in domain_records
                if record.attribute("type") == "TXT"
                and record.attribute("name")
                == self._compute_record_name(domain, record_name)
                and record.attribute("content")
                == self._compute_record_content(record_content)
            ]
        except HTTPError as exception:
            LOGGER.debug(
                "Error removing TXT record from the Exonet API: %s",
                exception.response.text,
            )
            return

        for record in matching_records:
            try:
                LOGGER.debug("Deleting DNS record with id: %s", record.id())
                record.delete()
            except HTTPError as exception:
                LOGGER.warning(
                    "Error deleting TXT record %s using the Exonet API: %s",
                    record.id(),
                    exception,
                )

    def _find_zone(self, domain_name: str) -> ApiResource:
        """Find the domain resource for a given domain name.

        Args:
            domain_name: The domain name for which to find the corresponding Domain.

        Raises:
            PluginError: If no matching Domain is found.

        Returns:
            The Domain, if found.
        """
        # Convert to registered domain.
        domain = tldextract.extract(domain_name).registered_domain  # type: ignore[attr-defined] # noqa: E501

        # Get all available zones.
        zones = self.client.resource("dns_zones").filter("name", domain).get()

        # See if any zones match.
        matches = [zone for zone in zones if zone.attribute("name") == domain]

        # If a match is found, return it.
        if matches:
            zone = matches[0]
            LOGGER.debug(
                "Found DNS zone %s for domain %s", zone.attribute("name"), domain_name
            )
            return zone

        raise PluginError(
            f"Unable to find DNS zone for {domain_name}. Zone {domain} not found."
        )

    @staticmethod
    def _compute_record_name(domain: ApiResource, full_record_name: str) -> str:
        # The name of the DNS record, without the DNS zone name.
        return full_record_name.rpartition("." + domain.attribute("name"))[0]

    @staticmethod
    def _compute_record_content(record_content: str) -> str:
        # The DNS record content within quotes.
        return '"' + record_content + '"'
