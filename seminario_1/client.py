from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import base64
import requests
import random

from flask import request, jsonify

# Chave simétrica compartilhada (deve ser segura e igual à usada pelo servidor)
SECRET_KEY = b'minhachavesegura'  # 16 bytes para AES-128

def encrypt_message(message: str, iv: str) -> bytes:
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_message)
    
    # Para embaralhar os bytes da mensagem criptografada, não deu certo
    # encrypted_bytes = bytearray(encrypted_bytes)
    # random_index = random.randint(0, len(encrypted_bytes) - 1)
    # encrypted_bytes[random_index] ^= 0xFF

    return encrypted_bytes

def build_payload(encrypted_bytes, iv: str) -> dict:
   return {
        'encrypted_message': base64.b64encode(encrypted_bytes).decode('utf-8'),
        'iv': base64.b64encode(iv).decode('utf-8')
    }

def decrypt_message(encrypted_message, iv: str) -> str:
    # Decodificar e descriptografar
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    encrypted_bytes = base64.b64decode(encrypted_message)
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)

    decrypted_message = decrypted_bytes.decode('utf-8')

    return decrypted_message

# Mensagem a ser enviada
message = "Hello from client"

# Envia para o servidor
for i in range(10):
  iv = get_random_bytes(16)  # IV aleatório

  encrypted_message = encrypt_message(message, iv)
  payload = build_payload(encrypted_message, iv)
  print(payload)
  response = requests.post('http://127.0.0.1:5000/decrypt', json=payload)

  try:
    data = response.json()
    encrypted_message = data.get('encrypted_message')
    iv = base64.b64decode(data.get('iv')) # Não precisaria no nosso caso, mas deixamos caso os servidor altere o iv

    decrypted_message = decrypt_message(encrypted_message, iv)

    print(f"\n- Pacote do Servidor\n{data}")
    print(f"- Mensagem do Servidor Criptografada\n{encrypted_message}")
    print(f"- Mensagem do Servidor Descriptografada\n{decrypted_message}", end="\n\n")

  except Exception as e:
    print(data)

