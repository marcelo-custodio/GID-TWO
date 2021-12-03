from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

private_key = rsa.generate_private_key(public_exponent=65537, key_size=512)
pem_private = private_key.private_bytes(encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption())
key_private = pem_private
print(key_private)

print()

public_key = private_key.public_key()
pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.PKCS1)
key_public = pem_public
print(key_public)