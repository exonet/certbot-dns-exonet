Certbot plugin for authentication using the Exonet DNS
======================================================

.. image:: https://img.shields.io/pypi/v/certbot-dns-exonet.svg?style=flat-square
    :target: https://pypi.org/project/certbot-dns-exonet
.. image:: https://img.shields.io/pypi/pyversions/certbot-dns-exonet.svg?style=flat-square
    :target: https://pypi.org/project/certbot-dns-exonet
.. image:: https://img.shields.io/pypi/l/certbot-dns-exonet.svg?style=flat-square
    :target: https://github.com/exonet/certbot-dns-exonet/blob/master/LICENSE

`Certbot <https://certbot.eff.org>`_ DNS Authenticator plugin for `Exonet DNS <https://www.exonet.nl>`_.

Conventions
-----------
- Code style guide: PEP 8.
- Docstring conventions: PEP 257 and reStructuredText.

Installation
------------
Install using pip::

 pip install certbot-dns-exonet

Usage
-----

1. Request an Exonet API token (`contact Exonet <https://www.exonet.nl/contact>`_)

2. After the installation, verify if the plugin is available in certbot::

    certbot plugins

3. Create an exonet.ini file::

    touch /etc/letsencrypt/exonet.ini
    chmod 0600 /etc/letsencrypt/exonet.ini

3. Add the Exonet API token in /etc/letsencrypt/exonet.ini::

    certbot_dns_exonet:dns_exonet_token = YOUR_EXONET_API_TOKEN

5. Request a certificate with certbot and this plugin to obtain a certificate using DNS record authentication::

    certbot certonly --authenticator certbot-dns-exonet:dns-exonet --certbot-dns-exonet:dns-exonet-credentials /etc/letsencrypt/exonet.ini -d domain.com

Change log
----------
Please see `CHANGELOG <https://github.com/exonet/certbot-dns-exonet/blob/master/CHANGELOG.md>`_ for more information on what has changed recently.

Security
--------
If you discover any security related issues please email `development@exonet.nl <mailto:development@exonet.nl>`_ instead of using the issue tracker.

Credits
-------
- `Exonet <https://github.com/exonet>`_
- `All Contributors <https://github.com/exonet/certbot-dns-exonet/graphs/contributors>`_

License
-------
The MIT License (MIT). Please see `License File <https://github.com/exonet/certbot-dns-exonet/blob/master/LICENSE>`_ for more information.
