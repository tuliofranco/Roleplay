from adapters.database import create_db, insert_words

# Cria o banco de dados
create_db()

# Adiciona palavras iniciais
words = [
    ('run', 'correr', 'verb'),
    ('book', 'livro', 'noun'),
    ('happy', 'feliz', 'adjective'),
]
insert_words(words)
