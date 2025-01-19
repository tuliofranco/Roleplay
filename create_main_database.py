import os
import pandas as pd
import sqlite3
import shutil  # Para duplicar o banco de dados

# Caminhos para os arquivos
csv_file_path = './main_database.csv'
db_file_path = './main_database.db'
backup_dir = './backup/'
backup_db_file_path = os.path.join(backup_dir, 'main_database_backup.db')

# Função para criar o banco de dados a partir do CSV
def create_database_from_csv(csv_path, db_path):
    try:
        # Lendo o arquivo CSV
        data = pd.read_csv(csv_path)
        
        # Verificando e removendo a coluna "Unnamed: 0", se existir
        if "Unnamed: 0" in data.columns:
            data.drop(columns=["Unnamed: 0"], inplace=True)
            print("Coluna 'Unnamed: 0' detectada e removida do CSV.")

        print("Base de dados CSV carregada com sucesso!")
        
        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Criando a tabela no banco de dados
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS main_database (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Word TEXT NOT NULL,
            Translation TEXT,
            Part_of_Speech TEXT
        )
        ''')

        # Inserindo os dados do DataFrame no banco
        data.to_sql('main_database', conn, if_exists='replace', index=False)
        print(f"Banco de dados criado e dados inseridos em '{db_path}' com sucesso!")
        
        # Fechando a conexão com o banco de dados
        conn.close()
    except FileNotFoundError:
        print(f"Erro: O arquivo {csv_path} não foi encontrado.")
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")

# Função para duplicar o banco de dados
def duplicate_database(src_path, dest_path):
    try:
        # Cria o diretório de backup, se não existir
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        # Duplica o arquivo do banco de dados
        shutil.copy(src_path, dest_path)
        print(f"Banco de dados duplicado com sucesso em '{dest_path}'")
    except Exception as e:
        print(f"Erro ao duplicar o banco de dados: {e}")

# Executando as funções
create_database_from_csv(csv_file_path, db_file_path)  # Cria o banco no diretório principal
duplicate_database(db_file_path, backup_db_file_path)  # Duplica o banco no diretório de backup
