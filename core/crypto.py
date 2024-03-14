import os

from cryptography.fernet import Fernet


# Генерируем случайный ключ
def generate_key():
    key = Fernet.generate_key()
    file_path = "secret.key"

    if not os.path.exists(file_path):
        with open(file_path, "wb") as key_file:
            key_file.write(key)


# Загружаем ключ из файла
def load_key():
    return open("secret.key", "rb").read()


# Шифрование строки
def encrypt_message(message, key):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message


# Дешифрование строки
def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message
