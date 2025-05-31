import tkinter as tk
from tkinter import ttk  # Para usar ComboBox
from tkinter import messagebox
from PIL import Image, ImageTk  # Manejo de imágenes con Pillow
import os

import random  # Importar random para la selección aleatoria

class ClueGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Clue")
        self.intentos = 0  # Contador de intentos

        # Activar pantalla completa
        self.root.attributes('-fullscreen', True)

        # Ruta relativa para las imágenes
        self.image_path = os.path.join(os.path.dirname(__file__), 'images')

        # Cargar y redimensionar imágenes
        self.load_and_resize_images()

        # Seleccionar un final aleatorio
        self.final_correcto = self.seleccionar_final_aleatorio()
        print(f"Final seleccionado: {self.final_correcto}")  # Imprimir el final en consola

        # Pantalla de introducción
        self.introduccion_screen()

    def seleccionar_final_aleatorio(self):
        """Selecciona aleatoriamente uno de los finales posibles."""
        finales = [
            ("Cruell De Ville", "Jardín de Loto", "Polvo Venenoso", self.final_polvo_cruell_lotos),
            ("Princesa Tiara", "Biblioteca Da Ville", "Pistola Láser", self.final_pistola_princesa_biblioteca),
            ("Alien Spoch", "Centro de Spoch", "Bastón de Pelea", self.final_baston_espoch_centro),
            ("Muñeco Falof", "Villa Invernal", "Lupa", self.final_lupa_falof_villa),
            ("Detective Mike", "Centro de Operaciones", "Pala", self.final_pala_centroop_mike)
        ]
        return random.choice(finales)

    def comprobar_adivinanza(self, personaje, lugar, arma):
        """Comprobar si la adivinanza es correcta y mostrar el final correspondiente."""
        personaje_correcto, lugar_correcto, arma_correcta, img_final = self.final_correcto

        if personaje == personaje_correcto and lugar == lugar_correcto and arma == arma_correcta:
            self.mostrar_final(img_final)
        else:
            self.mostrar_final_incorrecto()


    def load_and_resize_images(self):
        """Cargar y redimensionar imágenes al tamaño de la pantalla."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.introduccion_img = self.resize_image("intro.png", screen_width, screen_height)
        self.opciones_img = self.resize_image("opciones.png", screen_width, screen_height)
        self.armas_img = self.resize_image("armas.png", screen_width, screen_height)
        self.locaciones_img = self.resize_image("lugares.png", screen_width, screen_height)
        self.personajes_img = self.resize_image("personajes.png", screen_width, screen_height)

        # Imágenes de pistas
        self.pista_baston_mike_villa = self.resize_image("pista_baston_mike_villa.png", screen_width, screen_height)
        self.pista_lupa_princesa_centroop = self.resize_image("pista_lupa_princesa_centroop.png", screen_width, screen_height)
        self.pista_pala_espoch_biblioteca = self.resize_image("pista_pala_espoch_biblioteca.png", screen_width, screen_height)
        self.pista_pistola_princesa_centro = self.resize_image("pista_pistola_princesa_centro.png", screen_width, screen_height)
        self.pista_polvo_falof_loto = self.resize_image("pista_polvo_falof_loto.png", screen_width, screen_height)

        # Imágenes de final
        self.final_polvo_cruell_lotos = self.resize_image("final_polvo_cruell_lotos.png", screen_width, screen_height)
        self.final_baston_espoch_centro = self.resize_image("final_baston_espoch_centro.png", screen_width, screen_height)
        self.final_lupa_falof_villa = self.resize_image("final_lupa_falof_villa.png", screen_width, screen_height)
        self.final_pala_centroop_mike = self.resize_image("final_pala_centroop_mike.png", screen_width, screen_height)
        self.final_pistola_princesa_biblioteca = self.resize_image("final_pistola_princesa_biblioteca.png", screen_width, screen_height)


    def resize_image(self, filename, width, height):
        """Redimensionar una imagen con Pillow."""
        path = os.path.join(self.image_path, filename)
        img = Image.open(path)
        img = img.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def introduccion_screen(self):
        """Pantalla inicial."""
        self.clear_window()

        label = tk.Label(self.root, image=self.introduccion_img)
        label.place(relwidth=1, relheight=1)

        boton = tk.Button(self.root, text="Resolver misterio", command=self.menu_opciones)
        boton.place(relx=0.5, rely=0.8, anchor='center', x=0, y=130)

    def menu_opciones(self):
        """Menú principal de opciones."""
        self.clear_window()
        label = tk.Label(self.root, image=self.opciones_img)
        label.place(relwidth=1, relheight=1)

        self.crear_boton("Personajes", self.personajes_screen, 0.15, 0.8)
        self.crear_boton("Lugares", self.locaciones_screen, 0.5, 0.8)
        self.crear_boton("Armas", self.armas_screen, 0.83, 0.8)

    def crear_boton(self, texto, comando, relx, rely):
        """Crea un botón en una posición específica."""
        tk.Button(self.root, text=texto, command=comando).place(
            relx=relx, rely=rely, anchor='center'
        )

    def armas_screen(self):
        """Pantalla de selección de armas."""
        self.clear_window()
        label = tk.Label(self.root, image=self.armas_img)
        label.place(relwidth=1, relheight=1)

        self.crear_boton("Polvo Venenoso", lambda: self.mostrar_pista(self.pista_polvo_falof_loto), 0.165, 0.50)
        self.crear_boton("Pala de Falof", lambda: self.mostrar_pista(self.pista_pala_espoch_biblioteca), 0.5, 0.50)
        self.crear_boton("Bastón de pelea", lambda: self.mostrar_pista(self.pista_baston_mike_villa), 0.83, 0.50)
        self.crear_boton("Lupa", lambda: self.mostrar_pista(self.pista_lupa_princesa_centroop), 0.28, 0.95)
        self.crear_boton("Pistola Láser", lambda: self.mostrar_pista(self.pista_pistola_princesa_centro), 0.735, 0.95)

    def locaciones_screen(self):
        """Pantalla de selección de locaciones."""
        self.clear_window()
        label = tk.Label(self.root, image=self.locaciones_img)
        label.place(relwidth=1, relheight=1)

        self.crear_boton("Villa Invernal", lambda: self.mostrar_pista(self.pista_baston_mike_villa), 0.165, 0.50)
        self.crear_boton("Centro de Operaciones", lambda: self.mostrar_pista(self.pista_lupa_princesa_centroop), 0.5, 0.50)
        self.crear_boton("Jardín de Loto", lambda: self.mostrar_pista(self.pista_polvo_falof_loto), 0.83, 0.50)
        self.crear_boton("Biblioteca Da Ville", lambda: self.mostrar_pista(self.pista_pala_espoch_biblioteca), 0.28, 0.95)
        self.crear_boton("Centro de Spoch", lambda: self.mostrar_pista(self.pista_pistola_princesa_centro), 0.735, 0.95)

    def personajes_screen(self):
        """Pantalla de selección de personajes."""
        self.clear_window()
        label = tk.Label(self.root, image=self.personajes_img)
        label.place(relwidth=1, relheight=1)

        self.crear_boton("Princesa Tiara", lambda: self.mostrar_pista(self.pista_lupa_princesa_centroop), 0.165, 0.50)
        self.crear_boton("Detective Mike", lambda: self.mostrar_pista(self.pista_baston_mike_villa), 0.5, 0.50)
        self.crear_boton("Alien Spoch", lambda: self.mostrar_pista(self.pista_pala_espoch_biblioteca), 0.83, 0.50)
        self.crear_boton("Muñeco Falof", lambda: self.mostrar_pista(self.pista_polvo_falof_loto), 0.28, 0.95)
        self.crear_boton("Cruell De Ville", lambda: self.mostrar_pista(self.pista_baston_mike_villa), 0.735, 0.95)

    def mostrar_pista(self, pista_img):
        """Mostrar la pista seleccionada."""
        self.clear_window()
        label = tk.Label(self.root, image=pista_img)
        label.place(relwidth=1, relheight=1)

        if self.intentos < 2:
            boton = tk.Button(self.root, text="Continuar", command=self.menu_opciones)
        else:
            boton = tk.Button(self.root, text="Adivinar", command=self.adivinanza_final)

        boton.place(relx=0.5, rely=0.8, anchor='center', x=0, y=130)
        self.intentos += 1


    def adivinanza_final(self):
        """Pantalla para adivinar al culpable."""
        self.clear_window()

        # Cargar la imagen de fondo
        fondo_path = os.path.join(self.image_path, "FondoCLue.png")
        fondo_img = self.resize_image(fondo_path, self.root.winfo_screenwidth(), self.root.winfo_screenheight())

        fondo_label = tk.Label(self.root, image=fondo_img)
        fondo_label.image = fondo_img  # Mantener referencia para evitar recolección de basura
        fondo_label.place(relwidth=1, relheight=1)  # Expandir al tamaño completo

        frame = tk.Frame(self.root, bg='')
        frame.place(relx=0.5, rely=0.5, anchor='center')

        # Crear ComboBoxes con imágenes interactivas
        self.crear_seccion(frame, "personaje_unknown.png", 
                        ["Princesa Tiara", "Detective Mike", "Alien Spoch", "Muñeco Falof", "Cruell De Ville"], 
                        "personaje_combobox")
        self.crear_seccion(frame, "arma_unknown.png", 
                        ["Pistola Láser", "Polvo Venenoso", "Bastón de pelea", "Lupa", "Pala"], 
                        "arma_combobox")
        self.crear_seccion(frame, "lugar_unknown.png", 
                        ["Villa Invernal", "Centro de Operaciones", "Jardín de Loto", "Biblioteca Da Ville", "Centro de Spoch"], 
                        "lugar_combobox")

        # Botón para confirmar la adivinanza
        confirmar_btn = tk.Button(self.root, text="Confirmar Adivinanza", command=self.confirmar_adivinanza)
        confirmar_btn.place(relx=0.5, rely=0.85, anchor='center')

    def confirmar_adivinanza(self):
        """Recupera la selección y comprueba la adivinanza."""
        # Obtener las opciones seleccionadas por el usuario
        personaje = self.personaje_combobox.get()
        arma = self.arma_combobox.get()
        lugar = self.lugar_combobox.get()

        # Llamar a comprobar_adivinanza con los valores seleccionados
        self.comprobar_adivinanza(personaje, lugar, arma)

    def crear_seccion(self, parent, img_path, opciones, combobox_attr):
        """Crea una sección con una imagen interactiva y un ComboBox."""
        # Frame interno para la distribución vertical de imagen y ComboBox
        seccion_frame = tk.Frame(parent)
        seccion_frame.pack(side=tk.LEFT, padx=10)

        # Cargar imagen inicial y mostrarla en una etiqueta
        img = self.resize_image(img_path, 200, 200)
        img_label = tk.Label(seccion_frame, image=img)
        img_label.image = img  # Mantener referencia para evitar recolección de basura
        img_label.pack(pady=5)

        # Crear ComboBox y enlazar evento de selección
        combobox = ttk.Combobox(seccion_frame, values=opciones, state="readonly")
        combobox.current(0)  # Opción por defecto
        combobox.pack(pady=5)

        # Asociar el ComboBox con su atributo para uso posterior
        setattr(self, combobox_attr, combobox)

        # Enlazar selección del ComboBox para actualizar la imagen
        combobox.bind("<<ComboboxSelected>>", lambda event: self.update_image(combobox, img_label, opciones))

    def update_image(self, combobox, img_label, opciones):
        """Actualiza la imagen según la opción seleccionada en el ComboBox."""
        opcion = combobox.get()

        # Mapeo de opciones a archivos de imagen
        filename_map = {
            "Princesa Tiara": "personaje_princesa.png",
            "Detective Mike": "personaje_mike.png",
            "Alien Spoch": "personaje_spoch.png",
            "Muñeco Falof": "personaje_falof.png",
            "Cruell De Ville": "personaje_cruell.png",
            "Pistola Láser": "arma_pistolal.png",
            "Polvo Venenoso": "arma_polvo.png",
            "Bastón de pelea": "arma_baston.png",
            "Lupa": "arma_lupa.png",
            "Pala": "arma_pala.png",
            "Villa Invernal": "lugar_villa.png",
            "Centro de Operaciones": "lugar_centroop.png",
            "Jardín de Loto": "lugar_jardinloto.png",
            "Biblioteca Da Ville": "lugar_biblioteca.png",
            "Centro de Spoch": "lugar_centrospoch.png",
        }

        # Cargar y actualizar la imagen seleccionada
        img_path = os.path.join(self.image_path, filename_map.get(opcion, "unknown.png"))
        new_img = self.resize_image(img_path, 200, 200)

        img_label.config(image=new_img)
        img_label.image = new_img  # Mantener referencia para evitar recolección de basura

    def create_combobox(self, parent, values):
        """Crea y devuelve un ComboBox."""
        combobox = ttk.Combobox(parent, values=values, state="readonly")
        combobox.current(0)  # Establece la opción por defecto en la primera
        combobox.pack(pady=5)
        return combobox


    def mostrar_final(self, final_img):
        """Mostrar la pantalla del final correcto con la imagen como fondo."""
        self.clear_window()

        # Mostrar la imagen como fondo en un Label
        fondo_label = tk.Label(self.root, image=final_img)
        fondo_label.place(relwidth=1, relheight=1)  # Expandir para cubrir toda la ventana
        fondo_label.image = final_img  # Referencia para evitar recolección de basura

        # Botón para reiniciar el juego
        boton_reiniciar = tk.Button(self.root, text="Reiniciar", 
                                    command=self.introduccion_screen, width=10)
        boton_reiniciar.place(x=200, y=800)  # Ajusta la posición con coordenadas exactas

        # Botón para salir del juego
        boton_salir = tk.Button(self.root, text="Salir", 
                                command=self.root.quit, width=10)
        boton_salir.place(x=350, y=800)  # Ajusta la posición con coordenadas exactas



    def mostrar_final_incorrecto(self):
        """Mostrar mensaje de intento fallido."""
        self.clear_window()

        # Mensaje de fracaso
        label_text = tk.Label(self.root, text="Intento fallido. ¿Quieres intentarlo de nuevo?", 
                            wraplength=600, justify='center', bg="#2C2C2C", fg="white")
        label_text.place(relx=0.5, rely=0.4, anchor='center')

        # Botón para reiniciar el juego
        boton_reiniciar = tk.Button(self.root, text="Reiniciar", 
                                    command=self.introduccion_screen)
        boton_reiniciar.place(relx=0.4, rely=0.6, anchor='center')

        # Botón para salir del juego
        boton_salir = tk.Button(self.root, text="Salir", command=self.root.quit)
        boton_salir.place(relx=0.6, rely=0.6, anchor='center')



    def clear_window(self):
        """Limpia la ventana actual."""
        for widget in self.root.winfo_children():
            widget.destroy()

# Inicializar la ventana principal
root = tk.Tk()
app = ClueGame(root)
root.mainloop()
