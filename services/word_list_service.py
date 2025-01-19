import sqlite3
from datetime import datetime
from adapters.maritaca_adapter import MaritacaAdapter
from adapters.openai_adapter import OpenAIAdapter
import logging

datetime.now()
class WordListService:
    def __init__(self):
        """
        Inicializa o serviço com o caminho do banco de dados e a data de início.
        :param db_path: Caminho do banco de dados.
        :param start_date: Data de início no formato 'YYYY-MM-DD'.
        """
        self.db_path = './main_database.db'
        self.db_backup_path = './backup/main_database_backup.db'
        self.start_date = datetime.strptime('2025-01-17', '%Y-%m-%d').date()

    def calculate_study_day(self):
        """
        Calcula o dia de estudo com base na data de início.
        :return: Número inteiro representando o dia de estudo.
        """
        today = datetime.now().date()
        return (today - self.start_date).days + 1

    def add_words_for_today(self, num_words):
        """
        Adiciona palavras ao banco de dados learning_words para o dia atual.
        :param num_words: Número de palavras a adicionar.
        """
        day = self.calculate_study_day()

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Selecionar as próximas palavras da tabela main_database
            cursor.execute('''
            SELECT Word, Translation, Part_of_Speech 
            FROM main_database
            WHERE Word NOT IN (SELECT Word FROM learning_words)
            LIMIT ?
            ''', (num_words,))
            words = cursor.fetchall()

            if not words:
                return f"Nenhuma palavra disponível para adicionar no dia {day}."

            # Prepara as palavras com o dia atual
            words_with_day = [(word[0], word[1], word[2], 0, 0, day) for word in words]

            # Query para inserir as palavras na tabela learning_words
            query = '''
            INSERT INTO learning_words (Word, Translation, Part_of_Speech, frequency, err_qty, day)
            VALUES (?, ?, ?, ?, ?, ?)
            '''

            # Executa a query nos dois bancos
            for word in words_with_day:
                self.execute_on_both_databases(query, word)

            return f"{len(words_with_day)} palavras adicionadas para o dia {day}."
        except Exception as e:
            return f"Erro ao adicionar palavras: {e}"


    def get_learning_words(self):
        """
        Retorna as palavras aprendidas para um dia específico.
        :param day: Dia de estudo a ser filtrado.
        :return: Lista de palavras aprendidas para o dia informado.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            day = self.calculate_study_day()

            # Selecionar todas as palavras da tabela learning_words
            cursor.execute('SELECT * FROM learning_words WHERE day = ? or frequency = 0  ORDER BY day, id', (day,) )
            words = cursor.fetchall()

            conn.close()
            return words
        except Exception as e:
            return f"Erro ao recuperar palavras para o dia {day}: {e}"
        
    def verify_phrase(self, word, sentence, tense, selected_ai):
        """
        Verifica se a frase está correta usando a IA.
        :param word: Palavra escolhida.
        :param sentence: Frase criada pelo usuário.
        :param tense: Tempo verbal escolhido.
        :return: Resposta da IA.
        """
        if selected_ai == "OpenAI":
            llm = OpenAIAdapter()
        elif selected_ai == "MaritacaAI":
            llm = MaritacaAdapter()
        else:
            raise ValueError("Adaptador de IA inválido. Escolha 'OpenAI' ou 'MaritacaAI'.")
        
        try:
            prompt = (
                f"Verifique se a frase está correta para a palavra '{word}' no tempo verbal '{tense}'.\n"
                f"Frase: {sentence}\n"
                "Se estiver correta, responda 'A frase está correta.'. Caso contrário, sugira melhorias."
            )

            response = llm.generate_response(prompt=prompt)
            
            return response
        except Exception as e:
            logging.error(f"Erro ao obter feedback da IA: {e}")
            return "Ocorreu um erro ao gerar o feedback. Por favor, tente novamente."
        
        
    def update_learning_word_feedback(self, word, feedback_type):
        """
        Atualiza o feedback na tabela learning_words.
        :param word: Palavra a ser atualizada.
        :param feedback_type: Tipo de feedback ("Correct" ou "Wrong").
        """
        try:
            if feedback_type :
                query = '''
                UPDATE learning_words
                SET corr_qty = corr_qty + 1
                WHERE Word = ?
                '''
            elif not feedback_type :
                query = '''
                UPDATE learning_words
                SET err_qty = err_qty + 1
                WHERE Word = ?
                '''
            else:
                raise ValueError("Tipo de feedback inválido. Use 'Correct' ou 'Wrong'.")

            # Executa a query nos dois bancos
            self.execute_on_both_databases(query, (word,))

            print(f"Feedback '{feedback_type}' atualizado para a palavra '{word}'.")
        except Exception as e:
            print(f"Erro ao atualizar feedback para a palavra '{word}': {e}")


    def execute_on_both_databases(self, query, params=()):
        """
        Executa uma query SQL nos bancos de dados principal e de backup.
        :param query: A query SQL a ser executada.
        :param params: Parâmetros para a query.
        """
        try:
            # Conecta ao banco principal
            conn_main = sqlite3.connect(self.db_path)
            cursor_main = conn_main.cursor()

            # Conecta ao banco de backup
            conn_backup = sqlite3.connect(self.db_backup_path)
            cursor_backup = conn_backup.cursor()

            # Executa a query em ambos os bancos
            cursor_main.execute(query, params)
            cursor_backup.execute(query, params)

            # Commit nas alterações
            conn_main.commit()
            conn_backup.commit()

            # Fecha as conexões
            conn_main.close()
            conn_backup.close()

        except Exception as e:
            print(f"Erro ao executar a query em ambos os bancos: {e}")