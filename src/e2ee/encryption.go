package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"database/sql"
	"encoding/base64"
	"fmt"
	"io"
	"io/ioutil"

	_ "github.com/mattn/go-sqlite3"
)

// Gera uma chave de 32 bytes (AES-256).
func generateKey() []byte {
	return []byte("aVeryStrongEncryptionKey12345678")
}

// Criptografa usando AES.
func encrypt(plaintext string, key []byte) (string, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return "", err
	}

	nonce := make([]byte, 12) // GCM requires a 12 byte nonce.
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return "", err
	}

	aesGCM, err := cipher.NewGCM(block)
	if err != nil {
		return "", err
	}

	ciphertext := aesGCM.Seal(nil, nonce, []byte(plaintext), nil)
	finalCiphertext := append(nonce, ciphertext...) // Combines nonce + ciphertext

	return base64.StdEncoding.EncodeToString(finalCiphertext), nil
}

// Desencriptografa usando AES.
func decrypt(encodedCiphertext string, key []byte) (string, error) {
	data, err := base64.StdEncoding.DecodeString(encodedCiphertext)
	if err != nil {
		return "", err
	}

	nonce := data[:12]
	ciphertext := data[12:]

	block, err := aes.NewCipher(key)
	if err != nil {
		return "", err
	}

	aesGCM, err := cipher.NewGCM(block)
	if err != nil {
		return "", err
	}

	plaintext, err := aesGCM.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		return "", err
	}

	return string(plaintext), nil
}

// Salva mensagem criptografada no banco de dados.
func saveEncryptedMessage(db *sql.DB, filename, encryptedMessage string) error {
	_, err := db.Exec("INSERT INTO messages (data, filename) VALUES (?, ?)", encryptedMessage, filename)
	return err
}

// Le conteúdo do arquivo como string.
func readFileContent(filepath string) (string, error) {
	data, err := ioutil.ReadFile(filepath)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

// Cria banco de dados SQLite e tabelas.
func createDatabase() (*sql.DB, error) {
	db, err := sql.Open("sqlite3", "./encrypted_files.db")
	if err != nil {
		return nil, err
	}

	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS messages (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		filename TEXT NOT NULL,
		data TEXT NOT NULL
	);`)
	if err != nil {
		return nil, err
	}

	return db, nil
}

// Faz um GET e printa tudo do banco.
func printEncryptedMessages(db *sql.DB) error {
	rows, err := db.Query("SELECT id, data FROM messages")
	if err != nil {
		return err
	}
	defer rows.Close()

	fmt.Println("Mensagens criptografadas armazenadas no banco:")
	for rows.Next() {
		var id int
		var data string
		if err := rows.Scan(&id, &data); err != nil {
			return err
		}
		fmt.Printf("ID: %d, Data Criptografada: %s\n", id, data)
	}
	return nil
}

// Desencriptografa e printa legal o conteúdo de um arquivo específico.
func decryptAndPrintFile(db *sql.DB, id int, key []byte) error {
	var filename, encryptedData string
	err := db.QueryRow("SELECT filename, data FROM messages WHERE id = ?", id).Scan(&filename, &encryptedData)
	if err != nil {
		return err
	}

	decryptedData, err := decrypt(encryptedData, key)
	if err != nil {
		return err
	}

	fmt.Printf("Arquivo Descriptografado [%s]:\n%s\n", filename, decryptedData)
	return nil
}
