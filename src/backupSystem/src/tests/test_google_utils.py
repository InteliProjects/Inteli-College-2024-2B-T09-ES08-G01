from unittest.mock import patch, MagicMock
from src.google_utils import upload_to_google, list_google_files, initialize_google_client

# Teste para verificar a inicialização do cliente Google Cloud
@patch('google.cloud.storage.Client')
def test_initialize_google_client(MockClient):
    # Teste a inicialização do cliente
    initialize_google_client()
    MockClient.assert_called_once()

# Teste para verificar o upload para o Google Cloud
@patch('google.cloud.storage.Client')
def test_upload_to_google(MockClient):
    # Simulando o upload de arquivo
    mock_blob = MagicMock()
    mock_bucket = MagicMock()
    MockClient.return_value.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob

    upload_to_google('fake_path/file.pdf', 'file.pdf')

    mock_blob.upload_from_filename.assert_called_with('fake_path/file.pdf')

# Teste para verificar a listagem de arquivos no Google Cloud
@patch('google.cloud.storage.Client')
def test_list_google_files(MockClient):
    # Simulando listagem de arquivos
    mock_bucket = MagicMock()
    MockClient.return_value.bucket.return_value = mock_bucket
    mock_blob = MagicMock()
    mock_blob.name = 'file.pdf'
    mock_bucket.list_blobs.return_value = [mock_blob]

    files = list_google_files()
    
    assert 'file.pdf' in files
