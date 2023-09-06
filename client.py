import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("server ip", 12345)  #
man = [
'''
''',
'''
|
|
|
|
|
|
|
|
''',
'''
|-----------------
|
|
|
|
|
|
|
''',
'''
|----------------|
|                |           
|                |
|                |
|                |
|                |
|                |
|                |
''',
'''
|----------------|
|        |       |           
|                |
|                |
|                |
|                |
|                |
|                |
''',
'''
|----------------|
|        |       |           
|        0       |
|                |
|                |
|                |
|                |
|                |
''',
'''
|----------------|
|        |       |           
|        0       |
|        |       |
|        |       |
|                |
|                |
|                |
''',
'''
|----------------|
|        |       |           
|        0       |
|        |       |
|        |       |
|       /        |
|                |
|                |
''',
'''
|----------------|
|        |       |           
|        0       |
|        |       |
|        |       |
|       / \      |
|                |
|                |
''',
'''
|----------------|
|        |       |           
|        0       |
|        |\      |
|        |       |
|       / \      |
|                |
|                |
''',
'''
|----------------|
|        |       |           
|        0       |
|       /|\      |
|        |       |
|       / \      |
|                |
|                |
''']
client_socket.connect(server_address)
print("Подключено!")
while True:
    response = client_socket.recv(1024).decode("utf-8")
    if response == "1":
        message = input("Выберите слово: ")
        client_socket.send(message.encode("utf-8"))
        message2 = input("Дайте подсказку:  ")
        client_socket.send(message2.encode("utf-8"))
        response = "lose"
    elif response == "lose":
        print("Вы проиграли!")
        break
    elif response == "win":
        print("Вы выиграли!")
        break
    elif response == "lose_ten":
        print(
f"""
|----------------|
|        |       |           
|        0       |
|       /|\      |
|        |       |
|       / \      |
|                |
|                |
Вы проиграли!
""")
        break
    elif response == "win_ten":
        print(
            f"""
    |----------------|
    |        |       |           
    |        0       |
    |       /|\      |
    |        |       |
    |       / \      |
    |                |
    |                |
    Вы победили!
    """)
        break

    elif response[:1] == "l":
        print(man[10])
        print(f"Вы проиграли! Загадоное слово: {response[2:]}")
        break
    elif response == "wad":
        message = input("Введите букву: ")
        client_socket.send(message.encode("utf-8"))
    else:
        print(response)

client_socket.close()


