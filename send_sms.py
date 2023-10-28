from twilio.rest import Client

# Suas credenciais da conta Twilio
account_sid = 'AC66f1fb323118a95ea728e03646c27fdd'
auth_token = 'c9b2a156cb57bdec4b7de5c1b2fb6c03'

# Criar uma instância do cliente Twilio
client = Client(account_sid, auth_token)

# Número de telefone de destino
to_phone_number = '+5516994502671'  # Substitua pelo número de telefone de destino

# Número de telefone Twilio que você adquiriu
from_phone_number = '+19544510656' 




for i in  range(20):

    # Mensagem que você deseja enviar
    message = client.messages.create(
        to=to_phone_number,
        from_=from_phone_number,
        body='Oi Shu tudo Bem? aprendi a enivar sms automatico ontem'
    )

print(f'Mensagem enviada com o SID: {message.sid}')
