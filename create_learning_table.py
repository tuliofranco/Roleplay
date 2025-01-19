

import sqlite3

# Caminho do banco de dados de backup
db_file_path = './backup/main_database_backup.db'
main_db_file_path = './main_database.db'

# Função para criar a tabela learning_words
def create_learning_table(db_path):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Criar a tabela learning_words
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Word TEXT NOT NULL,
            Translation TEXT,
            Part_of_Speech TEXT,
            frequency INTEGER DEFAULT 0,
            coor_qty INTEGER DEFAULT 0,
            err_qty INTEGER DEFAULT 0,
            day INTEGER DEFAULT 0
        )
        ''')
        conn.commit()
        print("Tabela 'learning_words' criada com sucesso!")
        
        # Fechar a conexão
        conn.close()
    except Exception as e:
        print(f"Erro ao criar a tabela 'learning_words': {e}")

# Executar a função para criar a tabela
create_learning_table(main_db_file_path)  
create_learning_table(db_file_path)