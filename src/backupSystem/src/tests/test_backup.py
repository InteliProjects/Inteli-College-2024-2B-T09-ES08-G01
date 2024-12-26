import os
import pytest
from unittest.mock import patch

# Simulando a função de upload para o Google e Backblaze
def mock_upload_to_google(file_path, relative_path):
    return f"Uploaded {relative_path} to Google Cloud"

def mock_upload_to_backblaze(file_path, relative_path):
    return f"Uploaded {relative_path} to Backblaze"


@patch("src.google_utils.upload_to_google", side_effect=mock_upload_to_google)
@patch("src.backblaze_utils.upload_to_backblaze", side_effect=mock_upload_to_backblaze)
def test_simple_backup(mock_upload_to_google, mock_upload_to_backblaze):
    # Criando um arquivo no diretório local
    LOCAL_DIRECTORY = "/fake/local/directory"
    os.makedirs(LOCAL_DIRECTORY, exist_ok=True)
    file_path = os.path.join(LOCAL_DIRECTORY, "file1.txt")
    with open(file_path, "w") as f:
        f.write("File content")

    # Simulando o upload para o Google 
    mock_upload_to_google(file_path, "file1.txt")

    # Verificando se a função de upload foi chamada
    mock_upload_to_google.assert_called_with(file_path, "file1.txt")
    mock_upload_to_backblaze.assert_not_called()

   
