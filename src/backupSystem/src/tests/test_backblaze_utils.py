import os
import tempfile
from unittest.mock import patch, MagicMock
from .. import backblaze_utils 

upload_to_backblaze = backblaze_utils.upload_to_backblaze
list_backblaze_files = backblaze_utils.list_backblaze_files
initialize_backblaze_client = backblaze_utils.initialize_backblaze_client

# Teste para inicialização do cliente Backblaze
from unittest.mock import patch
from src.backblaze_utils import initialize_backblaze_client

@patch('src.backblaze_utils.B2Api')  
def test_initialize_backblaze_client(MockB2Api):
    initialize_backblaze_client()
    
    # Verifica se o método `B2Api` foi chamado uma vez
    MockB2Api.assert_called_once()

    # Verifica se o método `authorize_account` foi chamado com os parâmetros certos
    MockB2Api.return_value.authorize_account.assert_called_once_with(
        "production",
        "0056989592890500000000002",  
        "K005UNLVkLlHxN//pqmNLSuI5V9aCRU"
    )

def test_upload_to_backblaze():
    # Criar um arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"Teste de upload para o Backblaze.")
        temp_file_path = temp_file.name

    # Nome do arquivo no bucket
    destination_file_name = "test_folder/test_file.pdf"

    try:
        # Realiza o upload do arquivo
        upload_to_backblaze(temp_file_path, destination_file_name)

        # Lista arquivos no bucket para verificar se o upload foi bem-sucedido
        uploaded_files = list_backblaze_files()

        # Verifica se o arquivo foi carregado corretamente
        assert destination_file_name.split('/')[-1] in uploaded_files, f"Arquivo {destination_file_name} não encontrado no bucket."

        # Obter o file_id para deletar o arquivo
        b2_api = initialize_backblaze_client()
        bucket = b2_api.get_bucket_by_name("backup-ipt-3")

        # Listar arquivos no bucket e obter o file_id
        for file_info, _ in bucket.ls():  # Acessando corretamente o id_
            if file_info.file_name == destination_file_name:
                file_id = file_info.id_  # Usando o id_ em vez de file_id
                break

      
        bucket.delete_file_version(file_id, destination_file_name)

    finally:
        os.remove(temp_file_path)

@patch('b2sdk.v2.B2Api')
def test_list_backblaze_files(MockB2Api):
    # Simulando listagem de arquivos
    mock_bucket = MagicMock()
    MockB2Api.return_value.get_bucket_by_name.return_value = mock_bucket
    
    # Simula o retorno do ls como uma lista de tuplas (file_info, other_data)
    mock_file_info = MagicMock()
    mock_file_info.file_name = 'test_folder/test_file.pdf'  
    
    # Simula o retorno de ls() do bucket com a lista de arquivos
    mock_bucket.ls.return_value = [(mock_file_info, )]  # ls retorna uma lista de tuplas
    
    # Chama a função
    files = list_backblaze_files()

    # Verifica se o nome do arquivo está na lista
    assert 'test_file.pdf' in files  
