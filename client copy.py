from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import base64
import requests
import random

from flask import request, jsonify

SECRET_KEY = b'minhachavesegura'  # Deve ter 16 bytes

def encrypt_message_client(message: str) -> dict:
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

def decrypt_message_client():
    try:
        # Dados enviados pelo cliente
        data = request.json
        encrypted_message = data.get('encrypted_message')
        iv = base64.b64decode(data.get('iv'))  # Vetor de inicialização

        # Decodificar e descriptografar
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
        encrypted_bytes = base64.b64decode(encrypted_message)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)

        decrypted_message = decrypted_bytes.decode('utf-8')

        print(f"\nMensagem Criptografada: {encrypted_message}\nMensagem Descriptografada: {decrypted_message}\n")

        return jsonify({
            'encrypted_message': encrypted_message,
            'decrypted_message': decrypted_message
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Mensagem a ser enviada
message = "Hello Cryptography"

# Envia para o servidor
for i in range(1):
  payload = encrypt_message_client(message)
  response = requests.post('http://127.0.0.1:5000/decrypt', json=payload)
  print(response.json())
