from unittest.mock import Mock, patch

from certbot.errors import PluginError
from exonetapi.structures import ApiResource, ApiResourceSet
from pytest import raises

from certbot_dns_exonet.services.dns_service import DnsService


class TestDnsService:
    """Test the DNS service."""

    @patch(
        "certbot_dns_exonet.clients.exonet_client.ExonetClient.find_dns_zone_by_name"
    )
    @patch("certbot_dns_exonet.clients.exonet_client.ExonetClient.post_api_resource")
    def test_add_txt_record(
        self, mock_post_api_resource: Mock, mock_find_dns_zone_by_name: Mock
    ) -> None:
        """Test adding TXT record.

        Args:
            mock_post_api_resource: Mock of
                certbot_dns_exonet.clients.exonet_client.ExonetClient.post_api_resource.
            mock_find_dns_zone_by_name: Mock of
                certbot_dns_exonet.clients.exonet_client.ExonetClient.find_dns_zone_by_name.
        """
        zone = ApiResource({"type": "dns_zones", "id": "BqgWr8dr0XV7"})
        zone.attribute("name", "test.nl")

        mock_find_dns_zone_by_name.return_value = zone

        dns_service = DnsService("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")
        dns_service.add_txt_record(
            "exodev.nl",
            "_acme-challenge.exodev.nl",
            "KEna0LvLAKFIcTCadLBQAH5yq_laL2PSKgNALcck5ms",
        )

        # Check mock calls.
        assert mock_find_dns_zone_by_name.call_count == 1
        assert mock_post_api_resource.call_count == 1

        # Check call args.
        assert mock_find_dns_zone_by_name.call_args[0][0] == "exodev.nl"

        assert mock_post_api_resource.call_args[0][0].attribute("type") == "TXT"
        assert mock_post_api_resource.call_args[0][0].attribute("ttl") == 3600
        assert (
            mock_post_api_resource.call_args[0][0].attribute("content")
            == '"KEna0LvLAKFIcTCadLBQAH5yq_laL2PSKgNALcck5ms"'
        )

    @patch(
        "certbot_dns_exonet.clients.exonet_client.ExonetClient.find_dns_zone_by_name"
    )
    @patch("certbot_dns_exonet.clients.exonet_client.ExonetClient.post_api_resource")
    def test_add_txt_record_no_zone(
        self, mock_post_api_resource: Mock, mock_find_dns_zone_by_name: Mock
    ) -> None:
        """Test adding TXT record when not zone is found.

        Args:
            mock_post_api_resource: Mock of
                certbot_dns_exonet.clients.exonet_client.ExonetClient.post_api_resource.
            mock_find_dns_zone_by_name: Mock of
                certbot_dns_exonet.clients.exonet_client.ExonetClient.find_dns_zone_by_name.
        """
        mock_find_dns_zone_by_name.return_value = None

        dns_service = DnsService("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")

        with raises(PluginError) as e_info:
            dns_service.add_txt_record(
                "exodev.nl",
                "_acme-challenge.exodev.nl",
                "KEna0LvLAKFIcTCadLBQAH5yq_laL2PSKgNALcck5ms",
            )

        # Check error message.
        assert (
            e_info.value.args[0]
            == "Unable to find DNS zone for exodev.nl. Zone exodev.nl not found."
        )

        # Check mock calls.
        assert mock_find_dns_zone_by_name.call_count == 1
        assert mock_post_api_resource.call_count == 0

    @patch(
        "certbot_dns_exonet.clients.exonet_client.ExonetClient.find_dns_zone_by_name"
    )
    @patch("certbot_dns_exonet.clients.exonet_client.ExonetClient.get_relation")
    @patch("certbot_dns_exonet.clients.exonet_client.ExonetClient.delete_api_resource")
    def test_del_txt_record(
        self,
        mock_delete_api_resource: Mock,
        mock_get_relation: Mock,
        mock_find_dns_zone_by_name: Mock,
    ) -> None:
        """Test deleting TXT record.

        Args:
            mock_delete_api_resource: Mock of
                certbot_dns_exonet.clients.exonet_client.ExonetClient.delete_api_resource.
            mock_get_relation: Mock of
                certbot_dns_exonet.clients.exonet_client.ExonetClient.get_relation.
             mock_find_dns_zone_by_name (Mock): Mock of
                certbot_dns_exonet.clients.exonet_client.ExonetClient.find_dns_zone_by_name.
        """
        zone = ApiResource({"type": "dns_zones", "id": "BqgWr8dr0XV7"})
        zone.attribute("name", "exodev.nl")

        mock_find_dns_zone_by_name.return_value = zone

        record = ApiResource({"type": "dns_records", "id": "LsaWr8dr0KSa"})
        record.attribute("name", "_acme-challenge")
        record.attribute("type", "TXT")
        record.attribute("content", '"KEna0LvLAKFIcTCadLBQAH5yq_laL2PSKgNALcck5ms"')

        records = ApiResourceSet()
        records.add_resource(record)

        mock_get_relation.return_value = records

        dns_service = DnsService("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")
        dns_service.del_txt_record(
            "exodev.nl",
            "_acme-challenge.exodev.nl",
            "KEna0LvLAKFIcTCadLBQAH5yq_laL2PSKgNALcck5ms",
        )

        # Check mock calls.
        assert mock_find_dns_zone_by_name.call_count == 1
        assert mock_get_relation.call_count == 1
        assert mock_delete_api_resource.call_count == 1

        # Check call args.
        assert mock_find_dns_zone_by_name.call_args[0][0] == "exodev.nl"
        assert mock_get_relation.call_args[0][0].id() == "BqgWr8dr0XV7"
        assert mock_get_relation.call_args[0][1] == "records"
        assert mock_delete_api_resource.call_args[0][0].id() == "LsaWr8dr0KSa"

    @patch(
        "certbot_dns_exonet.clients.exonet_client.ExonetClient.find_dns_zone_by_name"
    )
    @patch("certbot_dns_exonet.clients.exonet_client.ExonetClient.get_relation")
    @patch("certbot_dns_exonet.clients.exonet_client.ExonetClient.delete_api_resource")
    def test_del_txt_record_no_records(
        self,
        mock_delete_api_resource: Mock,
        mock_get_relation: Mock,
        mock_find_dns_zone_by_name: Mock,
    ) -> None:
        """Test deleting TXT record when no records are found.

        Args:
            mock_delete_api_resource: Mock of
                certbot_dns_exonet.clients.exonet_client.ExonetClient.delete_api_resource.
            mock_get_relation: Mock of
                certbot_dns_exonet.clients.exonet_client.ExonetClient.get_relation.
             mock_find_dns_zone_by_name (Mock): Mock of
                certbot_dns_exonet.clients.exonet_client.ExonetClient.find_dns_zone_by_name.
        """
        zone = ApiResource({"type": "dns_zones", "id": "BqgWr8dr0XV7"})
        zone.attribute("name", "exodev.nl")

        mock_find_dns_zone_by_name.return_value = zone

        mock_get_relation.return_value = None

        dns_service = DnsService("kaSD0ffAD1ldSA92A0KODkaksda02KDAK")

        with raises(PluginError) as e_info:
            dns_service.del_txt_record(
                "exodev.nl",
                "_acme-challenge.exodev.nl",
                "KEna0LvLAKFIcTCadLBQAH5yq_laL2PSKgNALcck5ms",
            )

        # Check error message.
        assert e_info.value.args[0] == f"Unable to find DNS records for {zone}."

        # Check mock calls.
        assert mock_find_dns_zone_by_name.call_count == 1
        assert mock_get_relation.call_count == 1
        assert mock_delete_api_resource.call_count == 0

        # Check call args.
        assert mock_find_dns_zone_by_name.call_args[0][0] == "exodev.nl"
        assert mock_get_relation.call_args[0][0].id() == "BqgWr8dr0XV7"
        assert mock_get_relation.call_args[0][1] == "records"
