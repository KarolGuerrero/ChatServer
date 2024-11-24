### **README: Guía para Ejecutar la Aplicación de Chat Distribuido**

---

#### **Descripción General**
Esta aplicación implementa un sistema de chat distribuido utilizando microservicios para manejar notificaciones y el historial de mensajes. Incluye las siguientes partes:

1. **Servidor Principal (`server.py`)**  
   Gestiona las conexiones de los clientes y coordina la comunicación entre ellos.
   
2. **Microservicio de Notificaciones (`notifications_server.py`)**  
   Muestra notificaciones emergentes cuando ocurren eventos (como la conexión o desconexión de un cliente).
   
3. **Microservicio de Historial de Chats (`history_server.py`)**  
   Guarda y registra los mensajes en un archivo JSON.

4. **Cliente (`client.py`)**  
   Permite a los usuarios conectarse al servidor, enviar y recibir mensajes en tiempo real.

---

#### **Requisitos Previos**
1. **Python 3.x instalado**.  
   Verifica que tienes Python instalado con:  
   ```bash
   python3 --version
   ```
   
2. **Librerías necesarias** (instalarlas si no están):  
   ```bash
    pip install tkinter

   ```

3. **Estructura del Proyecto**  
   Asegúrate de tener los siguientes archivos en el directorio principal del proyecto:
   ```
   server.py
   notifications_server.py
   history_server.py
   client.py
   logs.py
   notifications.db
   chat_history.json (opcional; el archivo se creará automáticamente si no existe)
   ```

---

#### **Pasos para Ejecutar la Aplicación**

##### **1. Ejecutar el Microservicio de Notificaciones**
En una terminal, ejecuta el archivo `notifications_service.py` para iniciar el microservicio de notificaciones:
```bash
python3 notifications_server.py
```
Esto iniciará el microservicio en `127.0.0.1:5001` (puerto por defecto).

---

##### **2. Ejecutar el Microservicio de Historial**
En una nueva terminal, ejecuta el archivo `history_server.py` para iniciar el microservicio de historial:
```bash
python3 history_server.py
```
Este servicio estará escuchando en `127.0.0.1:5002` y almacenará los mensajes en `chat_history.json`.

---

##### **3. Ejecutar el Servidor Principal**
En otra terminal, inicia el servidor principal:
```bash
python3 server.py 127.0.0.1 -p 1060
```
Esto iniciará el servidor en la dirección `127.0.0.1` y el puerto `1060`.

---

##### **4. Ejecutar los Clientes**
Abre tantas terminales como clientes quieras conectar al servidor y ejecuta `client.py` con el siguiente comando:
```bash
python3 client.py 127.0.0.1
```

Cada cliente se conectará al servidor principal, y podrán comenzar a enviar y recibir mensajes en tiempo real.

---

#### **Flujo de Ejecución**
1. Cuando un cliente se conecta, el servidor envía una notificación al microservicio de notificaciones.
2. Los mensajes enviados por los clientes se retransmiten a todos los demás clientes conectados.
3. Los mensajes también se guardan en el archivo `chat_history.json` mediante el microservicio de historial.

---

#### **Archivos y Funcionalidades**
1. **`server.py`**  
   - Coordina la comunicación entre los clientes.  
   - Conecta con los microservicios de notificaciones e historial.  

2. **`notifications_server.py`**  
   - Muestra notificaciones emergentes en el sistema operativo.

3. **`history_server.py`**  
   - Registra los mensajes enviados por los clientes en `chat_history.json`.

4. **`client.py`**  
   - Permite a los usuarios interactuar con el servidor, enviar mensajes y recibirlos.

5. **`logs.py`**  
   - Maneja el registro de eventos (como nuevas conexiones y mensajes).

---

#### **Cómo Ver el Historial de Chats**
1. Después de la ejecución, abre el archivo `chat_history.json` para consultar los mensajes almacenados.
2. El archivo se actualizará dinámicamente con cada nuevo mensaje enviado.

---

#### **Cierre de la Aplicación**
- Para cerrar el servidor, escribe `q` en la terminal donde se ejecuta `server.py`. Esto cerrará todas las conexiones activas y detendrá el servidor.  
- Detén los microservicios (`notifications_server.py` y `history_server.py`) presionando `Ctrl+C`.

