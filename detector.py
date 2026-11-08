from datetime import datetime
import os


def registrar_respuesta(usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("respuesta.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha},USUARIO_BLOQUEADO,{usuario}\n")

    return fecha


if not os.path.exists("eventos.log"):
    print("Sin eventos para analizar (eventos.log no existe).")
else:
    intentos = {}

    with open("eventos.log", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            fecha, tipo, usuario = linea.split(",")
            if tipo == "LOGIN_FALLIDO":
                if usuario not in intentos:
                    intentos[usuario] = []
                intentos[usuario].append(fecha)

    if not intentos or not any(len(r) >= 3 for r in intentos.values()):
        print("Sin alertas: ningun usuario alcanza 3 intentos fallidos.")
    else:
        for usuario, registros in intentos.items():
            if len(registros) >= 3:
                print("ALERTA DE SEGURIDAD")
                print("Usuario:", usuario)
                print("Intentos fallidos:", len(registros))
                print("Primer intento:", registros[0])
                print("Detección:", registros[2])

                # Orden corregido (Anexo B obs. 1): primero registrar
                # respuesta, luego calcular metricas. La guia original
                # calculaba MTTR/MTTD antes de definir fecha_respuesta
                # (NameError).
                fecha_respuesta = registrar_respuesta(usuario)

                print("Acción aplicada: bloqueo de usuario")
                print("Respuesta:", fecha_respuesta)

                inicio = datetime.strptime(registros[0], "%Y-%m-%d %H:%M:%S")
                deteccion = datetime.strptime(registros[2], "%Y-%m-%d %H:%M:%S")
                respuesta = datetime.strptime(fecha_respuesta, "%Y-%m-%d %H:%M:%S")

                mttr = (respuesta - deteccion).total_seconds()
                print("MTTR:", mttr, "segundos")

                mttd = (deteccion - inicio).total_seconds()
                print("MTTD:", mttd, "segundos")
