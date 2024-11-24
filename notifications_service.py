import socket
import threading
import tkinter as tk
from tkinter import messagebox

class NotificationService:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_server(self):
        """
        Inicia el servidor para recibir notificaciones.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Microservicio de notificaciones escuchando en {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Conexión establecida con {client_address}")
            
            # Crear un hilo para manejar la conexión del cliente
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        """
        Maneja las notificaciones recibidas del servidor principal.
        """
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                # Procesar y mostrar la notificación
                self.process_notification(data)
        except ConnectionResetError:
            print("Conexión cerrada por el servidor principal")
        finally:
            client_socket.close()

    def process_notification(self, notification):
        """
        Procesa la notificación recibida y muestra una ventana emergente.
        """
        # Parsear la notificación (formato: event_type|user|message)
        try:
            event_type, user, message = notification.split('|', 2)
        except ValueError:
            print(f"Formato de notificación inválido: {notification}")
            return

        # Crear y mostrar la ventana emergente en el hilo principal de Tkinter
        threading.Thread(target=self.show_popup, args=(event_type, user, message)).start()

    def show_popup(self, event_type, user, message):
        """
        Muestra una ventana emergente con la notificación.
        """
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter

        if event_type == "connect":
            messagebox.showinfo("Notificación", f"Nuevo cliente conectado: {user}")
        elif event_type == "message":
            messagebox.showinfo("Mensaje", f"{user} dice: {message}")
        elif event_type == "disconnect":
            messagebox.showwarning("Notificación", f"Cliente desconectado: {user}")
        else:
            messagebox.showerror("Error", f"Evento desconocido: {event_type}")

        root.destroy()  # Cerrar la ventana emergente después de mostrarla


if __name__ == '__main__':
    HOST = '127.0.0.1'  # Dirección IP del microservicio
    PORT = 5001         # Puerto del microservicio

    notification_service = NotificationService(HOST, PORT)
    notification_service.start_server()
