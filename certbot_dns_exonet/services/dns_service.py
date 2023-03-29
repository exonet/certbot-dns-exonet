from certbot_dns_exonet.clients.exonet_client import ExonetClient
from exonetapi.structures import ApiResource
from certbot.errors import PluginError

from requests.exceptions import HTTPError
from logging import getLogger

LOGGER = getLogger(__name__)


class DnsService:
    """Dns service."""

    exonet_client: ExonetClient

    def __init__(self, token) -> None:
        self.exonet_client = ExonetClient(token)

    def add_txt_record(
        self, domain_name: str, record_name: str, record_content: str
    ) -> None:
        try:
            domain = self.find_dns_zone_by_name(domain_name)
        except HTTPError as exception:
            hint = None

            if exception.response.status_code == 401:
                hint = "Did you provide a valid API token?"

            hint_message = f" ({hint})" if hint else ""
            error_message = f"Error finding DNS zone using the Exonet API: {exception}{hint_message}"  # noqa: E501
            LOGGER.debug(error_message)
            raise PluginError(error_message) from exception

        LOGGER.debug("Adding TXT record to DNS.")

        # Add the TXT record to the DNS.
        record = ApiResource("dns_records")
        record.attribute("type", "TXT")
        record.attribute("name", self._compute_record_name(domain, record_name))
        record.attribute("content", self._compute_record_content(record_content))
        record.attribute("ttl", 3600)
        record.relationship("zone", domain)
        created_record = self.exonet_client.post_api_resource(record)

        LOGGER.debug("Successfully added TXT record with id: %s", created_record.id())

    @staticmethod
    def _compute_record_name(domain: ApiResource, full_record_name: str) -> str:
        # The name of the DNS record, without the DNS zone name.
        return full_record_name.rpartition("." + domain.attribute("name"))[0]

    @staticmethod
    def _compute_record_content(record_content: str) -> str:
        # The DNS record content within quotes.
        return '"' + record_content + '"'
