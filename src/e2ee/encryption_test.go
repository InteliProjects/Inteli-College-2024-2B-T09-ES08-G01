package main

import (
	"database/sql"
	"fmt"
	"os"
	"testing"

	_ "github.com/mattn/go-sqlite3"
)

func setupTestDatabase() (*sql.DB, error) {
	// Cria um banco de dados na memória para testes
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		return nil, err
	}

	// Cria a tabela para armazenar mensagens criptografadas
	_, err = db.Exec(`CREATE TABLE messages (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		filename TEXT NOT NULL,
		data TEXT NOT NULL
	);`)
	if err != nil {
		return nil, err
	}

	return db, nil
}

// Testa salvar e listar mensagens criptografadas no banco de dados
func TestSaveAndRetrieveEncryptedMessages(t *testing.T) {
	key := generateKey()

	// Configura o banco de dados de teste
	db, err := setupTestDatabase()
	if err != nil {
		t.Fatalf("Erro ao configurar o banco de dados: %v", err)
	}
	defer db.Close()

	// Mensagens de exemplo para criptografar e salvar
	messages := []string{
		"Primeira mensagem confidencial",
		"Segunda mensagem criptografada",
		"Mensagem importante em repouso",
	}

	// Criptografa e salva as mensagens
	for i, message := range messages {
		encryptedMessage, err := encrypt(message, key)
		if err != nil {
			t.Fatalf("Erro ao criptografar a mensagem '%s': %v", message, err)
		}
		filename := fmt.Sprintf("mockfile%d.txt", i+1) // Nome fictício para testes
		if err := saveEncryptedMessage(db, filename, encryptedMessage); err != nil {
			t.Fatalf("Erro ao salvar a mensagem criptografada no banco: %v", err)
		}
	}

	// Recupera e imprime as mensagens criptografadas
	rows, err := db.Query("SELECT id, filename, data FROM messages")
	if err != nil {
		t.Fatalf("Erro ao recuperar as mensagens do banco: %v", err)
	}
	defer rows.Close()

	fmt.Println("Mensagens criptografadas armazenadas no banco de dados (para verificação):")
	for rows.Next() {
		var id int
		var filename, encryptedMessage string
		if err := rows.Scan(&id, &filename, &encryptedMessage); err != nil {
			t.Fatalf("Erro ao escanear os resultados: %v", err)
		}
		fmt.Printf("ID: %d, Arquivo: %s, Mensagem Criptografada: %s\n", id, filename, encryptedMessage)
	}

	if err := rows.Err(); err != nil {
		t.Fatalf("Erro ao iterar pelos resultados: %v", err)
	}
}

// Testa a descriptografia para garantir que as mensagens podem ser recuperadas
func TestDecryptMessages(t *testing.T) {
	key := generateKey()

	// Configura o banco de dados de teste
	db, err := setupTestDatabase()
	if err != nil {
		t.Fatalf("Erro ao configurar o banco de dados: %v", err)
	}
	defer db.Close()

	// Mensagem de exemplo para criptografia e descriptografia
	plaintext := "Teste de criptografia e descriptografia"
	encryptedMessage, err := encrypt(plaintext, key)
	if err != nil {
		t.Fatalf("Erro ao criptografar a mensagem: %v", err)
	}

	// Salva a mensagem criptografada no banco
	filename := "mockfile.txt" // Nome fictício para testes
	if err := saveEncryptedMessage(db, filename, encryptedMessage); err != nil {
		t.Fatalf("Erro ao salvar a mensagem criptografada no banco: %v", err)
	}

	// Recupera a mensagem criptografada do banco
	var retrievedEncryptedMessage string
	err = db.QueryRow("SELECT data FROM messages WHERE id = 1").Scan(&retrievedEncryptedMessage)
	if err != nil {
		t.Fatalf("Erro ao recuperar a mensagem do banco: %v", err)
	}

	// Descriptografa a mensagem e verifica o conteúdo
	decryptedMessage, err := decrypt(retrievedEncryptedMessage, key)
	if err != nil {
		t.Fatalf("Erro ao descriptografar a mensagem: %v", err)
	}

	if decryptedMessage != plaintext {
		t.Fatalf("Esperava '%s', mas obteve '%s'", plaintext, decryptedMessage)
	}

	fmt.Printf("Mensagem original recuperada com sucesso: %s\n", decryptedMessage)
}

