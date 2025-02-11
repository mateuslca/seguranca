from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import requests

SECRET_KEY = b'minhachavesegura'  # Deve ter 16 bytes
iv = b'1234567890abcdef'  # 16 bytes

def encrypt_message(message: str) -> dict:
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_message)
    return {
        'encrypted_message': base64.b64encode(encrypted_bytes).decode('utf-8'),
        'iv': base64.b64encode(iv).decode('utf-8')
    }

# Mensagem a ser enviada
message = "Hello Cryptography"
payload = encrypt_message(message)

# Envia para o servidor
response = requests.post('http://127.0.0.1:5000/decrypt', json=payload)
print(response.json())
