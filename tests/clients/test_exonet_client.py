from unittest.mock import Mock, patch

from certbot.errors import PluginError
from exonetapi.auth.Authenticator import Authenticator
from exonetapi.RequestBuilder import RequestBuilder
from exonetapi.structures import ApiResource, ApiResourceSet
from pytest import raises
from requests import Response
from requests.exceptions import HTTPError

from certbot_dns_exonet.clients.exonet_client import ExonetClient


class TestExonetClient:
    """The Exonet test Client."""

    @patch.object(Authenticator, "set_token")
    def test_authenticate(self, mock_set_token: Mock) -> None:
        """Test Exonet client validation.

        Args:
            mock_set_token: Mock of set_token function from the Exonet API.
        """
        # Authenticate using Exonet client.
        ExonetClient("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")

        # Check mock calls.
        assert mock_set_token.call_args[0][0] == "kaSD0ffAD1ldSA92A0KODkaksda02KDAK"
        assert mock_set_token.call_count == 1

    @patch.object(Authenticator, "set_token")
    @patch.object(ApiResource, "post")
    def test_post_api_resource(self, mock_post: Mock, mock_set_token: Mock) -> None:
        """Test posting an ApiResource to the Exonet API.

        Args:
            mock_post: Mock of
                exonetapi.structures.ApiResource.post.
            mock_set_token: Mock of
                exonetapi.auth.Authenticator.set_token.
        """
        exonet_client = ExonetClient("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")
        exonet_client.post_api_resource(
            ApiResource({"type": "dns_records", "id": "qjJWA0Km8xgw"})
        )

        # Check mock calls.
        assert mock_post.call_count == 1
        assert mock_set_token.call_count == 1

        # Check call args.
        assert mock_set_token.call_args[0][0] == "kaSD0ffAD1ldSA92A0KODkaksda02KDAK"

    @patch.object(Authenticator, "set_token")
    @patch.object(ApiResource, "post")
    def test_post_api_resource_http_error(
        self, mock_post: Mock, mock_set_token: Mock
    ) -> None:
        """Test posting an ApiResource to the Exonet API when HTTPError occurs.

        Args:
            mock_post: Mock of
                exonetapi.structures.ApiResource.post.
            mock_set_token: Mock of
                exonetapi.auth.Authenticator.set_token.
        """
        response = Mock(spec=Response)
        response.text = "This is broken"
        error = HTTPError(response=response)

        mock_post.side_effect = error

        exonet_client = ExonetClient("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")

        with raises(PluginError) as e_info:
            exonet_client.post_api_resource(
                ApiResource({"type": "dns_records", "id": "qjJWA0Km8xgw"})
            )

        # Check error message.
        assert (
            e_info.value.args[0]
            == "Error adding ApiResource using the Exonet API: This is broken"
        )

        # Check mock calls.
        assert mock_post.call_count == 1
        assert mock_set_token.call_count == 1

        # Check call args.
        assert mock_set_token.call_args[0][0] == "kaSD0ffAD1ldSA92A0KODkaksda02KDAK"

    @patch.object(Authenticator, "set_token")
    @patch.object(ApiResource, "delete")
    def test_delete_api_resource(self, mock_delete: Mock, mock_set_token: Mock) -> None:
        """Test deleting an ApiResource to the Exonet API.

        Args:
            mock_delete: Mock of
                exonetapi.structures.ApiResource.delete.
            mock_set_token: Mock of
                exonetapi.auth.Authenticator.set_token.
        """
        exonet_client = ExonetClient("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")
        exonet_client.delete_api_resource(
            ApiResource({"type": "dns_records", "id": "qjJWA0Km8xgw"})
        )

        # Check mock calls.
        assert mock_delete.call_count == 1
        assert mock_set_token.call_count == 1

        # Check call args.
        assert mock_set_token.call_args[0][0] == "kaSD0ffAD1ldSA92A0KODkaksda02KDAK"

    @patch.object(Authenticator, "set_token")
    @patch.object(ApiResource, "delete")
    def test_delete_api_resource_http_error(
        self, mock_delete: Mock, mock_set_token: Mock
    ) -> None:
        """Test deleting an ApiResource from the Exonet API when HTTPError occurs.

        Args:
            mock_delete: Mock of
                exonetapi.structures.ApiResource.post.
            mock_set_token: Mock of
                exonetapi.auth.Authenticator.set_token.
        """
        response = Mock(spec=Response)
        response.text = "This is broken"
        error = HTTPError(response=response)

        mock_delete.side_effect = error

        exonet_client = ExonetClient("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")

        exonet_client.delete_api_resource(
            ApiResource({"type": "dns_records", "id": "qjJWA0Km8xgw"})
        )

        # Check mock calls.
        assert mock_delete.call_count == 1
        assert mock_set_token.call_count == 1

        # Check call args.
        assert mock_set_token.call_args[0][0] == "kaSD0ffAD1ldSA92A0KODkaksda02KDAK"

    @patch.object(Authenticator, "set_token")
    @patch.object(RequestBuilder, "get")
    def test_get_relation(self, mock_get: Mock, mock_set_token: Mock) -> None:
        """Test get_relation method from Exonet client.

        Args:
            mock_get: Mock of
                exonetapi.RequestBuilder.get.
            mock_set_token: Mock of
                exonetapi.auth.Authenticator.set_token.
        """
        exonet_client = ExonetClient("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")
        exonet_client.get_relation(
            ApiResource({"type": "dns_records", "id": "qjJWA0Km8xgw"}), "records"
        )

        # Check mock calls.
        assert mock_set_token.call_count == 1
        assert mock_get.call_count == 1

        # Check call args.
        assert mock_set_token.call_args[0][0] == "kaSD0ffAD1ldSA92A0KODkaksda02KDAK"

    @patch.object(Authenticator, "set_token")
    @patch.object(RequestBuilder, "get")
    def test_get_relation_http_error(
        self, mock_get: Mock, mock_set_token: Mock
    ) -> None:
        """Test get_relation method from Exonet client when HTTPError occurs.

        Args:
            mock_get: Mock of
                exonetapi.RequestBuilder.get.
            mock_set_token: Mock of
                exonetapi.auth.Authenticator.set_token.
        """
        response = Mock(spec=Response)
        response.text = "This is broken"
        error = HTTPError(response=response)

        mock_get.side_effect = error

        exonet_client = ExonetClient("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")
        call_response = exonet_client.get_relation(
            ApiResource({"type": "dns_records", "id": "qjJWA0Km8xgw"}), "records"
        )

        # Check mock calls.
        assert mock_set_token.call_count == 1
        assert mock_get.call_count == 1

        # Check call args.
        assert mock_set_token.call_args[0][0] == "kaSD0ffAD1ldSA92A0KODkaksda02KDAK"

        # Check response.
        assert call_response is None

    @patch.object(Authenticator, "set_token")
    @patch.object(RequestBuilder, "get")
    def test_find_dns_zone_by_name(self, mock_get: Mock, mock_set_token: Mock) -> None:
        """Test the find_dns_zone_by_name function from the Exonet client.

        Args:
            mock_get: Mock of
                exonetapi.RequestBuilder.get.
            mock_set_token: Mock of
                exonetapi.auth.Authenticator.set_token.
        """
        api_resource_set = ApiResourceSet()
        api_resource_set.add_resource(
            ApiResource({"type": "dns_zones", "id": "BqgWr8dr0XV7", "name": "test.nl"})
        )

        mock_get.return_value = api_resource_set

        exonet_client = ExonetClient("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")
        zone = exonet_client.find_dns_zone_by_name("test.nl")

        # Check mock calls.
        assert mock_set_token.call_count == 1
        assert mock_get.call_count == 1

        # Check call args.
        assert mock_set_token.call_args[0][0] == "kaSD0ffAD1ldSA92A0KODkaksda02KDAK"

        # Check response data.
        assert isinstance(zone, ApiResource)

    @patch.object(Authenticator, "set_token")
    @patch.object(RequestBuilder, "get")
    def test_find_dns_zone_by_name_http_error(
        self, mock_get: Mock, mock_set_token: Mock
    ) -> None:
        """Test the find_dns_zone_by_name from the Exonet client when HTTPError occurs.

        Args:
            mock_get: Mock of
                exonetapi.RequestBuilder.get.
            mock_set_token: Mock of
                exonetapi.auth.Authenticator.set_token.
        """
        response = Mock(spec=Response)
        response.text = "This is broken"
        response.status_code = 401
        error = HTTPError(response=response)

        mock_get.side_effect = error

        api_resource_set = ApiResourceSet()
        api_resource_set.add_resource(
            ApiResource({"type": "dns_zones", "id": "BqgWr8dr0XV7", "name": "test.nl"})
        )

        mock_get.return_value = api_resource_set

        exonet_client = ExonetClient("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")

        with raises(PluginError) as e_info:
            zone = exonet_client.find_dns_zone_by_name("test.nl")

            # Check response data.
            assert isinstance(zone, ApiResource)

        # Check error message.
        assert (
            e_info.value.args[0]
            == "Error finding DNS zone using the Exonet API:"
            + " (Did you provide a valid API token?)"
        )

        # Check mock calls.
        assert mock_set_token.call_count == 1
        assert mock_get.call_count == 1

        # Check call args.
        assert mock_set_token.call_args[0][0] == "kaSD0ffAD1ldSA92A0KODkaksda02KDAK"