func TestEncryptAndSaveFile(t *testing.T) {
	key := generateKey()

	// Cria um arquivo temporário para teste
	fileContent := "Este é um conteúdo de teste para criptografia e armazenamento."
	tmpFile, err := os.CreateTemp("", "testfile*.txt")
	if err != nil {
		t.Fatalf("Erro ao criar arquivo temporário: %v", err)
	}
	defer os.Remove(tmpFile.Name()) // Remove o arquivo após o teste

	_, err = tmpFile.WriteString(fileContent)
	if err != nil {
		t.Fatalf("Erro ao escrever no arquivo temporário: %v", err)
	}
	tmpFile.Close()

	// Configura o banco de dados de teste
	db, err := setupTestDatabase()
	if err != nil {
		t.Fatalf("Erro ao configurar o banco de dados: %v", err)
	}
	defer db.Close()

	// Lê o conteúdo do arquivo e criptografa
	content, err := readFileContent(tmpFile.Name())
	if err != nil {
		t.Fatalf("Erro ao ler o conteúdo do arquivo: %v", err)
	}

	encryptedContent, err := encrypt(content, key)
	if err != nil {
		t.Fatalf("Erro ao criptografar o conteúdo do arquivo: %v", err)
	}

	// Salva no banco
	if err := saveEncryptedMessage(db, tmpFile.Name(), encryptedContent); err != nil {
		t.Fatalf("Erro ao salvar o conteúdo criptografado no banco: %v", err)
	}

	// Recupera e imprime as mensagens criptografadas (apenas para verificação)
	if err := printEncryptedMessages(db); err != nil {
		t.Fatalf("Erro ao listar mensagens criptografadas: %v", err)
	}
}

func TestDecryptAndCompareFileContent(t *testing.T) {
	key := generateKey()

	// Configura o banco de dados de teste
	db, err := setupTestDatabase()
	if err != nil {
		t.Fatalf("Erro ao configurar o banco de dados: %v", err)
	}
	defer db.Close()

	// Conteúdo original
	originalContent := "Conteúdo para teste de descriptografia e comparação."
	filename := "testfile.txt"

	// Criptografa e salva no banco
	encryptedContent, err := encrypt(originalContent, key)
	if err != nil {
		t.Fatalf("Erro ao criptografar o conteúdo: %v", err)
	}

	if err := saveEncryptedMessage(db, filename, encryptedContent); err != nil {
		t.Fatalf("Erro ao salvar o conteúdo criptografado no banco: %v", err)
	}

	// Recupera do banco
	var retrievedEncryptedContent string
	err = db.QueryRow("SELECT data FROM messages WHERE filename = ?", filename).Scan(&retrievedEncryptedContent)
	if err != nil {
		t.Fatalf("Erro ao recuperar o conteúdo criptografado do banco: %v", err)
	}

	// Descriptografa e compara
	decryptedContent, err := decrypt(retrievedEncryptedContent, key)
	if err != nil {
		t.Fatalf("Erro ao descriptografar o conteúdo: %v", err)
	}

	if decryptedContent != originalContent {
		t.Fatalf("O conteúdo descriptografado é diferente do original.\nEsperado: %s\nObtido: %s", originalContent, decryptedContent)
	}
}

func TestRetrieveAndDecryptAllFiles(t *testing.T) {
	key := generateKey()

	// Configura o banco de dados de teste
	db, err := setupTestDatabase()
	if err != nil {
		t.Fatalf("Erro ao configurar o banco de dados: %v", err)
	}
	defer db.Close()

	// Dados de teste
	files := map[string]string{
		"file1.txt": "Primeiro conteúdo para teste.",
		"file2.txt": "Segundo conteúdo para armazenamento seguro.",
		"file3.txt": "Terceiro arquivo de teste com texto simples.",
	}

	// Criptografa e salva no banco
	for filename, content := range files {
		encryptedContent, err := encrypt(content, key)
		if err != nil {
			t.Fatalf("Erro ao criptografar o conteúdo do arquivo '%s': %v", filename, err)
		}
		if err := saveEncryptedMessage(db, filename, encryptedContent); err != nil {
			t.Fatalf("Erro ao salvar o arquivo '%s' no banco: %v", filename, err)
		}
	}

	// Recupera e descriptografa todos os arquivos
	rows, err := db.Query("SELECT filename, data FROM messages")
	if err != nil {
		t.Fatalf("Erro ao recuperar os arquivos do banco: %v", err)
	}
	defer rows.Close()

	for rows.Next() {
		var filename, encryptedContent string
		if err := rows.Scan(&filename, &encryptedContent); err != nil {
			t.Fatalf("Erro ao escanear os resultados: %v", err)
		}

		decryptedContent, err := decrypt(encryptedContent, key)
		if err != nil {
			t.Fatalf("Erro ao descriptografar o conteúdo do arquivo '%s': %v", filename, err)
		}

		// Verifica se o conteúdo descriptografado é igual ao original
		if decryptedContent != files[filename] {
			t.Fatalf("O conteúdo descriptografado do arquivo '%s' é diferente do original.\nEsperado: %s\nObtido: %s", filename, files[filename], decryptedContent)
		}
	}
}
