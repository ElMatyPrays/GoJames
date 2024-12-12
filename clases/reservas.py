import mysql.connector
import pymysql

class reserva():

    def Crear_reserva_destinos(self, RUT_cliente, ID_destino, fecha):

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
        cursor = "INSERT INTO reserva (RUT_cliente, ID_destino, fecha) VALUES ('{}', {}, '{}')".format(
            RUT_cliente, ID_destino, fecha
            )

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