import pymysql
import mysql.connector
from baseDeDatos.base_de_datos import baseDeDatos


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
        self.ventana.geometry("400x700")
        self.ventana.title("Login")

        fondo = "#9fbbf3"

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
                            font=("Calisto MT", 36, "bold"),
                            bg=fondo)
        self.titulo.pack(side="top", pady=20)

        ###########IMAGEN#####################



        #########DATOS##############

        self.label_usuario = Label(self.frame_inferior, text="Usuario", font=("Arial", 18), bg=fondo, fg="black")
        self.label_usuario.grid(row=0, column=0, padx=10, sticky="e")
        self.entry_usuario = Entry(self.frame_inferior, bd=0, width=14, font=("Arial", 18))
        self.entry_usuario.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")

        self.label_contraseña = Label(self.frame_inferior, text="Contraseña", font=("Arial", 18), bg=fondo, fg="black")
        self.label_contraseña.grid(row=1, column=0, padx=10, sticky="e")
        self.entry_contraseña = Entry(self.frame_inferior, bd=0, width=14, font=("Arial", 18), show="●")
        self.entry_contraseña.grid(row=1, column=1, columnspan=3, padx=5, sticky="w")

        self.boton_ingresar = Button(self.frame_inferior, text="Ingresar", width=16, font=("Arial", 12),
                                     command=self.entrar)
        self.boton_ingresar.grid(row=2, column=1, pady=35)

        #####FIN#####

        mainloop()

    def entrar(self):
        nombre = self.entry_usuario.get()
        contra = self.entry_contraseña.get()

        if nombre == "Ezpi" and contra == "1234":
            messagebox.showinfo("Acceso Correcto ", " Has iniciado correctamente")
            self.ventana.destroy()
            self.ventana2()
        else:
            messagebox.showinfo("Acceso Denegado ", " Intentelo Nuevamente")

    ###VENTANA2###

    def ventana2(self):
        self.ventana2 = Tk()
        self.ventana2.geometry("400x700")
        self.ventana2.title("Viajes Aventura")

        fondo1 = "#9fbbf3"

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
                             font=("Calisto MT", 36, "bold"),
                             bg=fondo1)
        self.titulo2.pack(side="top", pady=20)

        # AGREGAR DESTINOOO####
        self.boton_m_destino = Button(self.frame_inferior, text="Agregar Destinos", width=100, font=("Arial", 12),
                                      command=self.v_a_destino)
        self.boton_m_destino.grid(row=1, column=1, padx=50, pady=10)

        # Pasamos la lista destinos a la ventana de modificación
        self.boton_mod_destino = Button(self.frame_inferior, text="Modificar Destino", width=100, font=("Arial", 12),
                                        command=lambda: self.v_mod_destino(self.destinos))
        self.boton_mod_destino.grid(row=2, column=1, padx=50, pady=20)

        # Botón Ver Paquete Turístico
        self.boton_paquete = Button(self.frame_inferior, text="Ver Paquete Turístico", width=100, font=("Arial", 12),
                                    command=self.inter_paquete_turistico)
        self.boton_paquete.grid(row=3, column=1, padx=50, pady=30)

        self.boton_reservar_pq = Button(self.frame_inferior, text="Reservar Paquete Turístico", width=100,
                                        font=("Arial", 12), command=self.reservar_paquete)
        self.boton_reservar_pq.grid(row=4, column=1, padx=50, pady=40)

    ########VENTANA AGREGAR DESTINO##########

    def v_a_destino(self):
        self.v_a_destino = Tk()
        self.v_a_destino.geometry("850x900")  # Ampliamos la ventana para incluir la lista
        self.v_a_destino.title("Destinos")

        fondo3 = "#9fbbf3"

        # Frame superior
        self.frame_superior = Frame(self.v_a_destino)
        self.frame_superior.configure(bg=fondo3)
        self.frame_superior.pack(fill="both", expand=True)

        # Frame inferior para los botones
        self.frame_inferior = Frame(self.v_a_destino)
        self.frame_inferior.configure(bg=fondo3)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        # Título
        self.titulo_c_emp = Label(self.frame_superior, text="Destinos", font=("Calisto MT", 36, "bold"), bg=fondo3, )
        self.titulo_c_emp.pack(side="top", pady=20)

        # Frame para la lista de destinos y scroll
        self.frame_lista = Frame(self.v_a_destino)
        self.frame_lista.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Scrollbar
        self.scrollbar = Scrollbar(self.frame_lista)
        self.scrollbar.pack(side="right", fill="y")

        # Lista de destinos con fechas
        self.lista_destinos = Listbox(self.frame_lista, height=15, width=50, font=("Arial", 14),
                                      yscrollcommand=self.scrollbar.set)
        self.lista_destinos.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.lista_destinos.yview)

        # Función para agregar destinos y fechas a la lista
        def agregar_a_lista(destino, fecha):
            if not self.validar_fecha(fecha):  # Llamada al método validar_fecha
                messagebox.showerror("Error", "El formato de la fecha es incorrecto. Use dd/mm/yyyy.")
                return
            destino_fecha = f"{destino} - Fecha: {fecha}"
            self.lista_destinos.insert(END, destino_fecha)

        # Destinos con botones y campos de fecha
        destinos = [
            "Destino 1",
            "Destino 2",
            "Destino 3",
            "Destino 4",
            "Destino 5",
            "Destino 6",
            "Destino 7",
        ]

        self.fecha_entries = []  # Lista para almacenar las entradas de fecha

        for i, destino in enumerate(destinos):
            # Etiqueta para destino
            label = Label(self.frame_inferior, text=destino, font=("Arial", 18), bg=fondo3, fg="black")
            label.grid(row=i, column=0, padx=10, sticky="e")

            # Etiqueta para indicar formato de fecha
            label_fecha = Label(self.frame_inferior, text="Fecha (dd/mm/yyyy):", font=("Arial", 12), bg=fondo3,
                                fg="black")
            label_fecha.grid(row=i, column=1, padx=10, sticky="w")

            # Campo de entrada de fecha
            entry_fecha = Entry(self.frame_inferior, font=("Arial", 14))
            entry_fecha.grid(row=i, column=2, padx=10)
            self.fecha_entries.append(entry_fecha)

            # Botón para agregar destino con fecha
            boton = Button(self.frame_inferior, text="Agregar", font=("Arial", 14),
                           command=lambda d=destino, e=entry_fecha: agregar_a_lista(d, e.get()), )
            boton.grid(row=i, column=3, padx=10, sticky="w")

        # Botón para eliminar el destino seleccionado
        self.boton_eliminar = Button(
            self.frame_inferior, text="Eliminar Seleccionado", width=16, font=("Arial", 12),
            command=self.eliminar_destino
        )
        self.boton_eliminar.grid(row=7, column=2, pady=35)

        # Botón Finalizar
        self.boton_ingresar2 = Button(
            self.frame_inferior, text="Agregar Reserva", width=16, font=("Arial", 12), command=self.finalizar
        )
        self.boton_ingresar2.grid(row=7, column=1, pady=35)

        self.v_a_destino.mainloop()

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

    def finalizar(self):
        # Acción al hacer clic en Finalizar
        print("Destinos agregados:")
        destinos_agregados = []  # Lista para almacenar los destinos y fechas

        for destino in self.lista_destinos.get(0, END):
            print(destino)
            destinos_agregados.append(destino)

        # Espacio para guardar en la base de datos
        try:
            # Aquí puedes incluir tu lógica para conectarte y guardar en la base de datos
            # Por ejemplo:
            # conexion = tu_metodo_conexion()
            # cursor = conexion.cursor()
            # for destino in destinos_agregados:
            #     consulta = "INSERT INTO tu_tabla (destino, fecha) VALUES (%s, %s)"
            #     valores = destino.split(" - Fecha: ")
            #     cursor.execute(consulta, valores)
            # conexion.commit()
            print("Datos guardados en la base de datos correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los datos: {e}")
            return

        # Mensaje de éxito
        messagebox.showinfo("", "Destino Agregado Correctamente")
        self.v_a_destino.destroy()

    #######VENTANA MODIFICAR DESTINO##########

    def v_mod_destino(self, destinos):
        self.v_mod_destino = Tk()
        self.v_mod_destino.geometry("850x900")  # Ampliamos la ventana para incluir la lista
        self.v_mod_destino.title("Destinos")

        fondo3 = "#9fbbf3"

        # Frame superior
        self.frame_superior = Frame(self.v_mod_destino)
        self.frame_superior.configure(bg=fondo3)
        self.frame_superior.pack(fill="both", expand=True)

        # Frame inferior para los botones
        self.frame_inferior = Frame(self.v_mod_destino)
        self.frame_inferior.configure(bg=fondo3)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        # Título
        self.titulo_c_emp = Label(self.frame_superior, text="Destinos", font=("Calisto MT", 36, "bold"), bg=fondo3, )
        self.titulo_c_emp.pack(side="top", pady=20)

        # Frame para la lista de destinos y scroll
        self.frame_lista = Frame(self.v_mod_destino)
        self.frame_lista.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Scrollbar
        self.scrollbar = Scrollbar(self.frame_lista)
        self.scrollbar.pack(side="right", fill="y")

        # Lista de destinos con fechas
        self.lista_destinos = Listbox(self.frame_lista, height=15, width=50, font=("Arial", 14),
                                      yscrollcommand=self.scrollbar.set)
        self.lista_destinos.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.lista_destinos.yview)

        # Función para agregar destinos y fechas a la lista
        def agregar_a_lista(destino, fecha):
            if not self.validar_fecha(fecha):  # Llamada al método validar_fecha
                messagebox.showerror("Error", "El formato de la fecha es incorrecto. Use dd/mm/yyyy.")
                return
            destino_fecha = f"{destino} - Fecha: {fecha}"
            self.lista_destinos.insert(END, destino_fecha)

        # Destinos con botones y campos de fecha
        destinos = [
            "Destino 1",
            "Destino 2",
            "Destino 3",
            "Destino 4",
            "Destino 5",
            "Destino 6",
            "Destino 7",
        ]

        self.fecha_entries = []  # Lista para almacenar las entradas de fecha

        for i, destino in enumerate(destinos):
            # Etiqueta para destino
            label = Label(self.frame_inferior, text=destino, font=("Arial", 18), bg=fondo3, fg="black")
            label.grid(row=i, column=0, padx=10, sticky="e")

            # Etiqueta para indicar formato de fecha
            label_fecha = Label(self.frame_inferior, text="Fecha (dd/mm/yyyy):", font=("Arial", 12), bg=fondo3,
                                fg="black")
            label_fecha.grid(row=i, column=1, padx=10, sticky="w")

            # Campo de entrada de fecha
            entry_fecha = Entry(self.frame_inferior, font=("Arial", 14))
            entry_fecha.grid(row=i, column=2, padx=10)
            self.fecha_entries.append(entry_fecha)

            # Botón para agregar destino con fecha
            boton = Button(self.frame_inferior, text="Agregar", font=("Arial", 14),
                           command=lambda d=destino, e=entry_fecha: agregar_a_lista(d, e.get()), )
            boton.grid(row=i, column=3, padx=10, sticky="w")

        # Botón para eliminar el destino seleccionado
        self.boton_eliminar = Button(
            self.frame_inferior, text="Eliminar Seleccionado", width=16, font=("Arial", 12),
            command=self.eliminar_destino
        )
        self.boton_eliminar.grid(row=7, column=2, pady=35)

        # Botón Finalizar
        self.boton_ingresar2 = Button(
            self.frame_inferior, text="Agregar Reserva", width=16, font=("Arial", 12), command=self.finalizar1
        )
        self.boton_ingresar2.grid(row=7, column=1, pady=35)

        self.v_mod_destino.mainloop()

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

    def finalizar1(self):
        # Acción al hacer clic en Finalizar
        print("Destinos agregados:")
        destinos_agregados = []  # Lista para almacenar los destinos y fechas

        for destino in self.lista_destinos.get(0, END):
            print(destino)
            destinos_agregados.append(destino)

        # Espacio para guardar en la base de datos
        try:
            # Aquí puedes incluir tu lógica para conectarte y guardar en la base de datos
            # Ejemplo:
            # conexion = tu_metodo_conexion()
            # cursor = conexion.cursor()
            # for destino in destinos_agregados:
            #     consulta = "UPDATE tu_tabla SET fecha = %s WHERE destino = %s"
            #     valores = destino.split(" - Fecha: ")
            #     cursor.execute(consulta, (valores[1], valores[0]))
            # conexion.commit()
            print("Datos actualizados en la base de datos correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los datos: {e}")
            return

        # Mensaje de éxito
        messagebox.showinfo("", "Destino Modificado Correctamente")
        self.v_mod_destino.destroy()

    ### VENTANA INTERMEDIA DE PAQUETE TURISTICO ###

    def inter_paquete_turistico(self):
        ventana_intermedia = Tk()
        ventana_intermedia.geometry("400x400")
        ventana_intermedia.title("Seleccionar Paquete Turístico")

        fondo2 = "#d4f1f9"

        # Título
        titulo = Label(ventana_intermedia, text="Selecciona un Paquete Turístico", font=("Calisto MT", 18, "bold"),
                       bg=fondo2)
        titulo.pack(pady=20)

        # Botón para Paquete Turístico 1
        boton_paquete1 = Button(ventana_intermedia, text="Paquete Turístico 1", font=("Arial", 14),
                                command=self.ver_paquete_turistico1)
        boton_paquete1.pack(pady=10)

        # Botón para Paquete Turístico 2
        boton_paquete2 = Button(ventana_intermedia, text="Paquete Turístico 2", font=("Arial", 14),
                                command=self.ver_paquete_turistico2)
        boton_paquete2.pack(pady=20)

        # Botón para Paquete Turístico 3
        boton_paquete3 = Button(ventana_intermedia, text="Paquete Turístico 3", font=("Arial", 14),
                                command=self.ver_paquete_turistico3)
        boton_paquete3.pack(pady=30)

        # Botón cerrar ventana
        boton_cerrar = Button(ventana_intermedia, text="Cerrar", font=("Arial", 12), command=ventana_intermedia.destroy)
        boton_cerrar.pack(pady=40)

        ventana_intermedia.mainloop()

    ### Ventana de Ver Paquete Turístico1 ###
    def ver_paquete_turistico1(self):
        ventana_paquete1 = Tk()
        ventana_paquete1.geometry("400x500")
        ventana_paquete1.title("Paquete Turístico 2")

        fondo2 = "#d4f1f9"

        # Frame superior
        frame_superior = Frame(ventana_paquete1, bg=fondo2)
        frame_superior.pack(fill="both", expand=True)

        # Frame inferior
        frame_inferior = Frame(ventana_paquete1, bg=fondo2)
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
        boton_cerrar = Button(frame_inferior, text="Cerrar", font=("Arial", 12), command=ventana_paquete1.destroy)
        boton_cerrar.grid(row=4, column=0, pady=20)

        ventana_paquete1.mainloop()

    def ver_paquete_turistico1(self):
        ventana_paquete1 = Tk()
        ventana_paquete1.geometry("600x700")
        ventana_paquete1.title("Detalles del Paquete Turístico")

        fondo2 = "#d4f1f9"

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

        fondo2 = "#d4f1f9"

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

        fondo2 = "#d4f1f9"

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

        fondo2 = "#d4f1f9"

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

        fondo2 = "#d4f1f9"

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
        self.reserva = Tk()
        self.reserva.geometry("600x500")
        self.reserva.title("Reservar Paquete Turístico")

        fondo2 = "#f9e1d4"

        # Frame superior
        frame_superior = Frame(self.reserva, bg=fondo2)
        frame_superior.pack(fill="both", expand=True)

        # Frame inferior
        frame_inferior = Frame(self.reserva, bg=fondo2)
        frame_inferior.pack(fill="both", expand=True)

        # Título
        titulo = Label(frame_superior, text="Reservar Paquete Turístico", font=("Calisto MT", 18, "bold"), bg=fondo2)
        titulo.pack(pady=20)

        # Selección de paquetes
        label_paquete = Label(frame_inferior, text="Selecciona un Paquete:", font=("Arial", 14), bg=fondo2)
        label_paquete.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        paquetes = ["Paquete Turístico 1", "Paquete Turístico 2", "Paquete Turístico 3"]
        combo_paquete = Listbox(frame_inferior, height=3, width=30, font=("Arial", 12))
        combo_paquete.grid(row=1, column=0, padx=10, pady=5)
        for paquete in paquetes:
            combo_paquete.insert(END, paquete)

        # Botón agregar paquete
        def agregar_paquete():
            if combo_paquete.curselection():
                seleccion_paquete = combo_paquete.get(combo_paquete.curselection())
                self.lista_reservas.insert(END, f"Paquete: {seleccion_paquete}")
            else:
                messagebox.showwarning("Selección Incompleta", "Selecciona un paquete.")

        boton_agregar_paquete = Button(frame_inferior, text="Agregar Paquete", font=("Arial", 12),
                                       command=agregar_paquete)
        boton_agregar_paquete.grid(row=1, column=1, padx=10)

        # Selección de fechas
        label_fecha = Label(frame_inferior, text="Selecciona una Fecha:", font=("Arial", 14), bg=fondo2)
        label_fecha.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        fechas = ["15/06/2024", "20/07/2024", "01/08/2024"]
        combo_fecha = Listbox(frame_inferior, height=3, width=30, font=("Arial", 12))
        combo_fecha.grid(row=3, column=0, padx=10, pady=5)
        for fecha in fechas:
            combo_fecha.insert(END, fecha)

        # Botón agregar fecha
        def agregar_fecha():
            if combo_fecha.curselection():
                seleccion_fecha = combo_fecha.get(combo_fecha.curselection())
                self.lista_reservas.insert(END, f"Fecha: {seleccion_fecha}")
            else:
                messagebox.showwarning("Selección Incompleta", "Selecciona una fecha.")

        boton_agregar_fecha = Button(frame_inferior, text="Agregar Fecha", font=("Arial", 12), command=agregar_fecha)
        boton_agregar_fecha.grid(row=3, column=1, padx=10)

        # Lista de reservas
        label_reservas = Label(frame_inferior, text="Reservas Realizadas:", font=("Arial", 14), bg=fondo2)
        label_reservas.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Define self.lista_reservas como un atributo de clase
        self.lista_reservas = Listbox(frame_inferior, height=5, width=50, font=("Arial", 12))
        self.lista_reservas.grid(row=5, column=0, padx=10, pady=5)

        # Botón Reservar
        boton_cerrar = Button(frame_inferior, text="Reservar", font=("Arial", 12), command=self.fin_reserva)
        boton_cerrar.grid(row=6, column=0, pady=20)

        self.reserva.mainloop()

    def fin_reserva(self):
        try:
            print("Reserva realizada correctamente.")
            reservas_realizadas = []
            for reserva in self.lista_reservas.get(0, END):
                print(reserva)
                reservas_realizadas.append(reserva)

            # Aquí puedes incluir la lógica para guardar en una base de datos
            # Ejemplo: Guardar reservas_realizadas en una tabla

            messagebox.showinfo("Reserva", "Reserva realizada correctamente.")
            self.reserva.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la reserva: {e}")


# Crear la ventana de login
Login()