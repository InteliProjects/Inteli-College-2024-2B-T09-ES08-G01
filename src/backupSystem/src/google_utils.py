import os
from google.cloud import storage
from reportlab.pdfgen import canvas
import sys
sys.path.append('src')

from . import config 

GOOGLE_CONFIG = config.GOOGLE_CONFIG


def initialize_google_client():
    # Certificando que o caminho das credenciais seja absoluto
    credentials_path = os.path.abspath(GOOGLE_CONFIG["credentials_path"])

    # Inicializa a variável de ambiente com o caminho absoluto do arquivo de credenciais
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    return storage.Client()


def upload_to_google(file_path, destination_blob_name):
    # Faz upload de um arquivo para o bucket do Google Cloud.
    client = initialize_google_client()
    bucket = client.bucket(GOOGLE_CONFIG["bucket_name"])  
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(file_path)
    print(f"Arquivo {file_path} carregado para {destination_blob_name} no Google Cloud.")


def list_google_files():
    # Lista os arquivos no bucket do Google Cloud.
    client = initialize_google_client()
    bucket = client.bucket(GOOGLE_CONFIG["bucket_name"])  
    blobs = list(bucket.list_blobs())
    return [blob.name for blob in blobs]


def create_pdf(file_path):
    # Gera um arquivo PDF no caminho especificado.
    c = canvas.Canvas(file_path)
    c.drawString(100, 750, "Este é um PDF gerado dinamicamente!")
    c.drawString(100, 730, "Use este PDF como exemplo para uploads.")
    c.save()
    print(f"PDF gerado em: {file_path}")


def perform_backup():
    # Diretório local para PDFs
    LOCAL_DIRECTORY = "local_pdfs/"
    os.makedirs(LOCAL_DIRECTORY, exist_ok=True)

    # Lista de arquivos no diretório local
    local_files = os.listdir(LOCAL_DIRECTORY)
    if not local_files:
        print("Nenhum arquivo encontrado no diretório local para backup.")
        return

    # Realizar uploads para o Google Cloud
    for file_name in local_files:
        local_path = os.path.join(LOCAL_DIRECTORY, file_name)
        try:
            upload_to_google(local_path, file_name)
            print(f"Upload concluído: {file_name}")
        except Exception as e:
            print(f"Erro ao fazer upload de {file_name}: {e}")
