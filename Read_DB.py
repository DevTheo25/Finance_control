import pandas as pd
import sqlite3





# # Conectar ao banco de dados
# connection = sqlite3.connect('finanças.db')
# cursor = connection.cursor()

# import random
# # Suas listas de dados
# lista_nome = ["Eletrônicos", "Seguro", "Gás", "Lazer", "Farmácia", "saúde", "Presentes", "Impostos", "Alimentação", "médicas", "Academia", "Cinema", "Livros", "revista", "Café", "Hobbies", "Cafeteria", "Ingressos", "Eletricista", "Viagem", "Taxa", "Manutenção do carro", "Clube de campo", "Crianças", "Roupas", "Salão de beleza", "Escola", "Aluguel de equipamento esportivo", "Doações", "Gastos com animais de estimação", "Assinatura de streaming", "Telefone fixo", "Cinema em casa", "Jardim", "Assinatura de música", "Conserto da casa", "Cuidados com o carro", "Cinema em casa", "Jantares fora", "Assinatura de software", "Assinatura de jornal", "Compras online", "Investimento", "Presentes de aniversário", "Cartão de crédito", "Aulas particulares", "Assinatura de academia", "Coeletrônicos"]

# lista_data = ["18 {}, 2023 07:31".format(random.choice(["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"])) for _ in range(50)]

# lista_preço = ["200,00", "80,00", "30,00", "50,00", "40,00", "150,00", "70,00", "100,00", "120,00", "180,00", "60,00", "35,00", "25,00", "10,00", "5,00", "15,00", "75,00", "20,00", "40,00", "50,00", "350,00", "25,00", "90,00", "200,00", "80,00", "120,00", "45,00", "55,00", "250,00", "30,00", "40,00", "35,00", "25,00", "20,00", "40,00", "55,00", "60,00", "50,00", "45,00", "40,00", "30,00", "50,00", "70,00", "90,00", "80,00", "150,00", "200,00", "35,00", "60,00", "70,00"]

# lista_pago = [0] * 50

# lista_mes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"] * 4


# # Inserir dados no banco de dados
# for i in range(len(lista_nome)):
#     nome = lista_nome[i]
#     data = lista_data[i]
#     preço = lista_preço[i]
#     pago = lista_pago[i]
#     mes = lista_mes[i]

#     cursor.execute("INSERT INTO tasks (Task, Date, Gasto, Pago, Mes) VALUES (?, ?, ?, ?, ?)", (nome, data, preço, pago, mes))

# connection.commit()
# connection.close()




# Conectar ao banco de dados
connection = sqlite3.connect('finanças.db')
cursor = connection.cursor()


# Ler os dados atualizados
query = "SELECT * FROM tasks"
df = pd.read_sql_query(query, connection)

# Fechar a conexão
connection.close()

# Exibir os dados
print(df)
