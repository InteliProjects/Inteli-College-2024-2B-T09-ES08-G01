package main

import (
	"io/ioutil"
	"log"
	"os"
)

func main() {
	key := generateKey()

	// Cria o banco de dados SQLite
	db, err := createDatabase()
	if err != nil {
		log.Fatalf("Erro ao criar o banco de dados: %v", err)
	}
	defer db.Close()

	// Mock: Crie arquivos de exemplo
	filenames := []string{"example.txt", "example.md", "example.pdf"}
	fileContents := []string{
		"Este é o conteúdo do arquivo TXT.",
		"Este é um arquivo Markdown com **texto formatado**.",
		"Simulação de conteúdo PDF.",
	}

	for i, filename := range filenames {
		err := ioutil.WriteFile(filename, []byte(fileContents[i]), 0644)
		if err != nil {
			log.Fatalf("Erro ao criar o arquivo '%s': %v", filename, err)
		}
	}

	// Processa os arquivos
	for _, filename := range filenames {
		content, err := readFileContent(filename)
		if err != nil {
			log.Fatalf("Erro ao ler o arquivo '%s': %v", filename, err)
		}

		encryptedContent, err := encrypt(content, key)
		if err != nil {
			log.Fatalf("Erro ao criptografar o arquivo '%s': %v", filename, err)
		}

		if err := saveEncryptedMessage(db, filename, encryptedContent); err != nil {
			log.Fatalf("Erro ao salvar o arquivo criptografado '%s': %v", filename, err)
		}
	}

	// Lista todos os arquivos criptografados
	if err := printEncryptedMessages(db); err != nil {
		log.Fatalf("Erro ao listar os arquivos criptografados: %v", err)
	}

	// Descriptografa e exibe um arquivo específico
	if err := decryptAndPrintFile(db, 1, key); err != nil {
		log.Fatalf("Erro ao descriptografar o arquivo: %v", err)
	}

	// Remove os arquivos criados (limpeza)
	for _, filename := range filenames {
		if err := os.Remove(filename); err != nil {
			log.Printf("Erro ao remover o arquivo '%s': %v", filename, err)
		}
	}
}
