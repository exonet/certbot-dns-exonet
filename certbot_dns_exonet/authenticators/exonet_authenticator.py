from logging import getLogger
from typing import Callable

import zope.interface
from certbot.interfaces import IAuthenticator, IPluginFactory
from certbot.configuration import NamespaceConfig
from certbot.plugins.dns_common import DNSAuthenticator, CredentialsConfiguration

from certbot_dns_exonet.services.dns_service import DnsService

LOGGER = getLogger(__name__)


@zope.interface.implementer(IAuthenticator)
@zope.interface.provider(IPluginFactory)
class ExonetAuthenticator(DNSAuthenticator):
    """DNS Authenticator for Exonet.

    This Authenticator uses the Exonet API to fulfill a dns-01 challenge.
    """

    credentials: CredentialsConfiguration

    def __init__(self, config: NamespaceConfig, name: str) -> None:
        """Construct the Authenticator class.

        Args:
            config: Authenticator config.
            name: created by name.
        """
        super().__init__(config, name)
        self._setup_credentials()

        self.dns_service = DnsService(self.credentials.conf("token"))

    @classmethod
    def add_parser_arguments(
        cls, add: Callable[..., None], default_propagation_seconds: int = 10
    ) -> None:
        """Add arguments to parser.

        Args:
            add: Function to call.
            default_propagation_seconds: Default propagation. Defaults to 10 seconds.
        """
        super().add_parser_arguments(add, default_propagation_seconds)
        add("credentials", help="Exonet credentials INI file.")

    def more_info(self) -> str:
        """Get more info about the plugin.

        Returns:
            Information about the plugin.
        """
        return (
            "This plugin configures a DNS TXT record to respond"
            + " to a dns-01 challenge using the \
            Exonet API."
        )

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            "credentials",
            "Exonet credentials INI file",
            {"token": "API token for Exonet API"},
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        """Add TXT DNS record using the Exonet API.

        Args:
            domain: The domain name.
            validation_name: The validation name.
            validation: The validation.
        """
        self.dns_service.add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        """Delete TXT DNS record using the Exonet API.

        Args:
            domain: The domain name.
            validation_name: The validation name.
            validation: The validation.
        """
        self.dns_service.del_txt_record(domain, validation_name, validation)
