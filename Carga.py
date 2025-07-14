import requests
from datetime import datetime
from Configuracion import URL_Licitaciones, URL_CotizacionesCM, URL_Adjudicaciones,URL_OrdenesdeCompra,enviarWSP, registraLog

class Carga:

    def Licitaciones(self):
        try:
            response = requests.get(URL_Licitaciones, timeout=10)
            hora_actual = datetime.now().time()
            if response.status_code == 200:
                registraLog("Licitaciones cargadas a las: " + str(hora_actual))
                enviarWSP("Licitaciones cargadas a las: " + str(hora_actual))
            else:
                registraLog(f"Error en carga Licitaciones: {response.status_code}")
                enviarWSP("Error " + response.text + " al cargar Licitaciones a las: " + str(hora_actual))
        except Exception as e:
            registraLog(f"Error al consultar el servicio de Licitaciones: {e}")

    def CotizacionesCM(self):
        try:
            response = requests.get(URL_CotizacionesCM, timeout=10)
            hora_actual = datetime.now().time()
            if response.status_code == 200:
                registraLog("Cotizaciones CM cargadas a las: " + str(hora_actual))
                enviarWSP("Cotizaciones CM cargadas a las: " + str(hora_actual))
            else:
                registraLog(f"Error en carga CotizacionesCM: {response.status_code}")
                # enviarWSP("Error " + response.text + " al cargar CotizacionesCM a las: " + str(hora_actual))
        except Exception as e:
            registraLog(f"Error al consultar el servicio de CotizacionesCM: {e}")

    def OrdenesdeCompra(self):
        try:
            response = requests.get(URL_OrdenesdeCompra, timeout=10)
            hora_actual = datetime.now().time()
            if response.status_code == 200:
                registraLog("Órdenes de compra cargadas a las: " + str(hora_actual))
                enviarWSP("Órdenes de compras: " + str(hora_actual))
            else:
                registraLog(f"Error en carga Órdenes de compra: {response.status_code}")
                enviarWSP("Error " + response.text + " al cargar Órdenes de compra a las: " + str(hora_actual))
        except Exception as e:
            registraLog(f"Error al consultar el servicio de Órdenes de compra: {e}")

    def Adjudicaciones(self):
        try:
            response = requests.get(URL_Adjudicaciones, timeout=10)
            response.raise_for_status()
            data = response.json()

            adjudicaciones = data.get("Adjudicaciones", [])

            for item in adjudicaciones:
                tipo = item.get("Tipo", "")
                codigo = item.get("Codigo", "")
                estado= item.get("Estado", 0)
                mensaje = item.get("Mensaje", "")   
                
                if (estado ==1): # hay adjudicación
                    enviarWSP(mensaje)
                else:
                    registraLog("no hay adjudicación para el código: " + codigo)
        
        except Exception as e:
            registraLog(f"Error valida: {str(e)}")

    def Inicial(self):
        self.Licitaciones()
        self.CotizacionesCM()
        self.OrdenesdeCompra()
    #______________________________________________________

    def Diaria(self, ahora):
        registraLog("Ejecutando carga diaria: " + str(ahora.strftime('%H:%M:%S')))
        enviarWSP("Carga Diaria de Oportunidades de Negocio")
        self.Inicial()

    def Cada_una_hora(self, ahora):
        try:
            registraLog("Ejecución cada 1 hora: " + str(ahora.strftime('%H:%M:%S')))
            enviarWSP("Carga cada 1 hora: CotizacionesCM")
            
            # Aquí puedes añadir tareas periódicas adicionales si lo deseas
        except Exception as e:
            registraLog("Error en ejecución cada 1 hora: " + str(e))

    def Periodica(self, ahora):
        try:
            registraLog("Ejecución 3 veces al día: " + str(ahora.strftime('%H:%M:%S')))
            enviarWSP("Carga 3 veces al dia: Adjudicaciones, CotizacionesCM,Licitaciones")
            self.Adjudicaciones()
            self.CotizacionesCM()
            self.Licitaciones()
            # Aquí puedes añadir tareas periódicas adicionales si lo deseas
        except Exception as e:
            registraLog("Error en ejecución 3 veces al día: " + str(e))
            