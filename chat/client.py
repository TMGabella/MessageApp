import socket
import threading

# Создаем клиентский сокет
client_socket = socket.socket()
client_socket.connect(('localhost', 12345))  # Подключаемся к серверу
send_thread: threading.Thread
receive_thread: threading.Thread
ex = False
# Функция для отправки сообщений серверу
def send_message():
    global ex
    while not ex:
        message = input()
        client_socket.send(message.encode('utf-8'))
        if (message == "/exit"):
            ex = True

# Функция для приема сообщений от сервера
def receive_message():
    global ex
    while not ex:
        try:
            message = client_socket.recv(1024).decode('utf8')
            print(f"{message}", end="")
        except:
            print("Ошибка приема сообщения")
            break

# Создаем отдельные потоки для отправки и приема сообщений
send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_message)

receive_thread.start()
send_thread.start()
