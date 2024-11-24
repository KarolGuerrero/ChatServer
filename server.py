import threading
import socket
import argparse
import os
import json
from logs import log_info

# Configuración del microservicio de historial
HISTORY_HOST = '127.0.0.1'
HISTORY_PORT = 5002

# Configuración del microservicio de notificaciones
NOTIFICATIONS_HOST = '127.0.0.1'
NOTIFICATIONS_PORT = 5001

class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port
        self.history_socket = self.connect_to_history_service()
        self.notification_socket = self.connect_to_notifications_service()

    def connect_to_history_service(self):
        """
        Establece conexión con el microservicio de historial.
        """
        try:
            history_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            history_socket.connect((HISTORY_HOST, HISTORY_PORT))
            print("Conectado al microservicio de historial")
            return history_socket
        except Exception as e:
            print(f"Error al conectar con el microservicio de historial: {e}")
            return None

    def connect_to_notifications_service(self):
        """
        Establece conexión con el microservicio de notificaciones.
        """
        try:
            notification_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            notification_socket.connect((NOTIFICATIONS_HOST, NOTIFICATIONS_PORT))
            print("Conectado al microservicio de notificaciones")
            return notification_socket
        except Exception as e:
            print(f"Error al conectar con el microservicio de notificaciones: {e}")
            return None

    def send_to_history(self, chat_id, user, message):
        """
        Enviar mensaje al microservicio de historial para su almacenamiento.
        """
        if self.history_socket:
            try:
                request = {
                    "action": "save",
                    "chat_id": chat_id,
                    "user": user,
                    "message": message
                }
                self.history_socket.sendall(json.dumps(request).encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar mensaje al microservicio de historial: {e}")

    def send_notification(self, event_type, user, message=None):
        """
        Enviar notificación al microservicio de notificaciones.
        """
        if self.notification_socket:
            try:
                formatted_message = f"{event_type}|{user}|{message if message else ''}"
                self.notification_socket.sendall(formatted_message.encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar notificación: {e}")

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(1)
        print("Escuchando en", sock.getsockname())

        while True:
            sc, sockname = sock.accept()
            log_info(f"Cliente conectado desde {sc.getpeername()}")
            print(f"Aceptando una nueva conexión desde {sc.getpeername()} a {sc.getsockname()}")

            server_socket = ServerSocket(sc, sockname, self)
            server_socket.start()
            self.connections.append(server_socket)

    def broadcast(self, message, source):
        for connection in self.connections:
            # Enviar a todos los clientes conectados excepto el origen
            if connection.sockname != source:
                connection.send(message)

    def remove_connection(self, connection):
        # Enviar notificación de desconexión
        self.send_notification(event_type="disconnect", user=str(connection.sockname[0]))
        self.connections.remove(connection)

class ServerSocket(threading.Thread):
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server

    def run(self):
        while True:
            try:
                message = self.sc.recv(1024).decode('utf-8')
                if not message:
                    break

                # Procesar mensaje y enviarlo al historial
                print(f"{self.sockname} dice: {message}")
                self.server.send_to_history(chat_id="general", user=str(self.sockname[0]), message=message)

                # Reenviar mensaje a otros clientes
                self.server.broadcast(message, self.sockname)

            except Exception as e:
                print(f"Error con cliente {self.sockname}: {e}")
                break

        # Desconectar cliente
        self.sc.close()
        self.server.remove_connection(self)

    def send(self, message):
        """
        Enviar mensaje a este cliente.
        """
        self.sc.sendall(message.encode('utf-8'))

def exit_handler(server):
    """
    Manejo de cierre del servidor desde la consola.
    """
    while True:
        ipt = input("")
        if ipt == "q":
            print("Cerrando todas las conexiones...")
            for connection in server.connections:
                connection.sc.close()
            print("Apagando el servidor...")
            os._exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port(default 1060)')

    args = parser.parse_args()

    # Crear y iniciar el hilo del servidor
    server = Server(args.host, args.p)
    server.start()

    # Hilo para manejar el cierre del servidor
    exit_thread = threading.Thread(target=exit_handler, args=(server,))
    exit_thread.start()
