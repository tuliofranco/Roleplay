import sqlite3

# Configura o banco de dados
def create_db():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()

    # Cria a tabela para palavras
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        translation TEXT,
        part_of_speech TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Recupera as palavras do dia
def get_words(limit=20):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM words LIMIT ?', (limit,))
    words = cursor.fetchall()
    conn.close()
    return words

# Insere palavras no banco
def insert_words(words):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO words (word, translation, part_of_speech) VALUES (?, ?, ?)', words)
    conn.commit()
    conn.close()
