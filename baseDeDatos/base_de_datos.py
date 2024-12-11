import mysql.connector

def baseDeDatos():
    # Configuración de la conexión inicial
    host = 'localhost'
    user = 'root'  # Cambia esto por tu usuario de MySQL
    password = ''  # Cambia esto por tu contraseña de MySQL
    database = 'prueba4'  # Nombre de la base de datos

    try:
        # Conexión al servidor MySQL
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = conexion.cursor()

        # Crear la base de datos si no existe
        cursor.execute("SHOW DATABASES")
        bases_de_datos = [db[0] for db in cursor.fetchall()]

        if database not in bases_de_datos:
            cursor.execute(f"CREATE DATABASE {database}")
            print(f"Base de datos '{database}' creada.")
        else:
            print(f"La base de datos '{database}' ya existe.")

        # Usar la base de datos
        cursor.execute(f"USE {database}")

        # Crear las tablas en el orden correcto
        tablas_a_crear = {
            "cliente": """
                CREATE TABLE IF NOT EXISTS cliente (
                    RUT VARCHAR(12) NOT NULL,
                    nombre_cliente VARCHAR(35) NOT NULL,
                    password_cliente VARCHAR(45) NOT NULL,
                    estado TINYINT(1) NOT NULL DEFAULT 1,
                    PRIMARY KEY (RUT)
                )
            """,
            "destino": """
                CREATE TABLE IF NOT EXISTS destino (
                    ID_destino INT(11) NOT NULL AUTO_INCREMENT,
                    nombre VARCHAR(45) NOT NULL UNIQUE,
                    costo INT(9) NOT NULL,
                    PRIMARY KEY (ID_destino)
                )
            """,
            "lista_destinos": """
                CREATE TABLE IF NOT EXISTS lista_destinos (
                    ID_lista_destinos INT(11) NOT NULL AUTO_INCREMENT,
                    ID_destino_1 INT(11) NOT NULL,
                    ID_destino_2 INT(11) NOT NULL,
                    ID_destino_3 INT(11) NOT NULL,
                    ID_destino_4 INT(11) NOT NULL,
                    ID_destino_5 INT(11) NOT NULL,
                    PRIMARY KEY (ID_lista_destinos)
                )
            """,
            "paquete_turistico": """
                CREATE TABLE IF NOT EXISTS paquete_turistico (
                    ID_paquete INT(11) NOT NULL AUTO_INCREMENT,
                    ID_lista_destinos INT(11) NOT NULL,
                    fecha_ida VARCHAR(11) NOT NULL,
                    fecha_vuelta VARCHAR(11) NOT NULL,
                    descripcion VARCHAR(120) NOT NULL,
                    actividades_disponibles VARCHAR(120) NOT NULL,
                    precio_total INT(9) NOT NULL,
                    disponibilidad INT(11) NOT NULL,
                    PRIMARY KEY (ID_paquete),
                    UNIQUE KEY (ID_lista_destinos, fecha_ida, fecha_vuelta)
                )
            """,
            "reserva": """
                CREATE TABLE IF NOT EXISTS reserva (
                    ID_reserva INT(11) NOT NULL AUTO_INCREMENT,
                    RUT_cliente VARCHAR(12) NOT NULL,
                    ID_paquete INT(11),
                    ID_destino INT(11),
                    fecha VARCHAR(11),
                    estado TINYINT(1) NOT NULL DEFAULT 1,
                    PRIMARY KEY (ID_reserva)
                )
            """
        }

        # Crear las tablas
        for nombre, sql in tablas_a_crear.items():
            cursor.execute(sql)
            print(f"Tabla '{nombre}' creada o ya existía.")

        # Insertar datos base con INSERT IGNORE
        datos_a_insertar = {
            "destino": """
                INSERT IGNORE INTO destino (nombre, costo)
                VALUES 
                    ('Madrid', 100),
                    ('Barcelona', 105),
                    ('Roma', 110),
                    ('Paris', 98),
                    ('Milan', 108),
                    ('Berlin', 120),
                    ('Londres', 125);
            """,
            "lista_destinos": """
                INSERT IGNORE INTO lista_destinos (ID_destino_1, ID_destino_2, ID_destino_3, ID_destino_4, ID_destino_5)
                VALUES 
                    (1, 2, 3, 4, 5),
                    (3, 7, 1, 2, 6),
                    (7, 5, 6, 4, 1);
            """,
            "paquete_turistico": """
                INSERT IGNORE INTO paquete_turistico 
                (ID_lista_destinos, fecha_ida, fecha_vuelta, descripcion, actividades_disponibles, precio_total, disponibilidad)
                VALUES 
                    (1, '15/06/2024', '21/06/2024', '5 destinos turísticos, comida rica', 
                     'Visita Santiago Bernabéu, Sagrada Familia, Coliseo Romano, Torre Eiffel, San Siro', 1100, 10),
                    (2, '20/07/2024', '01/08/2024', '5 destinos turísticos, comida rica', 
                     'Coliseo Romano, Big Ben, Santiago Bernabéu, Sagrada Familia, Puerta de Brandeburgo', 1250, 10),
                    (3, '01/08/2024', '12/08/2024', '5 destinos turísticos, comida rica', 
                     'Big Ben, San Siro, Puerta de Brandeburgo, Torre Eiffel, Santiago Bernabéu', 1350, 10);
            """
        }

        for nombre, consulta in datos_a_insertar.items():
            cursor.execute(consulta)
            print(f"Datos insertados (o ignorados si ya existían) en '{nombre}'.")

        # Confirmar cambios
        conexion.commit()
        cursor.close()
        conexion.close()

    except mysql.connector.Error as e:
        print(f"Error de MySQL: {e}")

# Llamar a la función
baseDeDatos()
