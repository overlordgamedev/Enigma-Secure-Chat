import socket
import threading

# Функция обработки данных от клиента и отправки этих данных другому клиенту
def handle_client(client, other_socket):
    while True:
        try:
            # Получение данных от клиента
            # Метод для получения данных от конкретного клиента. Цифры означают размер ожидаемых данных
            data = client.recv(1024)
            # Если данных нет, значит клиент отключился
            if not data:
                break
            # Отправка полученных данных другому клиенту
            other_socket.send(data)
        except (ConnectionResetError, BrokenPipeError):
            # Если соединение было сброшено или соединение разорвано
            break
    # Закрытие сокета клиента
    client.close()

def main():
    # Создаем сокет для сервера
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Привязываем сокет к адресу и порту сервера
    server.bind((HOST, PORT))
    # Слушаем подключения. Можно только для двух пользователей
    server.listen(2)
    print("Сервер запущен. Ожидание двух подключений")

    # Список для хранения подключенных клиентов
    clients = []

    # Ожидаем подключения двух клиентов
    while len(clients) < 2:
        # Когда клиент подключается, он добавляется в переменную client а в addr добавляется его адрес
        client, addr = server.accept()
        print(f"Клиент подключен")
        clients.append(client)  # Добавление клиента из переменной в список clients

    # Назначение переменных каждому клиенту из списка clients
    client1, client2 = clients
    print("Оба клиента подключены")  # Сообщение, когда оба клиента подключены

    # Запуск двух потоков, для каждого клиента по потоку
    threading.Thread(target=handle_client, args=(client1, client2)).start()
    threading.Thread(target=handle_client, args=(client2, client1)).start()

# Запуск основной функции
if __name__ == "__main__":
    # Адрес и порт сервера
    HOST = 'localhost'
    PORT = 12345
    main()  # Запуск основной функции
