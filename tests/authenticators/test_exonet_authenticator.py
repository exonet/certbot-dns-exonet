"""Certbot DNS Exonet tests."""

from argparse import Namespace
from unittest.mock import Mock, patch

from certbot.configuration import NamespaceConfig

from certbot_dns_exonet.authenticators.exonet_authenticator import ExonetAuthenticator


class TestExonetAuthenticator:
    """Test the Exonet Authenticator."""

    @patch("certbot.plugins.dns_common.DNSAuthenticator._configure_credentials")
    def test_add_parser_arguments(self, mock_configure_credentials: Mock) -> None:
        """Test add_parser_arguments function.

        Args:
            mock_configure_credentials: Mock of
                certbot.plugins.dns_common.DNSAuthenticator._configure_credentials.

        """
        # Create input variables.
        config = NamespaceConfig(
            Namespace(
                config_dir="/home/dev/repositories/certbot-dns-exonet",
                work_dir="/home/dev/repositories/certbot-dns-exonet/test",
                logs_dir="/home/dev/repositories/certbot-dns-exonet/test",
                http01_port=80,
                https_port=443,
                domains=["exodev.nl"],
                test_user_credentials=[],
                dns_exonet_credentials="/home/dev/repositories/certbot-dns-exonet/exonet.ini",
            )
        )

        add_mock = Mock()

        # Make the call
        authenticator = ExonetAuthenticator(config, "dns-exonet")
        authenticator.add_parser_arguments(add_mock)

        # Check mock calls.
        assert mock_configure_credentials.call_count == 1
        assert add_mock.call_count == 2

        # Check call args.
        assert add_mock.call_args_list[0][0][0] == "propagation-seconds"
        assert add_mock.call_args_list[0][1]["default"] == 10
        assert add_mock.call_args_list[0][1]["type"] is int
        assert (
            add_mock.call_args_list[0][1]["help"]
            == "The number of seconds to wait for DNS to propagate before asking the ACME server to verify the DNS record."  # noqa: E501
        )

        assert add_mock.call_args_list[1][0][0] == "credentials"
        assert add_mock.call_args_list[1][1]["help"] == "Exonet credentials INI file."

    @patch("certbot.plugins.dns_common.DNSAuthenticator._configure_credentials")
    def test_more_info(self, mock_configure_credentials: Mock) -> None:
        """Test the more_info function.

        Args:
            mock_configure_credentials: Mock of
                certbot.plugins.dns_common.DNSAuthenticator._configure_credentials.

        """
        # Create input variables.
        config = NamespaceConfig(
            Namespace(
                config_dir="/home/dev/repositories/certbot-dns-exonet",
                work_dir="/home/dev/repositories/certbot-dns-exonet/test",
                logs_dir="/home/dev/repositories/certbot-dns-exonet/test",
                http01_port=80,
                https_port=443,
                domains=["exodev.nl"],
                test_user_credentials=[],
                dns_exonet_credentials="/home/dev/repositories/certbot-dns-exonet/exonet.ini",
            )
        )

        # Make the call/
        authenticator = ExonetAuthenticator(config, "dns-exonet")
        info = authenticator.more_info()

        # Check mock calls.
        assert mock_configure_credentials.call_count == 1

        # Check response.
        assert info == (
            "This plugin configures a DNS TXT record to respond to a dns-01 "
            "challenge using the Exonet API."
        )
