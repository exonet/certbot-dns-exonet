import sys

from setuptools import setup, find_packages

from codecs import open
from os import path


version = '1.0.4'

install_requires = [
    'acme',
    'certbot',
    'exonetapi>=3.0.3',
    'tldextract',
    'setuptools',
    'requests',
    'zope.interface',
]

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='certbot-dns-exonet',
    version=version,
    description="Exonet DNS Authenticator plugin for Certbot",
    long_description=long_description,
    url='https://github.com/exonet/certbot-dns-exonet',
    author="Exonet B.V.",
    author_email='development@exonet.nl',
    license='MIT',
    python_requires='>=3.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dns-exonet = certbot_dns_exonet._internal.dns_exonet:Authenticator',
        ],

    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
)
