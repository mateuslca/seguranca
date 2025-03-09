import os
import glob
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

# Carregar a chave privada
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Função para descriptografar arquivos
def decrypt_file(filepath, private_key):
    with open(filepath, "rb") as f:
        ciphertext = f.read()

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Salvar o arquivo original
    original_filepath = filepath.replace(".enc", "")
    with open(original_filepath, "wb") as f:
        f.write(plaintext)

    os.remove(filepath)  # Remove o arquivo criptografado

# Descriptografa todos os arquivos de um diretório
def decrypt_directory(directory, private_key):
    for filepath in glob.glob(os.path.join(directory, "*.enc")):
        decrypt_file(filepath, private_key)

# Definir o diretório alvo
directory = "files"

decrypt_directory(directory, private_key)
print("Arquivos descriptografados com sucesso!")
