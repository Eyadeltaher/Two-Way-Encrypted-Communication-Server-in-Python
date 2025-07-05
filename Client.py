import socket
from cryptography.fernet import Fernet
import threading


def get_valid_username():
    while True:
        username = input("Enter your username: ").strip()
        if any(char in username for char in [" ", "\n", ":"]):
            print("Invalid username. No spaces or colons allowed")
        else:
            return username

def get_valid_password():
    while True:
        password = input("Enter your password (min 8 chars, at least one digit and uppercase): ")
        if len(password) < 8:
            print("Password too short. Must be at least 8 characters.")
            continue
        if not any(c.isdigit() for c in password):
            print("Password must contain at least one digit.")
            continue
        if not any(c.isupper() for c in password):
            print("Password must contain at least one uppercase letter.")
            continue
        return password
    
def receive_messages(sock, cipher):
    try:
        while True:
            encrypted = sock.recv(1024)
            if not encrypted:
                print("Server closed connection.")
                break
            message = cipher.decrypt(encrypted).decode()
            print("\n" + message)
    except Exception as e:
        print(f"Error receiving messages: {e}")
    finally:
        sock.close()
        

def main():
    host='0.0.0.0'
    port=5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    encryption_key = client_socket.recv(1024)
    cipher = Fernet(encryption_key)

    while True:
        op = input("Enter operation (SIGNUP or LOGIN): ").strip().upper()
        if op not in ["SIGNUP", "LOGIN"]:
            print("Invalid operation, try again.")
            continue
        username = get_valid_username()
        password = get_valid_password()

        credentials = f"{op}\n{username}\n{password}\n"
        client_socket.sendall(credentials.encode())

        response = client_socket.recv(1024).decode() 
        if response == "SIGNUP_SUCCESS":
            print("Sign up successful!")
        elif response == "SIGNUP_FAILED":
            print("Sign up failed. Username already exists.")
            continue

        if response == "LOGIN_SUCCESS":
            print("Login successful!")
        elif response == "LOGIN_FAILED":
            print("Login failed. Invalid username or password.")
            continue

        break

    threading.Thread(target=receive_messages, args=(client_socket, cipher), daemon=True).start()     #daemon=True ensures thread closes when main program exits.
    print("You can start chatting. Type 'exit' to quit.")
    try:
        while True:
            msg = input()
            if msg.lower() == 'exit':
                print("Disconnecting...")
                break
            full_msg = f"{username}: {msg}"
            encrypted_msg = cipher.encrypt(full_msg.encode())
            client_socket.sendall(encrypted_msg)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
