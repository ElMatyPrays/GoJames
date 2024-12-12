import mysql.connector
import pymysql
from tkinter import Tk, Frame, Label, Entry, Button, messagebox

class Reserva:
    def __init__(self):
        pass

    def validar_y_guardar_reserva(self, RUT_cliente, nombre_destino, fecha):

        destinos = [
            "Madrid",
            "Barcelona",
            "Roma",
            "Paris",
            "Milan",
            "Berlin",
            "Londres",
        ]

        while True:
            # Validar que el cliente y el destino existan en la base de datos antes de guardar la reserva
            try:
                conexion = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='',
                    db='prueba4'
                )
                cursor = conexion.cursor()

                # Validar si el cliente existe
                consulta_cliente = "SELECT COUNT(*) FROM cliente WHERE RUT = %s"
                cursor.execute(consulta_cliente, (RUT_cliente,))
                cliente_existe = cursor.fetchone()[0]

                if not cliente_existe:
                    messagebox.showerror("Error", f"El cliente con RUT '{RUT_cliente}' no existe.")
                    break

                # Validar si el destino existe
                consulta_destino = "SELECT ID_destino FROM destino WHERE nombre = %s"
                cursor.execute(consulta_destino, (nombre_destino,))
                destino = cursor.fetchone()

                if not destino:
                    messagebox.showerror("Error", f"El destino con nombre '{nombre_destino}' no existe.")
                    messagebox.showinfo("Destinos disponibles", f"Los destinos disponibles son {destinos}")
                    return

                # Extraer el ID_destino desde el resultado de la consulta
                ID_destino = destino[0]

                # Guardar la reserva
                consulta_reserva = """
                    INSERT INTO reserva_viajes (RUT_cliente, ID_destino, fecha, nombre_destino, estado)
                    VALUES (%s, %s, %s, %s, 1)
                """
                cursor.execute(consulta_reserva, (RUT_cliente, ID_destino, fecha, nombre_destino))
                conexion.commit()

                messagebox.showinfo("Reserva Creada", f"Reserva creada exitosamente para:\n"
                                                     f"RUT: {RUT_cliente}\n"
                                                     f"Destino: {nombre_destino}\n"
                                                     f"Fecha: {fecha}")
                break

                conexion.close()

            except pymysql.Error as e:
                messagebox.showerror("Error", f"Error al guardar la reserva: {e}")




    def Crear_reserva_paquete(self, RUT_cliente, ID_paquete):

        # Conexión a la base de datos
        try:
            self.conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba2'
            )
            self.prueba = self.conexion.cursor()
            print("Conexión a la base de datos correcta")
        except Exception as e:
            print(f"Error de conexión a la base de datos: {e}")
            return

        # Consulta SQL
        cursor = "INSERT INTO reserva (RUT_cliente, ID_paquete) VALUES ('{}', {})".format(
            RUT_cliente, ID_paquete
            )
