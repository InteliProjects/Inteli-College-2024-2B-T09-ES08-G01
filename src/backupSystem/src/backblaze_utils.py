from b2sdk.v2 import InMemoryAccountInfo, B2Api
from . import config 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

BACKBLAZE_CONFIG = config.BACKBLAZE_CONFIG

def initialize_backblaze_client():
    # Inicializa o cliente do Backblaze.
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account("production", BACKBLAZE_CONFIG["application_key_id"], BACKBLAZE_CONFIG["application_key"])
    return b2_api

def create_pdf(file_path, text):
    # Cria um PDF simples com o texto fornecido.
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    # Adiciona o texto ao PDF
    c.drawString(100, height - 100, text)
    
    # Salva o PDF no caminho especificado
    c.save()

def upload_to_backblaze(file_path, destination_file_name):
    # Faz upload de um arquivo para o bucket do Backblaze.
    b2_api = initialize_backblaze_client()
    bucket = b2_api.get_bucket_by_name(BACKBLAZE_CONFIG["bucket_name"])
    bucket.upload_local_file(local_file=file_path, file_name=destination_file_name)
    print(f"Arquivo {file_path} carregado para {destination_file_name} no Backblaze.")

def list_backblaze_files():
    b2_api = initialize_backblaze_client()
    bucket = b2_api.get_bucket_by_name(BACKBLAZE_CONFIG["bucket_name"])
    
    # Extrai o nome do arquivo
    return [file_info[0].file_name.split('/')[-1] for file_info in bucket.ls()]


def generate_and_upload_pdf():
    # Gera um PDF e faz upload para o Backblaze
    pdf_file_path = "meu_pdf.pdf"  
    text = "Este é um PDF de exemplo gerado para upload no Backblaze."  
    
    create_pdf(pdf_file_path, text) 
    destination_file_name = "backup/meu_pdf_no_backblaze.pdf"  
    upload_to_backblaze(pdf_file_path, destination_file_name) 

    # Remover o arquivo temporário
    os.remove(pdf_file_path)
    print(f"PDF {pdf_file_path} removido do sistema local após o upload.")

