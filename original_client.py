import socket
import threading
from encrypt import gener_keys_get_message, encrypt_message, decrypt_message

class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())

        # create key pairs
        # (implemented in the write handler)

        # exchange public keys
        # (receive them)

        # receive the encrypted (and) secret key
        while True:
            input_handler = threading.Thread(target=self.write_handler,args=())
            input_handler.start()
            message_handler = threading.Thread(target=self.read_handler,args=())
            message_handler.start()
            

    def read_handler(self): 
        while True:
            # message = self.s.recv(1024).decode()

            # decrypt message with the secrete key
            received = self.s.recv(1024).decode().split(' ')
            msg, edited, e, n, d, receiver, username = received[0], int(received[1]), int(received[2]),\
                int(received[3]), int(received[4]), received[5], received[6]
            print(f'...a private message received from {username}')
            read_msg = decrypt_message(msg, d, n, edited)


            print('the message:   ', read_msg)

    def write_handler(self):
        while True:
            message = input()

            # encrypt message with the secrete key
            print('...generating the keys for the client')
            message, edited, e, n, d = gener_keys_get_message(message)
            
            receiver = input('enter the name of the receiver or press Enter to send it to all users on the server:')
            receiver = 'all_users' if receiver == '' else receiver
            message = encrypt_message(message, e, n)
            print(f'{self.username} is sending the encrypted message to the server...')
            fin_str = message+' '+str(edited)+' '+str(e)+' '+str(n)+' '+str(d)+' '+receiver+' '+str(self.username)
            self.s.send(fin_str.encode())
            print(f'{self.username} successfully sent the message!')

if __name__ == "__main__":
    try:
        cl = Client("127.010.0.0", 9003, "the_client")
        cl.init_connection()
    finally:
        # cl.s.close()
        pass
