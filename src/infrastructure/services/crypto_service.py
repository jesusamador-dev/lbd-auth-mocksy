import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class CryptoService:
    @staticmethod
    def jwk_to_pem(jwk):
        """Convert a JWK to a PEM formatted public key."""
        n_decoded = base64.urlsafe_b64decode(jwk['n'] + '===')
        e_decoded = base64.urlsafe_b64decode(jwk['e'] + '===')
        n = int.from_bytes(n_decoded, 'big')
        e = int.from_bytes(e_decoded, 'big')

        public_number = rsa.RSAPublicNumbers(e, n)
        public_key = public_number.public_key(default_backend())
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')
