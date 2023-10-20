import socket
import threading

# Создаем серверный сокет
server_socket = socket.socket()
server_socket.bind(('localhost', 12345))  # Привязываем сокет к адресу и порту
server_socket.listen(5)  # Разрешаем до 5 клиентов подключаться


# Список клиентских соксов и их адресов
class Client:
    def __init__(self, name: str, cl: socket):
        self.name: str = name
        self.cl: socket = cl


clients = []
addresses = []
msgs = []


# Функция для отправки сообщений всем клиентам
def broadcast(message):
    for client in clients:
        client.cl.send(message)


# Функция для обработки клиентских запросов
def handle_client(client: Client):
    while True:
        try:
            message = client.cl.recv(1024)
            print(message)
            msgs.append(f"{client.name}: {message.decode('utf-8')}\n")
            if message.decode('utf-8') == "/exit":
                index = clients.index(client)
                clients.remove(client)
                client.cl.close()
                address = addresses.pop(index)
                print(f"Пользователь {address} отключен")
            if message:
                print(f"{addresses[clients.index(client)]}: {msgs[-1]}", end="")
                broadcast(msgs[-1].encode())
            else:
                index = clients.index(client)
                clients.remove(client)
                client.cl.close()
                address = addresses.pop(index)
                print(f"Пользователь {address} отключен")
        except:
            continue


# Основной цикл сервера
while True:
    print("Ожидание подключения клиента...")
    client_socket, client_address = server_socket.accept()
    print(f"Подключен клиент: {client_address}")
    client_socket.send("Добро пожаловать в чат!\nname: ".encode(), )
    try:
        client_name = client_socket.recv(1024)
        print(f"Имя клиента: {client_name} ({client_address})")
    except:
        exit(1)
    addresses.append(client_address)
    clients.append(Client(client_name.decode('utf-8'), client_socket))
    for i in msgs:
        client_socket.send(i.encode())
    # Создаем отдельный поток для обработки клиента
    client_handler = threading.Thread(target=handle_client, args=(clients[-1],))
    client_handler.start()
