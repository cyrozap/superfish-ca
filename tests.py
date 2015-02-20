#!/usr/bin/env python

import unittest

from nose.tools import raises, assert_equal

from signer import CertificateGenerator

class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.certificate_info = {
                         'C': 'US',
                         'ST': 'Texas',
                         'L': 'San Antonio',
                         'O': 'Big Bob\'s Beepers',
                         'OU': 'Marketing',
                         'CN': 'example.com'
                        }

    def test_keypair_type(self):
        import OpenSSL.crypto
        cert_generator = CertificateGenerator(2048, self.certificate_info)
        self.assertTrue(isinstance(cert_generator.keypair, OpenSSL.crypto.PKey))

    def test_keypair_bits(self):
        cert_generator = CertificateGenerator(2048, self.certificate_info)
        assert_equal(cert_generator.keypair.bits(), 2048)

        cert_generator = CertificateGenerator(1024, self.certificate_info)
        assert_equal(cert_generator.keypair.bits(), 1024)

    def test_certificate_length(self):
        cert_generator = CertificateGenerator(2048, self.certificate_info)
        assert_equal(len(cert_generator.certificate), 1066)

    def test_certificate_starts_with(self):
        cert_generator = CertificateGenerator(2048, self.certificate_info)
        self.assertTrue(cert_generator.certificate.startswith('-----BEGIN CERTIFICATE-----'))

    def test_certificate_ends_with(self):
        cert_generator = CertificateGenerator(2048, self.certificate_info)
        self.assertTrue(cert_generator.certificate.endswith('-----END CERTIFICATE-----\n'))

    def test_private_key_starts_with(self):
        cert_generator = CertificateGenerator(2048, self.certificate_info)
        self.assertTrue(cert_generator.private_key.startswith('-----BEGIN PRIVATE KEY-----'))

    def test_private_key_ends_with(self):
        cert_generator = CertificateGenerator(2048, self.certificate_info)
        self.assertTrue(cert_generator.private_key.endswith('-----END PRIVATE KEY-----\n'))

class ExceptionTests(unittest.TestCase):
    @raises(KeyError)
    def test_missing_country(self):
        certificate_info = {
                    'ST': 'Texas',
                    'L': 'San Antonio',
                    'O': 'Big Bob\'s Beepers',
                    'CN': 'example.com'
                   }
        CertificateGenerator(2048, certificate_info)

    @raises(KeyError)
    def test_missing_state(self):
        certificate_info = {
                    'C': 'US',
                    'L': 'San Antonio',
                    'O': 'Big Bob\'s Beepers',
                    'CN': 'example.com'
                   }
        CertificateGenerator(2048, certificate_info)

    @raises(KeyError)
    def test_missing_locality(self):
        certificate_info = {
                    'C': 'US',
                    'ST': 'Texas',
                    'O': 'Big Bob\'s Beepers',
                    'CN': 'example.com'
                   }
        CertificateGenerator(2048, certificate_info)

    @raises(KeyError)
    def test_missing_organization(self):
        certificate_info = {
                    'C': 'US',
                    'ST': 'Texas',
                    'L': 'San Antonio',
                    'CN': 'example.com'
                   }
        CertificateGenerator(2048, certificate_info)

    @raises(KeyError)
    def test_missing_common_name(self):
        certificate_info = {
                    'C': 'US',
                    'ST': 'Texas',
                    'L': 'San Antonio',
                    'O': 'Big Bob\'s Beepers'
                   }
        CertificateGenerator(2048, certificate_info)
