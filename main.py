import win32serviceutil
import win32service
import win32event
from datetime import datetime, time
from Configuracion import enviarWSP, registraLog
from Carga import Carga


class MiServicio(win32serviceutil.ServiceFramework):
    _svc_name_ = "MiServicioWindows2"
    _svc_display_name_ = "MiServicioWindows2"
    _svc_description_ = "Este servicio ejecuta tareas programadas relacionadas con licitaciones, cotizaciones y adjudicaciones."

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.ultima_ejecucion_diaria = None
        self.ultima_ejecucion_hora = None
        self.ultima_ejecucion_parcial = None
        self.ultimo_log_ejecucion = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            registraLog("MiServicioWindows Ejecutándose.")
            carga = Carga()

            while True:
                ahora = datetime.now()

                if self.en_horario_laboral(ahora):
                    # Evento diario
                    if self.ultima_ejecucion_diaria is None or self.ultima_ejecucion_diaria.date() < ahora.date():
                        try:
                            carga.Diaria(ahora)
                            self.ultima_ejecucion_diaria = ahora
                        except Exception as e:
                            registraLog(f"Error en tarea Diaria: {e}")

                    # Evento cada 1 hora
                    #if self.ultima_ejecucion_hora is None or \
                    #        (ahora - self.ultima_ejecucion_hora).total_seconds() >= 3600:
                    #    try:
                    #        carga.Cada_una_hora(ahora)
                    #        self.ultima_ejecucion_hora = ahora
                    #    except Exception as e:
                    #        registraLog(f"Error en tarea Cada_una_hora: {e}")

                    # Evento parcial
                    horas_objetivo = [time(8, 45), time(15, 30), time(17, 30), time(19, 30)]
                    hora_actual = ahora.replace(second=0, microsecond=0)
                    for hora in horas_objetivo:
                        if hora_actual.time().hour == hora.hour and hora_actual.time().minute == hora.minute:
                            if not self.ultima_ejecucion_parcial or \
                                    self.ultima_ejecucion_parcial.replace(second=0, microsecond=0) != hora_actual:
                                try:
                                    carga.Periodica(ahora)
                                    self.ultima_ejecucion_parcial = ahora
                                except Exception as e:
                                    registraLog(f"Error en tarea Periodica: {e}")

                # Esperar hasta 60 segundos verificando si se debe detener
                for _ in range(60):
                    if win32event.WaitForSingleObject(self.stop_event, 1000) == win32event.WAIT_OBJECT_0:
                        registraLog("Servicio detenido correctamente.")
                        return

                # Registrar log de "ejecutándose" cada 10 minutos
                if self.ultimo_log_ejecucion is None or \
                        (datetime.now() - self.ultimo_log_ejecucion).total_seconds() >= 600:
                    registraLog("Servicio ejecutándose...")
                    self.ultimo_log_ejecucion = datetime.now()
                enviarWSP("Servicio ejecutado")
        except Exception as e:
            registraLog(f"Error en SvcDoRun: {e}")
            raise

    def en_horario_laboral(self, ahora):
        return ahora.weekday() < 5 and time(9, 0) <= ahora.time() <= time(20, 0)


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MiServicio)
