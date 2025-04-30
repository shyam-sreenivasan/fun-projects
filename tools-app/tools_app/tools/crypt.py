from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64


# Unpad the data
def unpad(s):
    return s.rstrip(b"\0")

# Pad data to be a multiple of 16 bytes
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt_string(key: bytes, plaintext: str) -> str:
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode('utf-8'))
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(iv + encrypted).decode('utf-8')

def decrypt_string(key: bytes, ciphertext_b64: str) -> str:
    data = base64.b64decode(ciphertext_b64)
    iv = data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(data[AES.block_size:])
    return unpad(decrypted_padded).decode('utf-8')
