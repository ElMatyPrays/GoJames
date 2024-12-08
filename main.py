import mysql.connector
import pymysql


# Configuración de la conexión inicial (sin base de datos)
host = 'localhost'
user = 'root'  # Cambia esto por tu usuario de MySQL
password = ''  # Cambia esto por tu contraseña de MySQL
database = 'prueba4'  # Nombre de la base de datos

try:
    # Conexión al servidor MySQL sin base de datos específica
    conexion = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = conexion.cursor()

    # Verificar si la base de datos ya existe
    cursor.execute("SHOW DATABASES")
    bases_de_datos = [db[0] for db in cursor.fetchall()]

    if database not in bases_de_datos:
        cursor.execute(f"CREATE DATABASE {database}")
        print(f"Base de datos '{database}' creada.")
    else:
        print(f"La base de datos '{database}' ya existe.")

    # Conectar a la base de datos existente o recién creada
    cursor.execute(f"USE {database}")

    # Verificar si las tablas existen antes de crearlas
    cursor.execute("SHOW TABLES")
    tablas_existentes = [tabla[0] for tabla in cursor.fetchall()]

    tablas_a_crear = {
        "cliente": """
            CREATE TABLE Cliente (
                RUT VARCHAR(12) NOT NULL,  -- Se usa VARCHAR para RUT
                nombre_cliente VARCHAR(35) NOT NULL,
                password_cliente VARCHAR(45) NOT NULL,
                estado TINYINT(1) NOT NULL DEFAULT 1,  -- Estado activo por defecto
                PRIMARY KEY (RUT)
            )
        """,
        "reserva": """
            CREATE TABLE Reserva (
                ID_reserva INT(11) NOT NULL AUTO_INCREMENT,  
                RUT_cliente VARCHAR(12) NOT NULL,
                ID_paquete INT(11) NOT NULL,
                estado TINYINT(1) NOT NULL DEFAULT 1,  -- Estado activo por defecto
                PRIMARY KEY (ID_reserva),
                KEY RUT_cliente_idx (RUT_cliente),
                KEY ID_paquete_idx (ID_paquete)
            )
        """,
        "paquete_turistico": """
            CREATE TABLE paquete_turistico (
                ID_paquete INT(11) NOT NULL AUTO_INCREMENT,
                ID_lista_destinos INT(11) NOT NULL,
                fecha_ida VARCHAR(11) NOT NULL,
                fecha_vuelta VARCHAR(11) NOT NULL,
                precio_total INT(9) NOT NULL,
                estado TINYINT(1) NOT NULL DEFAULT 1,  -- Estado activo por defecto
                PRIMARY KEY (ID_paquete),
                KEY ID_lista_destinos_idx (ID_lista_destinos)
            )
        """,
        "lista_destinos": """
            CREATE TABLE lista_destinos (
                ID_lista_destinos INT(11) NOT NULL AUTO_INCREMENT,
                ID_destino_1 INT(11) NOT NULL,
                ID_destino_2 INT(11) NOT NULL,
                ID_destino_3 INT(11) NOT NULL,
                ID_destino_4 INT(11) NOT NULL,
                ID_destino_5 INT(11) NOT NULL,
                estado TINYINT(1) NOT NULL DEFAULT 1,  -- Estado activo por defecto
                PRIMARY KEY (ID_lista_destinos),
                KEY ID_destino_1_idx (ID_destino_1),
                KEY ID_destino_2_idx (ID_destino_2),
                KEY ID_destino_3_idx (ID_destino_3),
                KEY ID_destino_4_idx (ID_destino_4),
                KEY ID_destino_5_idx (ID_destino_5)
            )
        """,
        "Destino": """
            CREATE TABLE destino (
                ID_destino INT(11) NOT NULL AUTO_INCREMENT,
                nombre VARCHAR(45) NOT NULL,
                descripcion VARCHAR(120) NOT NULL,
                actividades_disponibles VARCHAR(120) NOT NULL,
                costo INT(9) NOT NULL,
                estado TINYINT(1) NOT NULL DEFAULT 1,  -- Estado activo por defecto
                PRIMARY KEY (ID_destino)
            )
        """
    }

# Crear tablas solo si no existen
    for nombre_tabla, sql_creacion in tablas_a_crear.items():
        if nombre_tabla not in tablas_existentes:
            cursor.execute(sql_creacion)
            print(f"Tabla '{nombre_tabla}' creada.")
        else:
            print(f"La tabla '{nombre_tabla}' ya existe.")

    # Añadir restricciones de clave foránea
    restricciones = [
        "ALTER TABLE reserva ADD CONSTRAINT fk_RUT_cliente FOREIGN KEY (RUT_cliente) REFERENCES cliente (RUT_cliente), ADD CONSTRAINT fk_ID_paquete FOREIGN KEY (ID_paquete) REFERENCES paquete_turistico (ID_paquete)",
        "ALTER TABLE paquete_turistico ADD CONSTRAINT fk_ID_lista_destinos FOREIGN KEY (ID_lista_destinos) REFERENCES lista_destinos (ID_lista_destinos)",
        "ALTER TABLE lista_destinos ADD CONSTRAINT fk_ID_destino_1 FOREIGN KEY (ID_destino_1) REFERENCES destino (ID_destino), ALTER TABLE lista_destinos ADD CONSTRAINT fk_ID_destino_2 FOREIGN KEY (ID_destino_2) REFERENCES destino (ID_destino), ALTER TABLE lista_destinos ADD CONSTRAINT fk_ID_destino_3 FOREIGN KEY (ID_destino_3) REFERENCES destino (ID_destino), ALTER TABLE lista_destinos ADD CONSTRAINT fk_ID_destino_4 FOREIGN KEY (ID_destino_4) REFERENCES destino (ID_destino), ALTER TABLE lista_destinos ADD CONSTRAINT fk_ID_destino_5 FOREIGN KEY (ID_destino_5) REFERENCES destino (ID_destino)"
    ]

    for restriccion in restricciones:
        try:
            cursor.execute(restriccion)
        except mysql.connector.Error as err:
            print(f"Error al aplicar la restricción: {err}")

    print("Tablas y restricciones verificadas exitosamente.")

    cursor.close()
    conexion.close()

    # Conexión final con pymysql para realizar operaciones
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("Conexión exitosa a la base de datos.")

    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    for table in cursor.fetchall():
        print(table)

    cursor.close()
    connection.close()

except mysql.connector.Error as e:
    print(f"Error de MySQL: {e}")
except pymysql.MySQLError as e:
    print(f"Error de PyMySQL: {e}")