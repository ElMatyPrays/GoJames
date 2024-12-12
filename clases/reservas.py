import mysql.connector
import pymysql
import re
import datetime
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
            # Conectarse a la base de datos
            try:
                conexion = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='',
                    db='prueba4'
                )
                cursor = conexion.cursor()
                bd = conexion.cursor()

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

                # Obtener el ID_reserva generado
                ID_reserva = cursor.lastrowid


                messagebox.showinfo("Reserva Creada", f"Reserva creada exitosamente para:\n"
                                                     f"RUT: {RUT_cliente}\n"
                                                     f"Destino: {nombre_destino}\n"
                                                     f"Fecha: {fecha}\n"
                                                     f"ID_RESERVA: {ID_reserva}")
                break

                conexion.close()

            except pymysql.Error as e:
                messagebox.showerror("Error", f"Error al guardar la reserva: {e}")



    ## PARTE DE MODIFICACIÓN DEL DESTINO ##

    def validar_fecha(self, fecha):
        # Validar que la fecha esté en el formato dd-mm-yyyy
        try:
            datetime.datetime.strptime(fecha, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    def validar_destino(self, destino):
        if not destino:
            messagebox.showwarning("Campo Vacío", "El campo de destino no puede estar vacío.")
            return False
        return True

    def modificar_destino_reserva(self, ID_reserva, nuevo_nombre_destino, nueva_fecha, ventana):
        if not ID_reserva:
            messagebox.showwarning("Campo Vacío", "El campo de ID reserva no puede estar vacío.")
            return

        if not self.validar_destino(nuevo_nombre_destino):
            return

        if not self.validar_fecha(nueva_fecha):
            messagebox.showwarning("Formato Incorrecto", "El formato de la fecha debe ser DD-MM-YYYY.")
            return

        try:
            # Conectarse a la base de datos
            conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba4'
            )
            cursor = conexion.cursor()

            # Validar si la reserva existe
            consulta_reserva = "SELECT COUNT(*) FROM reserva_viajes WHERE ID_reserva = %s"
            cursor.execute(consulta_reserva, (ID_reserva,))
            reserva_existe = cursor.fetchone()[0]

            if not reserva_existe:
                messagebox.showerror("Error", f"La reserva con ID '{ID_reserva}' no existe.")
                return

            # Validar si el nuevo destino existe
            consulta_destino = "SELECT ID_destino FROM destino WHERE nombre = %s"
            cursor.execute(consulta_destino, (nuevo_nombre_destino,))
            resultado = cursor.fetchone()

            if not resultado:
                messagebox.showerror("Error", f"El destino '{nuevo_nombre_destino}' no existe.")
                return

            nuevo_ID_destino = resultado[0]

            # Actualizar la reserva con el nuevo destino y/o nueva fecha
            consulta_actualizar = """
                UPDATE reserva_viajes
                SET ID_destino = %s, nombre_destino = %s, fecha = %s
                WHERE ID_reserva = %s
            """
            cursor.execute(consulta_actualizar, (nuevo_ID_destino, nuevo_nombre_destino, nueva_fecha, ID_reserva))
            conexion.commit()

            messagebox.showinfo("Reserva Actualizada", f"La reserva con ID '{ID_reserva}' ha sido actualizada:\n"
                                                       f"- Nuevo Destino: '{nuevo_nombre_destino}'\n"
                                                       f"- Nueva Fecha: '{nueva_fecha}'.")

            ventana.destroy()  # Cerrar la ventana después de la modificación
            conexion.close()

        except pymysql.Error as e:
            messagebox.showerror("Error", f"Error al modificar la reserva: {e}")


    def eliminar_reserva(self, ID_reserva, ventana):
        if not ID_reserva:
            messagebox.showwarning("Campo Vacío", "El campo de ID reserva no puede estar vacío.")
            return

        try:
            # Conectarse a la base de datos
            conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba4'
            )
            cursor = conexion.cursor()

            # Validar si la reserva existe
            consulta_reserva = "SELECT COUNT(*) FROM reserva_viajes WHERE ID_reserva = %s"
            cursor.execute(consulta_reserva, (ID_reserva,))
            reserva_existe = cursor.fetchone()[0]

            if not reserva_existe:
                messagebox.showerror("Error", f"La reserva con ID '{ID_reserva}' no existe.")
                return

            # Eliminar la reserva
            consulta_eliminar = "DELETE FROM reserva_viajes WHERE ID_reserva = %s"
            cursor.execute(consulta_eliminar, (ID_reserva,))
            conexion.commit()

            messagebox.showinfo("Reserva Eliminada", f"La reserva con ID '{ID_reserva}' ha sido eliminada.")

            ventana.destroy()  # Cerrar la ventana después de la eliminación
            conexion.close()

        except pymysql.Error as e:
            messagebox.showerror("Error", f"Error al eliminar la reserva: {e}")


    ## PARTE DE PAQUETE TURISTICO
    def validar_y_guardar_reserva_paquete(self, RUT_cliente, ID_paquete):
        # Validar que el cliente y el paquete turístico existan en la base de datos antes de guardar la reserva
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
                return

            # Validar si el paquete existe
            consulta_paquete = "SELECT COUNT(*) FROM paquete_turistico WHERE ID_paquete = %s"
            cursor.execute(consulta_paquete, (ID_paquete,))
            paquete_existe = cursor.fetchone()[0]

            if not paquete_existe:
                messagebox.showerror("Error", f"El paquete turístico con ID '{ID_paquete}' no existe.")
                return

            # Obtener los detalles del paquete turístico
            consulta_detalles_paquete = """
                 SELECT ID_lista_destinos, fecha_ida, fecha_vuelta, descripcion, actividades_disponibles, precio_total, disponibilidad 
                 FROM paquete_turistico WHERE ID_paquete = %s
             """
            cursor.execute(consulta_detalles_paquete, (ID_paquete,))
            detalles_paquete = cursor.fetchone()

            # Insertar la reserva de paquete turístico
            consulta_reserva = """
                 INSERT INTO reserva_paquete_turistico (RUT_cliente, ID_paquete, ID_lista_destinos, fecha_ida, fecha_vuelta, descripcion, 
                                                        actividades_disponibles, precio_total, disponibilidad)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
             """
            cursor.execute(consulta_reserva, (
                RUT_cliente,
                ID_paquete,
                detalles_paquete[0],
                detalles_paquete[1],
                detalles_paquete[2],
                detalles_paquete[3],
                detalles_paquete[4],
                detalles_paquete[5],
                detalles_paquete[6]
            ))
            conexion.commit()

            # Obtener el ID_reserva recién generado
            ID_reserva = cursor.lastrowid

            # Mostrar mensaje de éxito con el ID_reserva
            messagebox.showinfo("Reserva Creada", f"Reserva de paquete turístico creada exitosamente:\n"
                                                  f"ID Reserva: {ID_reserva}\n"
                                                  f"RUT: {RUT_cliente}\n"
                                                  f"Paquete ID: {ID_paquete}\n"
                                                  f"Fecha Ida: {detalles_paquete[1]}\n"
                                                  f"Fecha Vuelta: {detalles_paquete[2]}\n"
                                                  f"Descripción: {detalles_paquete[3]}\n"
                                                  f"Precio Total: {detalles_paquete[5]}")

            conexion.close()


        except pymysql.Error as e:
            messagebox.showerror("Error", f"Error al guardar la reserva de paquete turístico: {e}")

    def modificar_paquete_turistico(self, ID_paquete, nueva_fecha_ida, nueva_fecha_vuelta, nueva_descripcion,
                                    nuevas_actividades, nuevo_precio):
        try:
            conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba4'
            )
            cursor = conexion.cursor()

            # Validar si el paquete turístico existe
            consulta_paquete = "SELECT COUNT(*) FROM paquete_turistico WHERE ID_paquete = %s"
            cursor.execute(consulta_paquete, (ID_paquete,))
            paquete_existe = cursor.fetchone()[0]

            if not paquete_existe:
                messagebox.showerror("Error", f"El paquete turístico con ID '{ID_paquete}' no existe.")
                return

            # Actualizar los datos del paquete turístico
            consulta_actualizar = """
                UPDATE paquete_turistico
                SET fecha_ida = %s, fecha_vuelta = %s, descripcion = %s,
                    actividades_disponibles = %s, precio_total = %s
                WHERE ID_paquete = %s
            """
            cursor.execute(consulta_actualizar, (
                nueva_fecha_ida, nueva_fecha_vuelta, nueva_descripcion,
                nuevas_actividades, nuevo_precio, ID_paquete
            ))
            conexion.commit()

            messagebox.showinfo("Paquete Actualizado",
                                f"El paquete turístico con ID '{ID_paquete}' ha sido actualizado:\n"
                                f"- Fecha de Ida: {nueva_fecha_ida}\n"
                                f"- Fecha de Vuelta: {nueva_fecha_vuelta}\n"
                                f"- Descripción: {nueva_descripcion}\n"
                                f"- Actividades: {nuevas_actividades}\n"
                                f"- Precio Total: {nuevo_precio}.")

            conexion.close()

        except pymysql.Error as e:
            messagebox.showerror("Error", f"Error al modificar el paquete turístico: {e}")

    def eliminar_paquete_turistico(self, ID_paquete, ventana):
        if not ID_paquete:
            messagebox.showwarning("Campo Vacío", "El campo de ID paquete turístico no puede estar vacío.")
            return

        try:
            # Conectarse a la base de datos
            conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba4'
            )
            cursor = conexion.cursor()

            # Validar si el paquete turístico existe
            consulta_paquete = "SELECT COUNT(*) FROM paquete_turistico WHERE ID_paquete = %s"
            cursor.execute(consulta_paquete, (ID_paquete,))
            paquete_existe = cursor.fetchone()[0]

            if not paquete_existe:
                messagebox.showerror("Error", f"El paquete turístico con ID '{ID_paquete}' no existe.")
                return

            # Eliminar el paquete turístico
            consulta_eliminar = "DELETE FROM paquete_turistico WHERE ID_paquete = %s"
            cursor.execute(consulta_eliminar, (ID_paquete,))
            conexion.commit()

            messagebox.showinfo("Paquete Eliminado", f"El paquete turístico con ID '{ID_paquete}' ha sido eliminado.")

            ventana.destroy()  # Cerrar la ventana después de la eliminación
            conexion.close()

        except pymysql.Error as e:
            messagebox.showerror("Error", f"Error al eliminar el paquete turístico: {e}")