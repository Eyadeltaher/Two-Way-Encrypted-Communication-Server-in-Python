import threading
import socket
from AuthManager import AuthManager
from cryptography.fernet import Fernet                 #for the symmetric encryption (AES) 

class Server:

    def __init__(self, host = '0.0.0.0', port =5555):
        self.host = host
        self.port = int(port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        #socket.AF_INET: Uses IPv4 addressing
        self.clients = {}                                                             #socket.SOCK_STREAM: Specifies TCP protocol
        self.auth = AuthManager("users.txt")
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.lock = threading.Lock()

    def start(self):                         #Start the server and listen for connections
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            client_socket.sendall(self.encryption_key)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            data = b""
            while data.count(b'\n') < 3:
                data += client_socket.recv(1024)

            lines = data.decode().split("\n")
            op = lines[0].strip()
            username = lines[1].strip()
            password = lines[2].strip()

            if op == "SIGNUP":
                success = self.auth.sign_up(username, password)
                client_socket.send(b"SIGNUP_SUCCESS" if success else b"SIGNUP_FAILED")
                if not success:
                    client_socket.close()
                    return

            elif op == "LOGIN":
                success = self.auth.log_in(username, password)
                client_socket.send(b"LOGIN_SUCCESS" if success else b"LOGIN_FAILED")
                if not success:
                    client_socket.close()
                    return
            else:
                client_socket.send(b"INVALID_OPERATION")
                client_socket.close()
                return
            
            with self.lock:
                self.clients[client_socket] = username
            self.broadcast(f"{username} joined the chat!", sender_socket=None)    #sender_socket=None means the message is sent to all clients.

            while True:
                encrypted = client_socket.recv(1024)
                if not encrypted:
                    break
                message = self.cipher.decrypt(encrypted).decode()
                self.broadcast(f"{message}", client_socket)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.remove_client(client_socket)
            self.broadcast(f"{username} left the chat.", sender_socket=None)
            client_socket.close()        

    def broadcast(self, message, sender_socket):
        encrypted_message = self.cipher.encrypt(message.encode())
        with self.lock:
            for client_socket in list(self.clients):
                if client_socket != sender_socket:
                    try:
                        client_socket.send(encrypted_message)
                    except:
                        self.remove_client(client_socket)
            
    def remove_client(self, client_socket):
        with self.lock:
            if client_socket in self.clients:
                deleted_client = self.clients.pop(client_socket)
                print(f"{deleted_client} disconnected")

if __name__ == "__main__":
    server = Server()
    server.start()


