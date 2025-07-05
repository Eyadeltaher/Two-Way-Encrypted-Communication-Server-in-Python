## Two-Way Encrypted Communication Server in Python

A complete implementation of a two-way encrypted communication system using Python, including both server and client components.

This system ensures secure messaging between multiple clients using:

  - Symmetric encryption (AES) via the Fernet module from the cryptography library.
  - Secure password hashing using bcrypt for authentication.

Built to support multiple concurrent users using Python's threading and designed with data privacy and integrity in mind.

---

## Class Diagram

![image](https://github.com/user-attachments/assets/3b8990c9-6a6b-4bf0-b976-7e14f172bad2)

---

## Key Python Concepts Used

| Concept                        | Description                                                                                                                                     |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **File I/O**                   | Used to store and retrieve user credentials (`open()`, `read()`, `write()` in `AuthManager`).                                                   |
| **Sockets**                    | Enables communication between server and clients over TCP (`socket.socket`, `bind()`, `listen()`, `accept()`, `connect()`, `send()`, `recv()`). |
| **Threading**                  | Each connected client runs in a separate thread to allow multiple simultaneous connections (`threading.Thread`).                                |
| **Symmetric Encryption (AES)** | Messages are encrypted using the `cryptography.fernet` module (Fernet = AES + HMAC).                                                            |
| **Password Hashing**           | Secure password storage using `bcrypt.gensalt()` and `bcrypt.hashpw()`.                                                                         |
| **Input Validation**           | Ensures usernames and passwords are valid before processing (e.g., minimum length, special character checks).                                   |
| **Exception Handling**         | Gracefully manages unexpected errors (e.g., disconnections, malformed messages).                                                                |
| **Thread-Safe Data Access**    | Uses `threading.Lock()` to prevent race conditions when accessing shared resources like `clients` dictionary.                                   |



---

## Workflow

![image](https://github.com/user-attachments/assets/77061192-eaa9-4b1d-88aa-c28e58e652aa)

---

### How to Use

**✅ Requirements**

- Python 3.6+
- cryptography for encryption
- bcrypt for password hashing

**Install required packages:**
```
pip install cryptography bcrypt
```

**Running the Server**

- Navigate to the project directory:
```
cd path/to/project
```

**Start the server:**
```
    python Server.py
```

**Running the Client** 

 - Run the client from a different terminal or machine:
```
    python Client.py
```

**Follow the prompts:**

- Choose between SIGNUP or LOGIN
- Enter a valid username (no space, : or newline)
- Enter a strong password (minimum 8 characters, 1 digit, 1 uppercase)
- Once authenticated, start chatting securely!
- Type messages and press Enter
- Type exit to leave the chat

---

**🌐 Remote Access (To allow clients from a different network to connect)**

- Run the server on a machine with a public IP
- Make sure port 5555 is open (configure router or firewall if needed)
- Use the server’s public IP in Client.py

---

## Notes

- Messages are limited to 1024 bytes; larger messages might be truncated or cause unexpected behavior.
- This implementation is intended for educational/demo purposes and may need enhancements (e.g., proper TCP framing, error handling, scalability) for production use.
- Communication assumes a trusted network for key distribution; in real-world scenarios, use secure key exchange protocols.

---

## Extensibility Ideas

- Implement a secure key exchange mechanism (e.g., Diffie-Hellman) for per-client encryption keys.
- Add message history and offline message delivery.
- Support private messages or chat rooms.
- Implement TLS or use ssl module for secure transport.
- Add GUI client for better usability.
- Enhance error handling and logging.

---

## Feel free to open issues or submit pull requests for improvements!
