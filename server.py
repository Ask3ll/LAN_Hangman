import time
import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("your local ip", 12345))
server_socket.listen(1)

print("Ожидание подключения...")
client_socket, client_address = server_socket.accept()

print(f"Подключено к {client_address}")

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
current_man = 0
word = ""
st = int(input("Введите 0 или 1 для определения кто будет загадывать. 1 - Вы, 0 - другая сторона: "))
if st:
    word = input("Введите слово: ").lower()
    response = input("Дайте подсказку: ")
    response = f"Ваша подсказка: {response}"
    client_socket.send(response.encode("utf-8"))
else:
    response = "1"
    client_socket.send(response.encode("utf-8"))
    message = client_socket.recv(1024).decode("utf-8")
    message2 = client_socket.recv(1024).decode("utf-8")
    print(f"Подсказка: {message2}")
    word = message.lower()



word_in = list(word)
guessed = []
used_leters = []
is_win = []
for i in range(len(word)):
    guessed.append(["_"])
    is_win.append("")
in_game = True
# main loop
while True:
    if word_in == is_win:
        if not st:
            print("Вы победили!")
            response = "lose"
            client_socket.send(response.encode("utf-8"))
            break
        else:
            print("Вы проиграли!")
            response = "win"
            client_socket.send(response.encode("utf-8"))
            break
    if current_man == 10:
        if st:
            print("Вы выиграли!")
            print(man[current_man])
            response = (f"l {word.capitalize()}")
            client_socket.send(response.encode("utf-8"))
            break
        else:
            print(man[current_man])
            print(f'Вы програли! Загаданное слово было - {word.capitalize()}')
            response = (f"{man[current_man]}")
            client_socket.send(response.encode("utf-8"))
            response = ("win")
            client_socket.send(response.encode("utf-8"))
            break






    print(man[current_man])

    nrml = []
    for i in guessed:
        nrml.append(i[0])
    print(nrml)
    print(f'Использованые буквы: {used_leters}')
    response = (f"""
{man[current_man]}
{nrml}
Использованые буквы: {used_leters}
""")
    client_socket.send(response.encode("utf-8"))
    if not st:
        guess = input("Введите букву: ").lower()
        if not guess.lower() == word.lower():
            response = f"Соперник ввел букву: {guess.upper()}"
        client_socket.send(response.encode("utf-8"))
    else:
        response = "wad"
        client_socket.send(response.encode("utf-8"))
        guess = client_socket.recv(1024).decode("utf-8")
        guess = guess.lower()
        print(f"Соперник ввел букву: {guess.upper()}")
    miss = []
    for i in list(guess):
        try:
            miss.append(int(i))
        except:
            pass


    if not st:
        if guess.lower() == word.lower():
            print("Вы победили!")
            response = "lose"
            client_socket.send(response.encode("utf-8"))
            break
        elif len(miss) != 0:
            print("Вводить можно только русские буквы!")
            time.sleep(0.2)
            continue
        if len(guess) > 1:
            print("Нужно вводить 1 символ!")
            time.sleep(0.2)
            continue
        if guess in used_leters:
            print('Эту букву уже вводили!')
            time.sleep(0.2)
            continue
        if guess in word_in:
            while guess in word_in:
                pos = word_in.index(guess)
                guessed[pos] = guess
                used_leters.append(guess)
                word_in[pos] = ''  # Удаляем угаданную букву из word_in
            print(f"Буква - {guess.upper()} есть!")
            time.sleep(0.2)
        else:
            print('Такой буквы нет!')
            response = "Соперник соперник ошибся в букве!"
            client_socket.send(response.encode("utf-8"))
            current_man += 1
            used_leters.append(guess)
            time.sleep(0.2)
            continue
    else:
        if guess.lower() == word.lower():
            print("Вы проиграли!")
            response = "win"
            client_socket.send(response.encode("utf-8"))
            break
        elif len(miss) != 0:
            response = "Можно вводить только русские буквы!"
            client_socket.send(response.encode("utf-8"))
            time.sleep(0.2)
            continue
        if len(guess) > 1:
            response = "Нужно вводить 1 символ!"
            client_socket.send(response.encode("utf-8"))
            time.sleep(0.2)
            continue
        if guess in used_leters:
            response = "Эту букву уже вводили!"
            client_socket.send(response.encode("utf-8"))
            time.sleep(0.2)
            continue
        if guess in word_in:
            while guess in word_in:
                pos = word_in.index(guess)
                guessed[pos] = guess
                used_leters.append(guess)
                word_in[pos] = ''
            response = f"Буква - {guess.upper()} есть!"
            client_socket.send(response.encode("utf-8"))
            time.sleep(0.2)
        else:
            response = "'Такой буквы нет!"
            client_socket.send(response.encode("utf-8"))
            print("Соперник соперник ошибся в букве!")
            current_man += 1
            used_leters.append(guess)
            time.sleep(0.2)
            continue
