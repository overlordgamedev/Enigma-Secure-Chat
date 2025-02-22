import socket
import threading
import string

# Функция для шифрования/расшифровки с использованием шифра Энигма
def enigma_cipher(message: str, password: str) -> str:
    # Определение роторов и их начальных позиций
    # rotors — это список, где каждый элемент представляет собой кортеж (проводка, метка переключения).
    # Проводка — это строка, в которой буквы перемешаны, показывая, как ротор заменяет буквы.
    # Метка переключения — это буква, при которой ротор переключает следующий.
    rotors = [
        ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "K"),
        ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "J"),
        ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "O"),
        ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "D")
    ]

    # Рефлекторная схема — это как зеркала для сигналов, они меняют буквы по аналогии с проводкой
    reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

    # Приводим пароль к верхнему регистру и ограничиваем его до 4 символов
    password = password.upper().ljust(4, 'A')[:4]
    # Преобразует строку в список. Было QWER, стало ['Q', 'W', 'E', 'R'].
    # Это нужно, чтобы обращаться к каждой букве отдельно.
    positions = list(password)
    # Создает копию позиций роторов. Это нужно, чтобы не менять оригинальный пароль т.к во время шифрования позиции будут меняться
    current_positions = positions.copy()
    # Пустой объект для хранения результата
    result = []

    # Цикл означает что будет браться по одному символу из сообщения для зашифровки
    for original_char in message:
        # Пропускаем не-буквы (Все знаки кроме букв не шифруются)
        if not original_char.isalpha():
            result.append(original_char)
            continue

        # Если символ в верхнем регистре true, если в нижнем false
        is_upper = original_char.isupper()
        # Перевод буквы в верхний регистр
        char = original_char.upper()

        # Логика вращения роторов
        rotate_next = True  # Флаг для переключения следующего ротора
        for i in range(len(current_positions)):
            if rotate_next:
                # Поворачиваем ротор на одну позицию (Берется текущая позиция ротора и к ней добавляется + 1)
                new_pos = (string.ascii_uppercase.index(current_positions[i]) + 1) % 26
                # Обновляем позицию ротора в current_positions
                current_positions[i] = string.ascii_uppercase[new_pos]
                # Проверяем, нужно ли переключить следующий ротор
                # Если текущая позиция ротора совпадает с меткой переключения (notch),
                # то флаг rotate_next будет установлен в True, и следующий ротор будет сдвигаться.
                rotate_next = current_positions[i] == rotors[i][1]
            else:
                break

        processed = char
        # Проходим по всем роторам (от первого к последнему).
        for i in range(len(rotors)):
            wiring = rotors[i][0]  # Проводка ротора
            pos = current_positions[i]  # Его позиция
            # Определяем, на сколько ротор сдвинут относительно алфавита.
            offset = string.ascii_uppercase.index(pos)
            # Проход символа через ротор
            processed = wiring[(string.ascii_uppercase.index(processed) + offset) % 26]

        # Проход через рефлектор
        processed = reflector[string.ascii_uppercase.index(processed)]

        # Обратный проход через роторы
        for i in reversed(range(len(rotors))):
            wiring = rotors[i][0]  # Проводка ротора
            pos = current_positions[i]  # Его позиция
            # Определяем, на сколько ротор сдвинут относительно алфавита.
            offset = string.ascii_uppercase.index(pos)
            # Проход символа через ротор
            processed = string.ascii_uppercase[(wiring.index(processed) - offset) % 26]

        # Восстанавливаем регистр
        # Если is_upper == True, то тогда буква остается в верхнем регистре, если false, то тогда переводится в нижний регистр
        result.append(processed if is_upper else processed.lower())

    return ''.join(result)

# Функция для получения сообщений от другого клиента
def receive_messages(sock, password):
    while True:
        try:
            # Получаем данные от клиента
            data = sock.recv(1024).decode('utf-8')
            # Расшифровываем сообщение
            decrypted = enigma_cipher(data, password)
            print(f"\n[Другой] Зашифрованное: {data}")
            print(f"[Другой] Расшифрованное: {decrypted}")
            print("> ", end="", flush=True)  # Для сохранения возможности ввода
        except (ConnectionResetError, KeyboardInterrupt):
            print("\nСоединение закрыто")
            break

# Функция для отправки сообщений серверу
def send_messages(sock, password):
    while True:
        try:
            print("> ", end="", flush=True)
            message = input()
            # Шифруем сообщение
            encrypted = enigma_cipher(message, password)
            print(f"\n[Вы] Оригинал: {message}")
            print(f"[Вы] Зашифрованное: {encrypted}")
            sock.send(encrypted.encode('utf-8'))  # Отправляем сообщение
        except (ConnectionResetError, KeyboardInterrupt):
            print("\nСоединение закрыто")
            break

# Основная функция
def main():
    # Адрес сервера куда отправлять сообщения
    HOST = 'localhost'
    PORT = 12345
    password = input("Введите пароль для шифрования (мин. 4 символа): ").strip()

    # Проверяем длину пароля
    while len(password) < 4:
        print("Пароль должен содержать только 4 буквы")
        password = input("Введите пароль для шифрования: ").strip()

    # Создаем сокет клиента
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Подключаемся к серверу
        client_socket.connect((HOST, PORT))
        print("Подключено к серверу!")
    except ConnectionRefusedError:
        print("Сервер недоступен!")
        return

    # Создаем поток для получения сообщений
    receiver = threading.Thread(target=receive_messages, args=(client_socket, password))
    receiver.start()

    try:
        # Отправляем сообщения
        send_messages(client_socket, password)
    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()

# Запуск основной функции
if __name__ == "__main__":
    main()
