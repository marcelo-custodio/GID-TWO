from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

private_key = rsa.generate_private_key(public_exponent=65537, key_size=1024)
pem_private = private_key.private_bytes(encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption())
key_private = pem_private
with open('keys/private_key.pem', 'wb') as f:
    f.write(pem_private)
    f.close()
print(key_private.decode('UTF-8'))

print()

public_key = private_key.public_key()
pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.PKCS1)
key_public = pem_public
with open('keys/public_key.pem', 'wb') as f:
    f.write(pem_public)
    f.close()
print(key_public.decode('UTF-8'))

message = b"encrypted data"
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print()
print(base64.encodebytes(ciphertext).decode('UTF-8'))

plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print(plaintext == message)

print(plaintext)