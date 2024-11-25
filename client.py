import threading
import socket
import os
import sys
import tkinter as tk
from tkinter import font 
import argparse

class Send(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        while True:
            print('{}: '.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]
            if message == "QUIT":
                self.sock.sendall('Server: {} ha dejado el chat'.format(self.name).encode('ascii'))
                break
            else:
                self.sock.sendall('{}: {} '.format(self.name, message).encode('ascii'))

        print('\nQuitting...')
        self.sock.close()
        os.exit(0)

class Receive(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    def run(self):
        while True:
            message = self.sock.recv(1024).decode('ascii')
            if message:
                if self.messages:
                    self.messages.insert(tk.END, message)
                    print('\r{}\n{}: '.format(message, self.name, end=''))
                else:
                    print('\r{}\n{}: '.format(message, self.name, end=''))
            else:
                print('\nNo se ha perdido la conexión con el servidor!')
                print('\nQuitting...')
                self.sock.close()
                os.exit(0)

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None

    def start(self):
        print('Conectando a {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('Conexión exitosa a {}:{}'.format(self.host, self.port))

        print()
        self.name = input('Tu nombre: ')
        print()
        print('Bienvenido, {}! Preparado para enviar y recibir mensajes...'.format(self.name))

        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        send.start()
        receive.start()

        self.sock.sendall('Server: {} ha entrado al chat'.format(self.name).encode('ascii'))
        print("\rListo! Deja el ChatRoom en cualquier momento escribiendo 'QUIT'\n")
        print('{}: '.format(self.name), end='')

        return receive
    
    def send(self, textInput):
        message = textInput.get()
        textInput.delete(0, tk.END)
        self.messages.insert(tk.END, '{}: {}'.format(self.name, message))

        if message == "QUIT":
            self.sock.sendall('Server: {} ha dejado el chat'.format(self.name).encode('ascii'))
            print('\nQuitting...')
            self.sock.close()
            os.exit(0)
        else:
            self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))


def main(host, port):
    # Configuración del cliente (no cambió)
    client = Client(host, port)
    receive = client.start()

    # Ventana principal
    window = tk.Tk()
    window.title("ChatRoom")
    window.configure(bg="#eae6d9")  # Fondo tipo WhatsApp

    # Fuente estilizada
    custom_font = font.Font(family="Segoe UI", size=14)

    # Encabezado
    header = tk.Label(
        master=window,
        text="ChatRoom",
        font=(custom_font, 16, "bold"),
        bg="#128C7E",  # Verde WhatsApp
        fg="white",
        pady=10,
    )
    header.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # Contenedor de mensajes
    frameMessages = tk.Frame(master=window, bg="#eae6d9")
    scrollBar = tk.Scrollbar(master=frameMessages)
    messages = tk.Listbox(
        master=frameMessages,
        yscrollcommand=scrollBar.set,
        bg="#ffffff",
        fg="#000000",
        font=custom_font,
        selectbackground="#25D366",  # Color verde al seleccionar
        selectforeground="white",
        borderwidth=0,
        relief="flat",
    )
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
    messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    frameMessages.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Asociar mensajes al cliente
    client.messages = messages
    receive.messages = messages

    # Entrada de texto
    frameEntry = tk.Frame(master=window, bg="#eae6d9")
    textInput = tk.Entry(
        master=frameEntry,
        font=custom_font,
        bg="#ffffff",
        fg="#000000",
        relief="solid",
        borderwidth=1,
    )
    textInput.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    textInput.bind("<Return>", lambda x: client.send(textInput))
    frameEntry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    # Botón de enviar
    btnSend = tk.Button(
        master=window,
        text="Enviar",
        command=lambda: client.send(textInput),
        bg="#128C7E",
        fg="white",
        font=custom_font,
        relief="flat",
    )
    btnSend.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    # Configuración de la cuadrícula
    window.rowconfigure(1, minsize=500, weight=1)  # Espacio para mensajes
    window.rowconfigure(2, minsize=50, weight=0)  # Entrada de texto
    window.columnconfigure(0, minsize=500, weight=1)  # Entrada de texto
    window.columnconfigure(1, minsize=100, weight=0)  # Botón de enviar

    window.mainloop()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chatroom Client")
    parser.add_argument('host', help='Interfaz al que el cliente se conecta')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='Puerto TCP (por defecto 1060)')
    args = parser.parse_args()

    main(args.host, args.p)