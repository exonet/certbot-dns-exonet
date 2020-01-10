"""DNS Authenticator for Exonet."""
import logging

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

from exonetapi import Client as ExonetClient
from exonetapi.structures import ApiResource
from requests.exceptions import HTTPError

from tldextract import extract as tldextract
import zope.interface

logger = logging.getLogger(__name__)

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Exonet

    This Authenticator uses the Exonet API to fulfill a dns-01 challenge.
    """
    description = 'Obtain certificates using a DNS TXT record with the Exonet DNS.'

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add)
        add('credentials', help='Exonet credentials INI file.')

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using the \
            Exonet API.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'Exonet credentials INI file',
            {
                'token': 'API token for Exonet API'
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_exonet_client().add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_exonet_client().del_txt_record(domain, validation_name, validation)

    def _get_exonet_client(self):
        return _ExonetClient(self.credentials.conf('token'))


class _ExonetClient(object):
    """
    Encapsulates all communication with the Exonet API.
    """

    def __init__(self, token):
        self.manager = ExonetClient()
        self.manager.authenticator.set_token(token)

    def add_txt_record(self, domain_name, record_name, record_content):
        """
        Add a TXT record using the supplied information.

        :param str domain_name: The domain to use to associate the record with.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :raises certbot.errors.PluginError: if an error occurs communicating with the Exonet API.
        """
        try:
            domain = self._find_zone(domain_name)
        except HTTPError as exception:
            hint = None

            if exception.response.status_code == 401:
                hint = 'Did you provide a valid API token?'

            error_message = 'Error finding DNS zone using the Exonet API: {0}{1}'\
                .format(exception, ' ({0})'.format(hint) if hint else '')
            logger.debug(error_message)
            raise errors.PluginError(error_message)

        try:
            logger.debug('Adding TXT record to DNS.')

            # Add the TXT record to the DNS.
            record = ApiResource('dns_records')
            record.attribute('type', 'TXT')
            record.attribute('name', self._compute_record_name(domain, record_name))
            record.attribute('content', self._compute_record_content(record_content))
            record.attribute('ttl', 3600)
            record.relationship('zone', domain)
            created_record = record.post()

            logger.debug('Successfully added TXT record with id: %s', created_record.id())
        except HTTPError as exception:
            error_message = 'Error adding TXT record using the Exonet API: {0}'\
                .format(exception.response.text)
            logger.debug(error_message)
            raise errors.PluginError(error_message)

    def del_txt_record(self, domain_name, record_name, record_content):
        """
        Delete a TXT record using the supplied information.

        Note that both the record's name and content are used to ensure that similar records
        created concurrently (e.g., due to concurrent invocations of this plugin) are not deleted.

        Failures are logged, but not raised.

        :param str domain_name: The domain to use to associate the record with.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        """
        try:
            domain = self._find_zone(domain_name)
        except HTTPError as exception:
            logger.debug('Error finding domain using the Exonet API: %s', exception)
            return

        try:
            domain_records = domain.related('records').get()

            matching_records = [record for record in domain_records
                                if record.attribute('type') == 'TXT'
                                and record.attribute('name') == self._compute_record_name(domain, record_name)
                                and record.attribute('content') == self._compute_record_content(record_content)
                                ]
        except HTTPError as exception:
            logger.debug(
                'Error removing TXT record from the Exonet API: %s',
                exception.response.text
            )
            return

        for record in matching_records:
            try:
                logger.debug('Deleting DNS record with id: %s', record.id())
                record.delete()
            except HTTPError as exception:
                logger.warning(
                    'Error deleting TXT record %s using the Exonet API: %s',
                    record.id(),
                    exception
                )

    def _find_zone(self, domain_name):
        """
        Find the domain resource for a given domain name.

        :param str domain_name: The domain name for which to find the corresponding Domain.
        :returns: The Domain, if found.
        :rtype: `~exonetapi.Resource`
        :raises certbot.errors.PluginError: if no matching Domain is found.
        """
        # Convert to registered domain.
        domain = tldextract(domain_name).registered_domain
        # Get all available zones.
        zones = self.manager.resource('dns_zones').filter('name', domain).get()

        # See if any zones match.
        matches = [zone for zone in zones if zone.attribute('name') == domain]

        # If a match is found, return it.
        if matches:
            zone = matches[0]
            logger.debug('Found DNS zone %s for domain %s', zone.attribute('name'), domain_name)
            return zone

        raise errors.PluginError('Unable to find DNS zone for {0}. Zone {1} not found.'
                                 .format(domain_name, domain))

    @staticmethod
    def _compute_record_name(domain, full_record_name):
        # The name of the DNS record, without the DNS zone name.
        return full_record_name.rpartition("." + domain.attribute('name'))[0]

    @staticmethod
    def _compute_record_content(record_content):
        # The DNS record content within quotes.
        return "\""+record_content+"\""
