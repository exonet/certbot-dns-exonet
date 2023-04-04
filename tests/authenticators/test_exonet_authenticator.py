from argparse import Namespace
from unittest.mock import Mock, patch

from certbot.configuration import NamespaceConfig

from certbot_dns_exonet.authenticators.exonet_authenticator import ExonetAuthenticator


class TestExonetAuthenticator:
    """Test the Exonet Authenticator."""

    @patch("certbot.plugins.dns_common.DNSAuthenticator")
    def test_add_parser_arguments(self, mock_dns_authenticator: Mock) -> None:
        """Test add_parser_arguments function.

        Args:
            mock_dns_authenticator: Mock of
                certbot.plugins.dns_common.DNSAuthenticator.
        """
        config = NamespaceConfig(
            Namespace(
                config_dir="/home/dev/repositories/certbot-dns-exonet",
                work_dir="/home/dev/repositories/certbot-dns-exonet/test",
                logs_dir="/home/dev/repositories/certbot-dns-exonet/test",
                http01_port=80,
                https_port=443,
                domains=["exodev.nl"],
                test_user_credentials=[],
            )
        )
        authenticator = ExonetAuthenticator(config, "test_user")
        # authenticator.add_parser_arguments()
        print("done")
