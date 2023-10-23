from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys
import os

ACTIONS = ["E", "D"]

# Pad data to be a multiple of 16 bytes
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

# Encrypt file
def encrypt_file(key, filename):
    with open(filename, "rb") as f:
        data = f.read()

    data = pad(data)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = iv + cipher.encrypt(data)

    with open(filename + ".enc", "wb") as f:
        f.write(encrypted_data)

# Unpad the data
def unpad(s):
    return s.rstrip(b"\0")

# Decrypt file
def decrypt_file(key, filename):
    with open(filename, "rb") as f:
        data = f.read()

    iv = data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(data[AES.block_size:])
    decrypted_data = unpad(decrypted_data)

    filename = filename[:-4]
    with open(filename, "wb") as f:  # Remove the .enc extension
        f.write(decrypted_data)

# Example usage
if __name__ == "__main__":
    args = sys.argv
    filename = args[1]
    if not os.path.exists(filename):
        print("File does not exist")
        sys.exit(0)

    actions = ["E", "D"]
    action = args[2]
    if action not in actions:
        print("Invalid action")
        sys.exit(0)

    key = args[3]
    key = key.strip().encode('utf-8')
    if not key:
        print("Invalid key")
        sys.exit(0)

    if action == "E":
        try:
            encrypt_file(key, filename)
            os.remove(filename)
            print("Encrypted")
        except Exception as e:
            print(e)
        
    else:
        decrypt_file(key, filename)
        print("Decrypted")
    print("Done.")