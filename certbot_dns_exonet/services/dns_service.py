from logging import getLogger

from certbot.errors import PluginError
from exonetapi.structures import ApiResource
from tldextract import extract

from certbot_dns_exonet.clients.exonet_client import ExonetClient

LOGGER = getLogger(__name__)


class DnsService:
    """Service containing all DNS logic."""

    client: ExonetClient

    def __init__(self, token: str) -> None:
        """DNS service constructor.

        Args:
            token: The Exonet API token.
        """
        self.client = ExonetClient(token)

    def add_txt_record(
        self, domain_name: str, record_name: str, record_content: str
    ) -> None:
        """Add a TXT record using the supplied information.

        Args:
             domain_name: The domain to use to associate the record with.
             record_name: The record name (typically beginning with '_acme-challenge.').
             record_content: The record content (typically the challenge validation).

         Raises:
             PluginError: PluginError: If an error occurs while finding DNS zone.
        """
        # Convert to registered domain.
        domain = extract(domain_name).registered_domain

        # Find the DNS zone.
        zone = self.client.find_dns_zone_by_name(domain)

        # If a zone is found, raise exception.
        if not zone:
            raise PluginError(
                f"Unable to find DNS zone for {domain_name}. Zone {domain} not found."
            )

        LOGGER.debug(
            "Found DNS zone %s for domain %s", zone.attribute("name"), domain_name
        )

        LOGGER.debug("Adding TXT record to DNS.")

        # Add the TXT record to the DNS.
        record = ApiResource("dns_records")
        record.attribute("type", "TXT")
        record.attribute("name", self._compute_record_name(zone, record_name))
        record.attribute("content", self._compute_record_content(record_content))
        record.attribute("ttl", 3600)
        record.relationship("zone", zone)
        created_record = self.client.post_api_resource(record)

        LOGGER.debug("Successfully added TXT record with id: %s", created_record.id())

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

        Raises:
             PluginError: PluginError: If no DNS records are found for a domain.
        """
        # Convert to registered domain.
        domain = extract(domain_name).registered_domain

        # Find the DNS zone.
        zone = self.client.find_dns_zone_by_name(domain)

        # Get DNS records for DNS zone.
        domain_records = self.client.get_relation(zone, "records")

        # If no records are found raise exception.
        if not domain_records:
            raise PluginError(f"Unable to find DNS records for {zone}.")

        # Get all matching records.
        matching_records = [
            record
            for record in domain_records
            if record.attribute("type") == "TXT"
            and record.attribute("name") == self._compute_record_name(zone, record_name)
            and record.attribute("content")
            == self._compute_record_content(record_content)
        ]

        # Delete all matching records.
        for record in matching_records:
            self.client.delete_api_resource(record)

    @staticmethod
    def _compute_record_name(domain: ApiResource, full_record_name: str) -> str:
        """Compute the DNS record name.

        Args:
            domain: The Exonet DNS record.
            full_record_name: The fill record name.

        Returns:
            str: The computed record name.
        """
        # The name of the DNS record, without the DNS zone name.
        return full_record_name.rpartition("." + domain.attribute("name"))[0]

    @staticmethod
    def _compute_record_content(record_content: str) -> str:
        """Compute the DNS record content name.

        Args:
            record_content: The record content.

        Returns:
            str: The computed record content name.
        """
        # The DNS record content within quotes.
        return '"' + record_content + '"'
