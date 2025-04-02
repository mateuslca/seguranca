import os
import argparse
import glob
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

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

def main(args):
  input_path = args.input

  if not os.path.isdir(input_path):
      print("Precisa ser um diretório")
      return

  # Para teste
  if not input_path.endswith("files"):
      print("CUIDADO")
      return
  
  # Carregar a chave privada
  with open("private_key.pem", "rb") as f:
      private_key = serialization.load_pem_private_key(f.read(), password=None)

  for root, _, files in os.walk(input_path):
        for file in files:
          filepath = os.path.join(root, file)
          if not filepath.endswith(".enc"):
                continue
          decrypt_file(filepath, private_key)
          
  print("Arquivos descriptografados com sucesso!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True)
    args = parser.parse_args()

    main(args)