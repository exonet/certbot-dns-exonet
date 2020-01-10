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

2. Install the plugin using `pip install certbot-dns-exonet`

3. Create an `exonet.ini` config file with your Exonet API token in it::

    # Exonet API token used by Certbot.
    certbot_dns_exonet:dns_exonet_token = YOUR_API_TOKEN


  Where `YOUR_API_TOKEN` should be replaced by your actual Exonet API token.

4. Set the right permissions on the credentials file to prevent unauthorized access by other users::

    chmod 600 exonet.ini
   
5. Run `certbot` with this plugin as the authenticator and tell it to use the exonet.ini credentials file to connect to the Exonet DNS like so::

    certbot certonly --authenticator certbot-dns-exonet:dns-exonet --certbot-dns-exonet:dns-exonet-credentials exonet.ini -d domain.com

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
