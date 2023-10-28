import pandas as pd
import sqlite3



# Conectar ao banco de dados
connection = sqlite3.connect('card_data.db')
cursor = connection.cursor()


# # Ler os dados atualizados
# query = "SELECT * FROM cards"
# df = pd.read_sql_query(query, connection)
# # Exibir os dados
# print(df)


query_delete = "DELETE FROM cards WHERE DataValid = '32/32'"
cursor.execute(query_delete)
connection.commit()

# Fechar a conexão
connection.close()

