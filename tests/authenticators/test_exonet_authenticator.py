from certbot_dns_exonet.authenticators.exonet_authenticator import ExonetAuthenticator
from certbot.configuration import NamespaceConfig
from argparse import Namespace


class TestExonetAuthenticator:
    def test_add_parser_arguments(self):
        config = NamespaceConfig(
            Namespace(
                config_dir="/home/exonet.ini",
                work_dir="/home",
                logs_dir="/home",
                http01_port=100,
                https_port=200,
                domains=[],
                test_user_credentials=[],
            )
        )
        authenticator = ExonetAuthenticator(config, "test_user")
        # authenticator.add_parser_arguments()
