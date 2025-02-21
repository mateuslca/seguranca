from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
import base64

app = Flask(__name__)

# Chave simétrica compartilhada (deve ser segura e igual à usada pelo cliente)
SECRET_KEY = b'minhachavesegura'  # 16 bytes para AES-128

def encrypt_message_server(message: str, iv: str) -> dict:
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

@app.route('/decrypt', methods=['POST'])
def decrypt_message():
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

if __name__ == '__main__':
    app.run(debug=True)
