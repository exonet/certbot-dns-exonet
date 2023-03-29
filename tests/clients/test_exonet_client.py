"""Test exonet Client."""
from unittest import mock

from certbot_dns_exonet.clients.exonet_client import ExonetClient


class TestExonetClient:
    """The Exonet test Client."""

    @mock.patch("exonetapi.auth.Authenticator.set_token")
    def test_authenticate(self, mock_set_token):
        """Test exonet client validation.

        Args:
            mock_set_token: mock of set_token function from the Exonet API.
        """
        # Authenticate using Exonet client.
        ExonetClient("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")

        # Check mock calls.
        assert mock_set_token.call_args[0][0] == "kaSD0ffAD1ldSA92A0KODkaksda02KDAK"
        assert mock_set_token.call_count == 1
