# Certbot plugin for authentication using the Exonet DNS

[![pypi]](https://pypi.org/project/certbot-dns-exonet)
[![Python]](https://pypi.org/project/certbot-dns-exonet)
[![License]](https://github.com/exonet/certbot-dns-exonet/blob/master/LICENSE)

[Certbot] DNS Authenticator plugin for [Exonet DNS]


# Conventions
- Code style guide: PEP 8.
- Docstring conventions: Google Python Style Guide and Markdown.

# Installation
Install using pip:
```bash
    pip install certbot-dns-exonet
```

# Usage
1. Request an Exonet API token ([contact Exonet])

2. After the installation, verify if the plugin is available in certbot:
    ```bash
        certbot plugins
    ```
3. Create an exonet.ini file:
    ```bash
        touch /etc/letsencrypt/exonet.ini
        chmod 0600 /etc/letsencrypt/exonet.ini
    ```
3. Add the Exonet API token in /etc/letsencrypt/exonet.ini:
    ```bash
        dns_exonet_token = YOUR_EXONET_API_TOKEN
    ```
5. Request a certificate with certbot and this plugin to obtain a certificate using DNS record authentication:
    ```bash
        certbot certonly \
            --config-dir /etc/letsencrypt \
            --work-dir /etc/letsencrypt \
            --logs-dir /etc/letsencrypt \
            --authenticator dns-exonet \
            --dns-exonet-credentials /etc/letsencrypt/exonet.ini \
            -d domain.com
    ```

# Change log
Please see [releases] for more information on what has changed recently.

# Security
If you discover any security related issues please email [development@exonet.nl] instead of using the issue tracker.

# Credits
- [Exonet]
- [All Contributors]

# License
The MIT License (MIT). Please see [License File] for more information.

<!-- MARKDOWN LINKS & IMAGES -->
[pypi]: https://img.shields.io/pypi/v/certbot-dns-exonet.svg?style=flat-square
[Python]: https://img.shields.io/pypi/pyversions/certbot-dns-exonet.svg?style=flat-square
[License]:https://img.shields.io/pypi/l/certbot-dns-exonet.svg?style=flat-square
[Certbot]: https://certbot.eff.org
[Exonet DNS]: https://www.exonet.nl
[contact Exonet]: https://www.exonet.nl/contact
[releases]: https://github.com/exonet/certbot-dns-exonet/releases
[development@exonet.nl]: mailto:development@exonet.nl
[Exonet]: https://github.com/exonet
[All Contributors]: https://github.com/exonet/certbot-dns-exonet/graphs/contributors
[License File]: https://github.com/exonet/certbot-dns-exonet/blob/master/LICENSE
