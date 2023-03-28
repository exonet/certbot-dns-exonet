import logging
from typing import Callable

import zope.interface
from certbot import interfaces
from certbot.configuration import NamespaceConfig
from certbot.plugins import dns_common

from certbot_dns_exonet.clients.exonet_client import ExonetClient

LOGGER = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Exonet.

    This Authenticator uses the Exonet API to fulfill a dns-01 challenge.
    """

    credentials: dns_common.CredentialsConfiguration

    def __init__(self, config: NamespaceConfig, name: str) -> None:
        """Construct the Authenticator class.

        Args:
            config: Authenticator config.
            name: created by name.
        """
        super().__init__(config, name)
        self._setup_credentials()

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
        self._get_exonet_client().add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        """Delete TXT DNS record using the Exonet API.

        Args:
            domain: The domain name.
            validation_name: The validation name.
            validation: The validation.
        """
        self._get_exonet_client().del_txt_record(domain, validation_name, validation)

    def _get_exonet_client(self) -> ExonetClient:
        """Get the Exonet Client.

        Returns:
            ExonetClient: Instance of the ExonetClient class.
        """
        return ExonetClient(self.credentials.conf("token"))
