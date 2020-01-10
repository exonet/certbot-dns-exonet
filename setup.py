import sys

from setuptools import find_packages
from setuptools import setup

version = '1.0.0'

install_requires = [
    'acme',
    'certbot',
    'exonetapi>=2.1.0',
    'tldextract',
    'setuptools',
    'requests',
    'zope.interface',
]

setup(
    name='certbot-dns-exonet',
    version=version,
    description="Exonet DNS Authenticator plugin for Certbot",
    url='https://github.com/exonet/certbot-dns-exonet',
    author="Exonet B.V.",
    author_email='development@exonet.nl',
    license='MIT',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dns-exonet = certbot_dns_exonet._internal.dns_exonet:Authenticator',
        ],

    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
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
