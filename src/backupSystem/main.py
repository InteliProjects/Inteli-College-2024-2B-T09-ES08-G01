from src.backup_manager import perform_backup

if __name__ == "__main__":
    print("Iniciando backup incremental e redundante...")
    perform_backup()
    print("Backup concluído com sucesso!")
