#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
 signer.py
 Certificate Generator

 Copyright (c) 2014 David Wittman <david@wittman.com>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

from string import hexdigits

from Crypto.Random import random
from OpenSSL import crypto

class CertificateGenerator(object):
    def __init__(self, key_bit_length, form_values):
        self.certificate_info = self._validate(form_values)
        self.keypair = self.generate_rsa_keypair(crypto.TYPE_RSA, key_bit_length)

    def _validate(self, form_values):
        valid = {}
        fields = ('C', 'ST', 'L', 'O', 'OU', 'CN')
        optional = ('OU',)

        for field in fields:
            try:
                valid[field] = form_values[field]
            except KeyError:
                if field not in optional:
                    raise

        return valid

    def generate_rsa_keypair(self, key_type, key_bit_length):
        "Generates a public/private key pair of the type key_type and size key_bit_length"
        key = crypto.PKey()
        key.generate_key(key_type, key_bit_length)
        return key

    @property
    def private_key(self):
        return crypto.dump_privatekey(crypto.FILETYPE_PEM, self.keypair)

    @property
    def certificate(self):
        digest = "sha256"
        serial = random.getrandbits(256)
        ca_certfile = open('ca_cert.pem', 'r').read()
        ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, ca_certfile)
        ca_keyfile = open('ca_privkey.pem', 'r').read()
        ca_privkey = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_keyfile)
        cert = crypto.X509()
        subject = cert.get_subject()

        for (k,v) in self.certificate_info.items():
            setattr(subject, k, v)

        cert.set_issuer(ca_cert.get_subject())
        cert.set_serial_number(serial)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(3650*24*60*60)
        cert.set_pubkey(self.keypair)
        cert.sign(ca_privkey, digest)
        return crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
