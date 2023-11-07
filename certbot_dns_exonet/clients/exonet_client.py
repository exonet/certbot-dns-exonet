from logging import getLogger
from typing import Optional

from certbot.errors import PluginError
from exonetapi import Client
from exonetapi.structures import ApiResource, ApiResourceSet
from requests.exceptions import HTTPError

LOGGER = getLogger(__name__)


class ExonetClient:
    """Encapsulates all communication with the Exonet API."""

    client: Client

    def __init__(self, token: str) -> None:
        """Exonet client constructor.

        Args:
            token: Exonet token.
        """
        self.client = Client()
        self.client.authenticator.set_token(token)

    def post_api_resource(self, resource: ApiResource) -> ApiResource:
        """Post the Exonet ApiResource.

        Args:
            resource: The Exonet ApiResource.

        Raises:
            PluginError: When resource can not de added.

        Returns:
            ApiResource: The created Exonet ApiResource.
        """
        try:
            return resource.post()
        except HTTPError as exception:
            description = f": {exception.response.text}" if exception.response else ""
            error_message = f"Error adding {type(resource).__name__} using the Exonet API{description}"  # noqa: E501
            LOGGER.debug(error_message)
            raise PluginError(error_message) from exception

    def delete_api_resource(self, resource: ApiResource) -> None:
        """Delete Exonet ApiResource.

        Args:
            resource: The Exonet ApiResource.
        """
        try:
            LOGGER.debug("Deleting DNS record with id: %s", resource.id())
            resource.delete()
        except HTTPError as exception:
            description = f": {exception.response.text}" if exception.response else ""
            LOGGER.warning(
                "Error deleting %s %s using the Exonet API%s",
                type(resource).__name__,
                resource.id(),
                description,
            )

    def get_relation(
        self, resource: ApiResource, relation_name: str
    ) -> Optional[ApiResourceSet]:
        """Get relation for ApiResource based on relation name.

        Args:
            resource: The Exonet ApiResource.
            relation_name: The name of the relation.

        Returns:
            Optional[ApiResourceSet]: ApiResourceSet if found.
        """
        try:
            return resource.related(relation_name).get()
        except HTTPError as exception:
            description = f": {exception.response.text}" if exception.response else ""
            LOGGER.debug(
                "Error getting %s from the Exonet API%s",
                type(resource).__name__,
                description,
            )
            return None

    def find_dns_zone_by_name(self, domain: str) -> Optional[ApiResource]:
        """Find the domain resource for a given domain.

        Args:
            domain: The registered domain name.

        Raises:
            PluginError: If no matching domain is found.

        Returns:
            The domain, if found.
        """
        try:
            # Get zone based on attribute name.
            zones = (
                self.client.resource("dns_zones")
                .filter("name", domain)
                .get()
                .resources()
            )
        except HTTPError as exception:
            status_code = exception.response.status_code if exception.response else None
            hint = "(Did you provide a valid API token?)" if status_code == 401 else ""
            error_message = (
                f"Error finding DNS zone using the Exonet API: {exception}{hint}"
            )
            LOGGER.debug(error_message)
            raise PluginError(error_message) from exception

        return zones[0] if zones else None
