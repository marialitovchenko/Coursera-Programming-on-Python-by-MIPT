#!/usr/bin/env python
# реализация сервера для тестирования метода get по заданию - Клиент для отправки метрик

# -*- coding: utf-8 -*-

import socket

sock = socket.socket()
sock.bind(('127.0.0.1', 8888))
sock.listen(1)
conn, addr = sock.accept()

print('Соединение установлено:', addr)

# переменная response хранит строку возвращаемую сервером, если вам для
# тестирования клиента необходим другой ответ, измените ее
response = b'ok\npalm.cpu 2.0 1150864247\npalm.cpu 200 1150864246\npalm.cpu 3.0 1150864248\n\n'

while True:
    data = conn.recv(1024)
    if not data:
        break
    request = data.decode('utf-8')
    print(f'Получен запрос: {ascii(request)}')
    print(f'Отправлен ответ {ascii(response.decode("utf-8"))}')
    conn.send(response)

conn.close()