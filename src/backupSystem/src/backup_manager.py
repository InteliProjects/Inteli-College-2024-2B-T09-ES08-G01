import os
from src.google_utils import upload_to_google, list_google_files
from src.backblaze_utils import upload_to_backblaze, list_backblaze_files
from . import config 

LOCAL_DIRECTORY = config.LOCAL_DIRECTORY

def perform_backup():
    # Realiza o backup incremental para Google Cloud e Backblaze.

    # Arquivos existentes nos serviços
    google_files = set(list_google_files())
    backblaze_files = set(list_backblaze_files())

    # Processa os arquivos locais
    for root, _, files in os.walk(LOCAL_DIRECTORY):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, LOCAL_DIRECTORY)

            # Faz upload para o Google se não existir lá
            if relative_path not in google_files:
                upload_to_google(file_path, relative_path)

            # Faz upload para o Backblaze, se não existir lá
            if relative_path not in backblaze_files:
                upload_to_backblaze(file_path, relative_path)
