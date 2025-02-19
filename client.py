from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import base64
import requests
import random

SECRET_KEY = b'minhachavesegura'  # Deve ter 16 bytes

def encrypt_message(message: str) -> dict:
    iv = get_random_bytes(16)  # IV aleatório
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_message)
    
    # encrypted_bytes = bytearray(encrypted_bytes)
    # random_index = random.randint(0, len(encrypted_bytes) - 1)
    # encrypted_bytes[random_index] ^= 0xFF

    return {
        'encrypted_message': base64.b64encode(encrypted_bytes).decode('utf-8'),
        'iv': base64.b64encode(iv).decode('utf-8')
    }

# Mensagem a ser enviada
message = "Hello Cryptography"

# Envia para o servidor
for i in range(10):
  payload = encrypt_message(message)
  response = requests.post('http://127.0.0.1:5000/decrypt', json=payload)
  print(response.json())
