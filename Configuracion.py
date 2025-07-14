from twilio.rest import Client
import os
import time
from dotenv import load_dotenv

# Cargar las variables del archivo .env
dotenv_path = r"C:\Desarrollo\Servicio\.env"
load_dotenv(dotenv_path=dotenv_path)

URL_Licitaciones = "http://127.0.0.1:8000/api/licitaciones"
URL_CotizacionesCM = "http://127.0.0.1:8000/api/cotizacionescm"
URL_Adjudicaciones = "http://127.0.0.1:8000/api/adjudicaciones"
URL_OrdenesdeCompra = "http://127.0.0.1:8000/api/ordenesdecompra"

account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
twilio_number = os.getenv('twilio_number')
destinatarios = os.getenv('destinatarios', '').split(',')

cliente = Client(account_sid, auth_token)


def enviarWSP(mensaje: str):
    try:
        for destinatario in destinatarios:
            destinatario = destinatario.strip()
            mensaje_enviado = cliente.messages.create(
                from_=twilio_number,
                to=destinatario,
                body=mensaje
            )
            registraLog(f"Mensaje enviado a {destinatario} con SID: {mensaje_enviado.sid}")
    except Exception as e:
        registraLog(f"Error WSP: {e}")


def registraLog(mensaje):
    try:
        with open("C:\\DESARROLLO\\Servicio\\MiServicioWindows.log", "a") as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {mensaje}\n")
    except Exception as e:
        print(f"Error al escribir en el log: {e}")
