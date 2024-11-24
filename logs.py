import logging
import os

# Configurar el archivo de log
LOG_FILE = "server_logs.log"

# Crear directorio "logs" si no existe
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename=os.path.join("logs", LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_info(message):
    """
    Registra un mensaje informativo.
    """
    logging.info(message)

def log_warning(message):
    """
    Registra un mensaje de advertencia.
    """
    logging.warning(message)

def log_error(message):
    """
    Registra un mensaje de error.
    """
    logging.error(message)

def log_critical(message):
    """
    Registra un mensaje crítico.
    """
    logging.critical(message)
