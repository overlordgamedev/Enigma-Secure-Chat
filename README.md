# Enigma-Secure-Chat

Данный проект предназначен для обмена сообщениями по сокетам с использованием самописной системы шифрования на основе Энигма. Сделано **OverlordGameDev** специально для форума **XSS.IS**.

---

## Описание проекта

Проект представляет собой защищенный чат, состоящий из двух частей:
1. **Серверная часть** — обеспечивает соединение между клиентами и пересылку сообщений.
2. **Клиентская часть** — позволяет пользователям подключаться к серверу, отправлять и получать зашифрованные сообщения.

Чат поддерживает одновременное подключение двух клиентов. Все сообщения шифруются с использованием алгоритма, вдохновленного шифровальной машиной **Энигма**.

---

## Как это работает

1. **Шифрование**:  
   Каждое сообщение шифруется на стороне отправителя с использованием пароля, который должен быть одинаковым у обоих клиентов.  
   Шифрование основано на роторной системе, аналогичной той, что использовалась в машине Энигма.

2. **Обмен сообщениями**:  
   Сервер пересылает зашифрованные сообщения между клиентами.  
   Получатель расшифровывает сообщение с помощью того же пароля.

3. **Подключение**:  
   Сервер ожидает подключения двух клиентов. После успешного подключения клиенты могут обмениваться сообщениями.
