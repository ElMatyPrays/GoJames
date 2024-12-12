import pymysql
import mysql.connector
from itertools import cycle
from baseDeDatos.base_de_datos import baseDeDatos
from clases.reservas import Reserva
from datetime import datetime


#BASE DE DATOS

baseDeDatos()


#------------------------------------------------------------------------------------------------



#TKINTER

from tkinter import Tk, Label, Button, Entry, Frame, messagebox, mainloop, Listbox, END, Scrollbar
from PIL import Image, ImageTk
import re



class Login:
    def __init__(self):
        self.destinos = ["Destino 1", "Destino 2", "Destino 3"]  # Lista compartida de destinos
        self.actividades = ["Actividad 1", "Actividad 2", "Actividad 3", "Actividad 4",
                            "Actividad 5"]  # Lista de actividades
        self.ventana = Tk()
        self.ventana.geometry("400x400")
        self.ventana.title("Login")

        fondo = "#ff6347"

        ##########FRAMES###########

        self.frame_superior = Frame(self.ventana)
        self.frame_superior.configure(bg=fondo)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.ventana)
        self.frame_inferior.configure(bg=fondo)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        ##########TITULO###########

        self.titulo = Label(self.frame_superior,
                            text="Login",
                            font=("Tahoma", 40, "bold"),
                            bg=fondo)
        self.titulo.pack(side="top", pady=20)



        #########DATOS##############

        self.label_usuario = Label(self.frame_inferior, text="RUT", font=("Helvetica", 18), bg=fondo, fg="black")
        self.label_usuario.grid(row=0, column=0, padx=10, sticky="e")
        self.entry_usuario = Entry(self.frame_inferior, bd=0, width=14, font=("Helvetica", 18))
        self.entry_usuario.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")

        self.label_contraseña = Label(self.frame_inferior, text="Contraseña", font=("Helvetica", 18), bg=fondo, fg="black")
        self.label_contraseña.grid(row=1, column=0, padx=10, sticky="e")
        self.entry_contraseña = Entry(self.frame_inferior, bd=0, width=14, font=("Helvetica", 18), show="●")
        self.entry_contraseña.grid(row=1, column=1, columnspan=3, padx=5, sticky="w")

        self.boton_ingresar = Button(self.frame_inferior, text="Ingresar", width=16, font=("Helvetica", 12),
                                     command=self.entrar)
        self.boton_ingresar.grid(row=2, column=1, pady=35)

        #####FIN#####

        mainloop()

    def entrar(self):
        while True:
            rut = self.entry_usuario.get()
            contraseña = self.entry_contraseña.get()

            if not rut:
                messagebox.showwarning("Campo Vacío", "El campo de RUT no puede estar vacío.")
                break

            if not re.match(r'^\d{1,8}-[\dkK]$', rut):
                messagebox.showwarning("Formato Inválido", "El RUT debe tener el formato 12345678-K.")
                break

            if not contraseña:
                messagebox.showwarning("Campo Vacío", "El campo Contraseña no puede estar vacío.")
                break


                # Separar el cuerpo del RUT y el dígito verificador
            cuerpo, dv = rut.split('-')
            dv = dv.upper()  # Convertir el dígito verificador a mayúscula si es necesario

            # Calcular el dígito verificador esperado
            reversed_digits = map(int, reversed(cuerpo))
            factors = cycle(range(2, 8))
            suma = sum(d * f for d, f in zip(reversed_digits, factors))
            dv_calculado = str((-suma) % 11)
            if dv_calculado == '10':
                dv_calculado = 'K'

            # Comparar el dígito verificador ingresado con el calculado
            if dv != dv_calculado:
                messagebox.showwarning("RUT Incorrecto", "El RUT ingresado no es válido.")
                break

            try:
                # Conectar a la base de datos
                conexion = pymysql.connect(host='localhost', user='root', password='', db='prueba4')
                cursor = conexion.cursor()

                # Validar si el usuario existe
                consulta_estado = "SELECT * FROM cliente WHERE RUT = %s AND password_cliente = %s"
                cursor.execute(consulta_estado, (rut,contraseña))
                resultado = cursor.fetchone()

                if resultado:
                    self.ventana.destroy()
                    self.ventana2()
                    break

                elif not resultado:
                    messagebox.showwarning("RUT No Encontrado", f"No existe un usuario con el RUT: {rut}.")
                    break

            except Exception as e:
                messagebox.showerror("Error", f"Error al verificar el RUT: {e}")
                break

            conexion.close()


    ###VENTANA2###

    def ventana2(self):
        self.ventana2 = Tk()
        self.ventana2.geometry("600x500")
        self.ventana2.title("Viajes Aventura")

        fondo1 = "#ff6347"

        self.frame_superior = Frame(self.ventana2)
        self.frame_superior.configure(bg=fondo1)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.ventana2)
        self.frame_inferior.configure(bg=fondo1)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        self.titulo2 = Label(self.frame_superior,
                             text="Gestion De Destinos",
                             font=("Tahoma", 36, "bold"),
                             bg=fondo1)
        self.titulo2.pack(side="top", pady=20)

        # AGREGAR DESTINOOO####
        self.boton_m_destino = Button(self.frame_inferior, text="Agregar Destino", width=100, font=("Helvetica", 12),
                                      command=self.v_a_destino)
        self.boton_m_destino.grid(row=1, column=1, padx=50, pady=10)

        # Pasamos la lista destinos a la ventana de modificación
        self.boton_mod_destino = Button(self.frame_inferior, text="Modificar Destino", width=100, font=("Helvetica", 12),
                                        command=lambda: self.v_mod_destino(self.destinos))
        self.boton_mod_destino.grid(row=2, column=1, padx=50, pady=10)

        # Botón Ver Paquete Turístico
        self.boton_paquete = Button(self.frame_inferior, text="Ver Paquete Turístico", width=100, font=("Helvetica", 12),
                                    command=self.inter_paquete_turistico)
        self.boton_paquete.grid(row=3, column=1, padx=50, pady=10)

        self.boton_reservar_pq = Button(self.frame_inferior, text="Reservar Paquete Turístico", width=100,
                                        font=("Helvetica", 12), command=self.reservar_paquete)
        self.boton_reservar_pq.grid(row=4, column=1, padx=50, pady=10)

        self.boton_modificar_pq = Button(self.frame_inferior, text="Modificar Paquete Turístico", width=100,
                                         font=("Helvetica", 12), command=self.v_mod_paquete_turistico)
        self.boton_modificar_pq.grid(row=5, column=1, padx=50, pady=10)



    ########VENTANA AGREGAR DESTINO##########

    def v_a_destino(self):
        reserva = Reserva()
        ventana = Tk()
        ventana.geometry("500x500")
        ventana.title("Crear Reserva destino")

        fondo3 = "#ff6347"

        # Configuración del frame
        frame = Frame(ventana, bg=fondo3)
        frame.pack(fill="both", expand=True)

        # Título
        titulo = Label(frame, text="Crear Reserva", font=("Tahoma", 20, "bold"), bg=fondo3)
        titulo.pack(pady=10)

        # Entrada para RUT del cliente
        label_rut = Label(frame, text="RUT Cliente:", font=("Helvetica", 12), bg=fondo3)
        label_rut.pack(pady=5)

        entrada_rut = Entry(frame, font=("Helvetica", 12), width=30)
        entrada_rut.pack(pady=5)

        # Entrada para Nombre del destino
        label_destino = Label(frame, text="Nombre Destino:", font=("Helvetica", 12), bg=fondo3)
        label_destino.pack(pady=5)

        entrada_destino = Entry(frame, font=("Helvetica", 12), width=30)
        entrada_destino.pack(pady=5)

        # Entrada para Fecha
        label_fecha = Label(frame, text="Fecha (DD-MM-YYYY):", font=("Helvetica", 12), bg=fondo3)
        label_fecha.pack(pady=5)

        entrada_fecha = Entry(frame, font=("Helvetica", 12), width=30)
        entrada_fecha.pack(pady=5)

        # Función para validar la fecha antes de proceder con la reserva
        def validar_reserva():
            try:
                fecha = entrada_fecha.get()
                # Validar formato de fecha
                datetime.strptime(fecha, "%d-%m-%Y")  # Asegura que la fecha esté en formato dd/mm/yyyy
                reserva.validar_y_guardar_reserva(entrada_rut.get(), entrada_destino.get(), fecha)
            except ValueError:
                messagebox.showerror("Error", "El formato de la fecha no es válido. Use dd-mm-yyyy.")

        # Botón para crear reserva
        boton_crear_reserva = Button(
            frame, text="Crear Reserva", font=("Helvetica", 14),
            command=validar_reserva
        )
        boton_crear_reserva.pack(pady=20)

        ventana.mainloop()


    # Función para eliminar destino seleccionado
    def eliminar_destino(self):
        try:
            # Obtener la selección actual
            seleccionado = self.lista_destinos.curselection()
            if seleccionado:
                # Eliminar el destino seleccionado
                self.lista_destinos.delete(seleccionado)
            else:
                messagebox.showwarning("Advertencia", "Por favor, selecciona un destino para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")



    #######VENTANA MODIFICAR DESTINO##########

    def v_mod_destino(self, event=None):
        reserva = Reserva()
        ventana = Tk()
        ventana.geometry("400x500")  # Aumento el tamaño de la ventana para agregar más elementos
        ventana.title("Modificar Reserva")

        fondo3 = "#ff6347"

        # Configuración del frame
        frame = Frame(ventana, bg=fondo3)
        frame.pack(fill="both", expand=True)

        # Título
        titulo = Label(frame, text="Modificar Reserva", font=("Helvetica", 18, "bold"), bg=fondo3)
        titulo.pack(pady=10)

        # Entrada para ID de la reserva
        label_id_reserva = Label(frame, text="ID Reserva:", font=("Helvetica", 12), bg=fondo3)
        label_id_reserva.pack(pady=5)

        entrada_id_reserva = Entry(frame, font=("Helvetica", 12), width=30)
        entrada_id_reserva.pack(pady=5)

        # Entrada para el nuevo nombre del destino
        label_destino = Label(frame, text="Nuevo Destino:", font=("Helvetica", 12), bg=fondo3)
        label_destino.pack(pady=5)

        entrada_destino = Entry(frame, font=("Helvetica", 12), width=30)
        entrada_destino.pack(pady=5)

        # Entrada para la nueva fecha
        label_fecha = Label(frame, text="Nueva Fecha (DD-MM-YYYY):", font=("Helvetica", 12), bg=fondo3)
        label_fecha.pack(pady=5)

        entrada_fecha = Entry(frame, font=("Helvetica", 12), width=30)
        entrada_fecha.pack(pady=5)

        # Botón para modificar la reserva
        boton_modificar_reserva = Button(
            frame, text="Modificar Reserva", font=("Helvetica", 14),
            command=lambda: reserva.modificar_destino_reserva(
                entrada_id_reserva.get(), entrada_destino.get(), entrada_fecha.get(), ventana
            )
        )
        boton_modificar_reserva.pack(pady=10)

        # Botón para eliminar la reserva
        boton_eliminar_reserva = Button(
            frame, text="Eliminar Reserva", font=("Helvetica", 14), bg="red", fg="white",
            command=lambda: reserva.eliminar_reserva(entrada_id_reserva.get(), ventana)
        )
        boton_eliminar_reserva.pack(pady=10)

        ventana.mainloop()

    # Método para validar el formato de la fecha
    def validar_fecha(self, fecha):
        # Validar el formato de la fecha: dd/mm/yyyy
        regex = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
        if re.match(regex, fecha):
            return True
        return False

    # Función para eliminar destino seleccionado
    def eliminar_destino(self):
        try:
            # Obtener la selección actual
            seleccionado = self.lista_destinos.curselection()
            if seleccionado:
                # Eliminar el destino seleccionado
                self.lista_destinos.delete(seleccionado)
            else:
                messagebox.showwarning("Advertencia", "Por favor, selecciona un destino para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


        # Mensaje de éxito
        messagebox.showinfo("", "Destino Modificado Correctamente")
        self.v_mod_destino.destroy()

    ### VENTANA INTERMEDIA DE PAQUETE TURISTICO ###

    def inter_paquete_turistico(self):
        self.ventana_intermedia = Tk()
        self.ventana_intermedia.geometry("400x500")
        self.ventana_intermedia.title("Seleccionar Paquete Turístico")
        fondo = "#ff6347"

        # Establecer el color de fondo de la ventana
        self.ventana_intermedia.configure(bg=fondo)

        # Frame superior
        self.frame_superior = Frame(self.ventana_intermedia)
        self.frame_superior.configure(bg=fondo)
        self.frame_superior.pack(fill="both", expand=True)

        # Frame inferior para los botones
        self.frame_inferior = Frame(self.ventana_intermedia)
        self.frame_inferior.configure(bg=fondo)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)


        # Título
        titulo = Label(self.ventana_intermedia, text="Selecciona un Paquete Turístico", font=("Calisto MT", 18, "bold"),
                       bg=fondo)
        titulo.pack(pady=20)

        # Botón para Paquete Turístico 1
        boton_paquete1 = Button(self.ventana_intermedia, text="Paquete Turístico 1", font=("Arial", 14),
                                command=self.ver_paquete_turistico1)
        boton_paquete1.pack(pady=10)

        # Botón para Paquete Turístico 2
        boton_paquete2 = Button(self.ventana_intermedia, text="Paquete Turístico 2", font=("Arial", 14),
                                command=self.ver_paquete_turistico2)
        boton_paquete2.pack(pady=20)

        # Botón para Paquete Turístico 3
        boton_paquete3 = Button(self.ventana_intermedia, text="Paquete Turístico 3", font=("Arial", 14),
                                command=self.ver_paquete_turistico3)
        boton_paquete3.pack(pady=30)

        # Botón cerrar ventana
        boton_cerrar = Button(self.ventana_intermedia, text="Cerrar", font=("Arial", 12), command=self.ventana_intermedia.destroy)
        boton_cerrar.pack(pady=40)

        self.ventana_intermedia.mainloop()

    ### Ventana de Ver Paquete Turístico1 ###
    def ver_paquete_turistico1(self):
        ventana_paquete1 = Tk()
        ventana_paquete1.geometry("400x500")
        ventana_paquete1.title("Paquete Turístico 2")

        fondo = "#ff6347"

        # Frame superior
        frame_superior = Frame(ventana_paquete1, bg=fondo)
        frame_superior.pack(fill="both", expand=True)

        # Frame inferior
        frame_inferior = Frame(ventana_paquete1, bg=fondo)
        frame_inferior.pack(fill="both", expand=True)

        # Título
        titulo = Label(frame_superior, text="Paquete Turístico: Islas", font=("Calisto MT", 20, "bold"), bg=fondo)
        titulo.pack(pady=20)

        # Lista de destinos
        titulo_destinos = Label(frame_inferior, text="Destinos incluidos:", font=("Arial", 14), bg=fondo)
        titulo_destinos.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        lista_destinos = Listbox(frame_inferior, height=5, width=30, font=("Arial", 12))
        lista_destinos.grid(row=1, column=0, padx=10, pady=5)
        for destino in self.destinos:
            lista_destinos.insert(END, destino)

        # Lista de actividades
        titulo_actividades = Label(frame_inferior, text="Actividades incluidas:", font=("Arial", 14), bg=fondo)
        titulo_actividades.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        lista_actividades = Listbox(frame_inferior, height=5, width=30, font=("Arial", 12))
        lista_actividades.grid(row=3, column=0, padx=10, pady=5)
        for actividad in self.actividades:
            lista_actividades.insert(END, actividad)

        # Botón cerrar ventana
        boton_cerrar = Button(frame_inferior, text="Cerrar", font=("Arial", 12), command=ventana_paquete1.destroy)
        boton_cerrar.grid(row=4, column=0, pady=20)

        ventana_paquete1.mainloop()

    def ver_paquete_turistico1(self):
        ventana_paquete1 = Tk()
        ventana_paquete1.geometry("600x700")
        ventana_paquete1.title("Detalles del Paquete Turístico")

        fondo2 = "#ff6347"

        # Frame superior
        frame_superior = Frame(ventana_paquete1, bg=fondo2)
        frame_superior.pack(fill="both", expand=True)

        # Frame inferior
        frame_inferior = Frame(ventana_paquete1, bg=fondo2)
        frame_inferior.pack(fill="both", expand=True)

        # Título del paquete
        titulo = Label(frame_superior, text="Paquete Turístico: Islas ", font=("Calisto MT", 24, "bold"), bg=fondo2)
        titulo.pack(pady=20)

        # Información general del paquete
        descripcion_paquete = Label(frame_superior, text="Explora destinos increíbles y disfruta actividades únicas.",
                                    font=("Arial", 14), bg=fondo2)
        descripcion_paquete.pack(pady=10)

        # Detalles de destinos incluidos
        titulo_destinos = Label(frame_inferior, text="Destinos incluidos:", font=("Arial", 16, "bold"), bg=fondo2)
        titulo_destinos.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        lista_destinos = Listbox(frame_inferior, height=5, width=50, font=("Arial", 12))
        lista_destinos.grid(row=1, column=0, padx=10, pady=5)
        for destino in self.destinos:
            lista_destinos.insert(END, destino)

        # Detalles de actividades incluidas
        titulo_actividades = Label(frame_inferior, text="Actividades incluidas:", font=("Arial", 16, "bold"), bg=fondo2)
        titulo_actividades.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        lista_actividades = Listbox(frame_inferior, height=5, width=50, font=("Arial", 12))
        lista_actividades.grid(row=3, column=0, padx=10, pady=5)
        for actividad in self.actividades:
            lista_actividades.insert(END, actividad)

        # Fechas específicas
        titulo_fechas = Label(frame_inferior, text="Fechas disponibles:", font=("Arial", 16, "bold"), bg=fondo2)
        titulo_fechas.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        lista_fechas = Listbox(frame_inferior, height=3, width=50, font=("Arial", 12))
        lista_fechas.grid(row=5, column=0, padx=10, pady=5)
        fechas_disponibles = ["15/06/2024", "01/07/2024", "15/07/2024"]
        for fecha in fechas_disponibles:
            lista_fechas.insert(END, fecha)

        # Precio total
        titulo_precio = Label(frame_inferior, text="Precio Total:", font=("Arial", 16, "bold"), bg=fondo2)
        titulo_precio.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        precio_total2 = Label(frame_inferior, text="$1500 USD", font=("Arial", 14), bg=fondo2, fg="green")
        precio_total2.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        # Botón cerrar ventana
        boton_cerrar = Button(frame_inferior, text="Cerrar", font=("Arial", 12), command=ventana_paquete1.destroy)
        boton_cerrar.grid(row=8, column=0, pady=20)

        ventana_paquete1.mainloop()

    ### Ventana de Ver Paquete Turístico 2 ###
    def ver_paquete_turistico2(self):
        ventana_paquete2 = Tk()
        ventana_paquete2.geometry("400x500")
        ventana_paquete2.title("Paquete Turístico 2")

        fondo2 = "#ff6347"

        # Frame superior
        frame_superior = Frame(ventana_paquete2, bg=fondo2)
        frame_superior.pack(fill="both", expand=True)

        # Frame inferior
        frame_inferior = Frame(ventana_paquete2, bg=fondo2)
        frame_inferior.pack(fill="both", expand=True)

        # Título
        titulo = Label(frame_superior, text="Paquete Turístico: Islas", font=("Calisto MT", 20, "bold"), bg=fondo2)
        titulo.pack(pady=20)

        # Lista de destinos
        titulo_destinos = Label(frame_inferior, text="Destinos incluidos:", font=("Arial", 14), bg=fondo2)
        titulo_destinos.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        lista_destinos = Listbox(frame_inferior, height=5, width=30, font=("Arial", 12))
        lista_destinos.grid(row=1, column=0, padx=10, pady=5)
        for destino in self.destinos:
            lista_destinos.insert(END, destino)

        # Lista de actividades
        titulo_actividades = Label(frame_inferior, text="Actividades incluidas:", font=("Arial", 14), bg=fondo2)
        titulo_actividades.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        lista_actividades = Listbox(frame_inferior, height=5, width=30, font=("Arial", 12))
        lista_actividades.grid(row=3, column=0, padx=10, pady=5)
        for actividad in self.actividades:
            lista_actividades.insert(END, actividad)

        # Botón cerrar ventana
        boton_cerrar = Button(frame_inferior, text="Cerrar", font=("Arial", 12), command=ventana_paquete2.destroy)
        boton_cerrar.grid(row=4, column=0, pady=20)

        ventana_paquete2.mainloop()

    def ver_paquete_turistico2(self):
        ventana_paquete2 = Tk()
        ventana_paquete2.geometry("600x700")
        ventana_paquete2.title("Detalles del Paquete Turístico")

        fondo2 = "#ff6347"

        # Frame superior
        frame_superior = Frame(ventana_paquete2, bg=fondo2)
        frame_superior.pack(fill="both", expand=True)

        # Frame inferior
        frame_inferior = Frame(ventana_paquete2, bg=fondo2)
        frame_inferior.pack(fill="both", expand=True)

        # Título del paquete
        titulo = Label(frame_superior, text="Paquete Turístico: Aventura Total", font=("Calisto MT", 24, "bold"),
                       bg=fondo2)
        titulo.pack(pady=20)

        # Información general del paquete
        descripcion_paquete = Label(frame_superior, text="Explora destinos increíbles y disfruta actividades únicas.",
                                    font=("Arial", 14), bg=fondo2)
        descripcion_paquete.pack(pady=10)

        # Detalles de destinos incluidos
        titulo_destinos = Label(frame_inferior, text="Destinos incluidos:", font=("Arial", 16, "bold"), bg=fondo2)
        titulo_destinos.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        lista_destinos = Listbox(frame_inferior, height=5, width=50, font=("Arial", 12))
        lista_destinos.grid(row=1, column=0, padx=10, pady=5)
        for destino in self.destinos:
            lista_destinos.insert(END, destino)

        # Detalles de actividades incluidas
        titulo_actividades = Label(frame_inferior, text="Actividades incluidas:", font=("Arial", 16, "bold"), bg=fondo2)
        titulo_actividades.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        lista_actividades = Listbox(frame_inferior, height=5, width=50, font=("Arial", 12))
        lista_actividades.grid(row=3, column=0, padx=10, pady=5)
        for actividad in self.actividades:
            lista_actividades.insert(END, actividad)

        # Fechas específicas
        titulo_fechas = Label(frame_inferior, text="Fechas disponibles:", font=("Arial", 16, "bold"), bg=fondo2)
        titulo_fechas.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        lista_fechas = Listbox(frame_inferior, height=3, width=50, font=("Arial", 12))
        lista_fechas.grid(row=5, column=0, padx=10, pady=5)
        fechas_disponibles = ["15/06/2024", "01/07/2024", "15/07/2024"]
        for fecha in fechas_disponibles:
            lista_fechas.insert(END, fecha)

        # Precio total
        titulo_precio = Label(frame_inferior, text="Precio Total:", font=("Arial", 16, "bold"), bg=fondo2)
        titulo_precio.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        precio_total2 = Label(frame_inferior, text="$1500 USD", font=("Arial", 14), bg=fondo2, fg="green")
        precio_total2.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        # Botón cerrar ventana
        boton_cerrar = Button(frame_inferior, text="Cerrar", font=("Arial", 12), command=ventana_paquete2.destroy)
        boton_cerrar.grid(row=8, column=0, pady=20)

        ventana_paquete2.mainloop()

    ### Ventana de Ver Paquete Turístico 3 ###
    def ver_paquete_turistico3(self):
        ventana_paquete3 = Tk()
        ventana_paquete3.geometry("400x500")
        ventana_paquete3.title("Paquete Turístico 2")

        fondo2 = "#ff6347"

        # Frame superior
        frame_superior = Frame(ventana_paquete3, bg=fondo2)
        frame_superior.pack(fill="both", expand=True)

        # Frame inferior
        frame_inferior = Frame(ventana_paquete3, bg=fondo2)
        frame_inferior.pack(fill="both", expand=True)

        # Título
        titulo = Label(frame_superior, text="Paquete Turístico: Islas", font=("Calisto MT", 20, "bold"), bg=fondo2)
        titulo.pack(pady=20)

        # Lista de destinos
        titulo_destinos = Label(frame_inferior, text="Destinos incluidos:", font=("Arial", 14), bg=fondo2)
        titulo_destinos.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        lista_destinos = Listbox(frame_inferior, height=5, width=30, font=("Arial", 12))
        lista_destinos.grid(row=1, column=0, padx=10, pady=5)
        for destino in self.destinos:
            lista_destinos.insert(END, destino)

        # Lista de actividades
        titulo_actividades = Label(frame_inferior, text="Actividades incluidas:", font=("Arial", 14), bg=fondo2)
        titulo_actividades.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        lista_actividades = Listbox(frame_inferior, height=5, width=30, font=("Arial", 12))
        lista_actividades.grid(row=3, column=0, padx=10, pady=5)
        for actividad in self.actividades:
            lista_actividades.insert(END, actividad)

        # Botón cerrar ventana
        boton_cerrar = Button(frame_inferior, text="Cerrar", font=("Arial", 12), command=ventana_paquete3.destroy)
        boton_cerrar.grid(row=4, column=0, pady=20)

        ventana_paquete3.mainloop()

    def ver_paquete_turistico3(self):
        ventana_paquete3 = Tk()
        ventana_paquete3.geometry("600x700")
        ventana_paquete3.title("Detalles del Paquete Turístico")

        fondo2 = "#ff6347"

        # Frame superior
        frame_superior = Frame(ventana_paquete3, bg=fondo2)
        frame_superior.pack(fill="both", expand=True)

        # Frame inferior
        frame_inferior = Frame(ventana_paquete3, bg=fondo2)
        frame_inferior.pack(fill="both", expand=True)

        # Título del paquete
        titulo = Label(frame_superior, text="Paquete Turístico: Aventura Total", font=("Calisto MT", 24, "bold"),
                       bg=fondo2)
        titulo.pack(pady=20)

        # Información general del paquete
        descripcion_paquete = Label(frame_superior, text="Explora destinos increíbles y disfruta actividades únicas.",
                                    font=("Arial", 14), bg=fondo2)
        descripcion_paquete.pack(pady=10)

        # Detalles de destinos incluidos
        titulo_destinos = Label(frame_inferior, text="Destinos incluidos:", font=("Arial", 16, "bold"), bg=fondo2)
        titulo_destinos.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        lista_destinos = Listbox(frame_inferior, height=5, width=50, font=("Arial", 12))
        lista_destinos.grid(row=1, column=0, padx=10, pady=5)
        for destino in self.destinos:
            lista_destinos.insert(END, destino)

        # Detalles de actividades incluidas
        titulo_actividades = Label(frame_inferior, text="Actividades incluidas:", font=("Arial", 16, "bold"), bg=fondo2)
        titulo_actividades.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        lista_actividades = Listbox(frame_inferior, height=5, width=50, font=("Arial", 12))
        lista_actividades.grid(row=3, column=0, padx=10, pady=5)
        for actividad in self.actividades:
            lista_actividades.insert(END, actividad)

        # Fechas específicas
        titulo_fechas = Label(frame_inferior, text="Fechas disponibles:", font=("Arial", 16, "bold"), bg=fondo2)
        titulo_fechas.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        lista_fechas = Listbox(frame_inferior, height=3, width=50, font=("Arial", 12))
        lista_fechas.grid(row=5, column=0, padx=10, pady=5)
        fechas_disponibles = ["15/06/2024", "01/07/2024", "15/07/2024"]
        for fecha in fechas_disponibles:
            lista_fechas.insert(END, fecha)

        # Precio total
        titulo_precio = Label(frame_inferior, text="Precio Total:", font=("Arial", 16, "bold"), bg=fondo2)
        titulo_precio.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        precio_total3 = Label(frame_inferior, text="$1500 USD", font=("Arial", 14), bg=fondo2, fg="green")
        precio_total3.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        # Botón cerrar ventana
        boton_cerrar = Button(frame_inferior, text="Cerrar", font=("Arial", 12), command=ventana_paquete3.destroy)
        boton_cerrar.grid(row=8, column=0, pady=20)

        ventana_paquete3.mainloop()



    ### Ventana para Reservar Paquete Turístico ###
    def reservar_paquete(self):
        reserva = Reserva()  # Crear una instancia de la clase Reserva
        ventana = Tk()
        ventana.geometry("400x450")
        ventana.title("Reservar Paquete Turístico")

        fondo3 = "#ff6347"

        # Configuración del frame
        frame = Frame(ventana, bg=fondo3)
        frame.pack(fill="both", expand=True)

        # Título
        titulo = Label(frame, text="Reservar Paquete Turístico", font=("Helvetica", 18, "bold"), bg=fondo3)
        titulo.pack(pady=10)

        # Entrada para RUT del cliente
        label_rut = Label(frame, text="RUT Cliente:", font=("Helvetica", 12), bg=fondo3)
        label_rut.pack(pady=5)

        entrada_rut = Entry(frame, font=("Helvetica", 12), width=30)
        entrada_rut.pack(pady=5)

        # Entrada para ID del paquete turístico
        label_paquete = Label(frame, text="ID Paquete Turístico:", font=("Helvetica", 12), bg=fondo3)
        label_paquete.pack(pady=5)

        entrada_paquete = Entry(frame, font=("Helvetica", 12), width=30)
        entrada_paquete.pack(pady=5)

        # Botón para crear la reserva
        boton_crear_reserva = Button(frame, text="Crear Reserva", font=("Helvetica", 14),
                                     command=lambda: [
                                         reserva.validar_y_guardar_reserva_paquete(entrada_rut.get(), entrada_paquete.get()),
                                         ventana.destroy()
                                        ]

                                     )
        boton_crear_reserva.pack(pady=20)

        ventana.mainloop()

    def v_mod_paquete_turistico(self, event=None):
        reserva = Reserva()
        ventana = Tk()
        ventana.geometry("400x550")  # Aumento el tamaño de la ventana para agregar más elementos
        ventana.title("Modificar Paquete Turístico")

        fondo3 = "#ff6347"

        # Configuración del frame
        frame = Frame(ventana, bg=fondo3)
        frame.pack(fill="both", expand=True)

        # Título
        titulo = Label(frame, text="Modificar Paquete Turístico", font=("Helvetica", 18, "bold"), bg=fondo3)
        titulo.pack(pady=10)

        # Entrada para ID de Paquete Turístico
        label_id_paquete = Label(frame, text="ID Paquete Turístico:", font=("Helvetica", 12), bg=fondo3)
        label_id_paquete.pack(pady=5)

        entrada_id_paquete = Entry(frame, font=("Helvetica", 12), width=30)
        entrada_id_paquete.pack(pady=5)

        # Entrada para nuevo nombre del destino
        label_destino = Label(frame, text="Nuevo Destino:", font=("Helvetica", 12), bg=fondo3)
        label_destino.pack(pady=5)

        entrada_destino = Entry(frame, font=("Helvetica", 12), width=30)
        entrada_destino.pack(pady=5)

        # Entrada para nueva fecha de ida
        label_fecha_ida = Label(frame, text="Nueva Fecha Ida (DD-MM-YYYY):", font=("Helvetica", 12), bg=fondo3)
        label_fecha_ida.pack(pady=5)

        entrada_fecha_ida = Entry(frame, font=("Helvetica", 12), width=30)
        entrada_fecha_ida.pack(pady=5)

        # Entrada para nueva fecha de vuelta
        label_fecha_vuelta = Label(frame, text="Nueva Fecha Vuelta (DD-MM-YYYY):", font=("Helvetica", 12), bg=fondo3)
        label_fecha_vuelta.pack(pady=5)

        entrada_fecha_vuelta = Entry(frame, font=("Helvetica", 12), width=30)
        entrada_fecha_vuelta.pack(pady=5)

        # Botón para modificar el paquete turístico
        boton_modificar_paquete = Button(
            frame, text="Modificar Paquete", font=("Helvetica", 14),
            command=lambda: reserva.modificar_paquete_turistico(
                entrada_id_paquete.get(), entrada_destino.get(), entrada_fecha_ida.get(), entrada_fecha_vuelta.get(),
                ventana
            )
        )
        boton_modificar_paquete.pack(pady=10)

        # Botón para eliminar el paquete turístico
        boton_eliminar_paquete = Button(
            frame, text="Eliminar Paquete", font=("Helvetica", 14), bg="red", fg="white",
            command=lambda: reserva.eliminar_paquete_turistico(entrada_id_paquete.get(), ventana)
        )
        boton_eliminar_paquete.pack(pady=10)

        ventana.mainloop()

# Crear la ventana de login
Login()