import socket
import threading
import json
from logs import log_info

# Configuración del servidor de historial
HISTORY_HOST = '127.0.0.1'  # Dirección del servidor de historial
HISTORY_PORT = 5002         # Puerto del servidor de historial
CHAT_HISTORY_FILE = 'chat_history.json'  # Archivo donde se almacenará el historial de chats

# Clase para manejar el historial
class ChatHistory:
    def __init__(self):
        # Cargar el historial existente o iniciar uno vacío
        try:
            with open(CHAT_HISTORY_FILE, 'r') as file:
                self.history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = {}

        # Bloqueo para manejar acceso concurrente
        self.lock = threading.Lock()

    def save_message(self, chat_id, user, message):
        """
        Guardar un mensaje en el historial.
        """
        with self.lock:
            if chat_id not in self.history:
                self.history[chat_id] = []

            self.history[chat_id].append({'user': user, 'message': message})

            # Guardar en archivo
            with open(CHAT_HISTORY_FILE, 'w') as file:
                json.dump(self.history, file, indent=4)

    def get_history(self, chat_id):
        """
        Obtener el historial de un chat específico.
        """
        with self.lock:
            return self.history.get(chat_id, [])

# Clase del servidor de historial
class HistoryServer(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.chat_history = ChatHistory()

    def handle_client(self, client_socket, client_address):
        """
        Manejar la comunicación con un cliente.
        """
        try:
            while True:
                # Recibir solicitud del cliente
                request = client_socket.recv(1024).decode('utf-8')
                if not request:
                    break

                data = json.loads(request)
                action = data.get('action')
                chat_id = data.get('chat_id')

                if action == 'save':
                    # Guardar un mensaje
                    user = data.get('user')
                    message = data.get('message')
                    self.chat_history.save_message(chat_id, user, message)
                    log_info(f"Mensaje guardado en chat {chat_id}: {user}: {message}")
                    client_socket.sendall(b"Message saved successfully")

                elif action == 'get':
                    # Obtener historial
                    history = self.chat_history.get_history(chat_id)
                    client_socket.sendall(json.dumps(history).encode('utf-8'))

                else:
                    client_socket.sendall(b"Invalid action")
        except Exception as e:
            log_info(f"Error manejando cliente {client_address}: {e}")
        finally:
            client_socket.close()
            log_info(f"Cliente desconectado: {client_address}")

    def run(self):
        """
        Iniciar el servidor de historial.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        print(f"Servidor de historial escuchando en {self.host}:{self.port}")
        log_info(f"Servidor de historial iniciado en {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            log_info(f"Cliente conectado: {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == '__main__':
    server = HistoryServer(HISTORY_HOST, HISTORY_PORT)
    server.start()
