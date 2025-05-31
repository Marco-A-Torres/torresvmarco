import tkinter as tk
from tkinter import PhotoImage, messagebox
import os

class ClueGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Clue")
        self.intentos = 0

        # Ruta relativa hacia la carpeta de imágenes
        self.image_path = os.path.join(os.path.dirname(__file__), 'images')

        # Cargar imágenes usando rutas relativas
        self.introduccion_img = PhotoImage(file=os.path.join(self.image_path, "Introducción.jpg"))
        self.opciones_img = PhotoImage(file=os.path.join(self.image_path, "Opciones.jpg"))
        self.armas_img = PhotoImage(file=os.path.join(self.image_path, "Armas.jpg"))
        self.locaciones_img = PhotoImage(file=os.path.join(self.image_path, "Locaciones.jpg"))
        self.personajes_img = PhotoImage(file=os.path.join(self.image_path, "Personajes.jpg"))

        # Pantalla de introducción
        self.introduccion_screen()

    def introduccion_screen(self):
        """Pantalla inicial con la historia de introducción."""
        self.clear_window()
        label = tk.Label(self.root, image=self.introduccion_img)
        label.pack()

        boton = tk.Button(self.root, text="Continuar", command=self.menu_opciones)
        boton.pack(pady=10)

    def menu_opciones(self):
        """Menú para elegir entre preguntas: armas, lugares o personajes."""
        self.clear_window()
        label = tk.Label(self.root, image=self.opciones_img)
        label.pack()

        # Botones de opciones
        tk.Button(self.root, text="Armas", command=self.armas_screen).pack(pady=5)
        tk.Button(self.root, text="Lugares", command=self.locaciones_screen).pack(pady=5)
        tk.Button(self.root, text="Personajes", command=self.personajes_screen).pack(pady=5)

    def armas_screen(self):
        """Pantalla con las opciones de armas."""
        self.clear_window()
        label = tk.Label(self.root, image=self.armas_img)
        label.pack()

        # Opciones de armas con historias fijas
        for i in range(1, 6):
            tk.Button(self.root, text=f"Arma {i}", 
                      command=lambda i=i: self.mostrar_historia(f"Historia sobre el Arma {i}")).pack(pady=5)

    def locaciones_screen(self):
        """Pantalla con las opciones de locaciones."""
        self.clear_window()
        label = tk.Label(self.root, image=self.locaciones_img)
        label.pack()

        # Opciones de locaciones con historias fijas
        for i in range(1, 6):
            tk.Button(self.root, text=f"Lugar {i}", 
                      command=lambda i=i: self.mostrar_historia(f"Historia sobre el Lugar {i}")).pack(pady=5)

    def personajes_screen(self):
        """Pantalla con las opciones de personajes."""
        self.clear_window()
        label = tk.Label(self.root, image=self.personajes_img)
        label.pack()

        # Opciones de personajes con historias fijas
        for i in range(1, 6):
            tk.Button(self.root, text=f"Personaje {i}", 
                      command=lambda i=i: self.mostrar_historia(f"Historia sobre el Personaje {i}")).pack(pady=5)

    def mostrar_historia(self, historia):
        """Muestra una historia fija al seleccionar una opción."""
        if self.intentos < 3:
            self.intentos += 1
            messagebox.showinfo("Historia", historia)
            self.menu_opciones()
        else:
            messagebox.showinfo("Intentos agotados", "Has usado tus 3 preguntas. Adivina el culpable.")
            self.adivinanza_final()

    def adivinanza_final(self):
        """Pantalla de adivinanza final."""
        self.clear_window()
        tk.Label(self.root, text="¿Quién es el culpable?").pack(pady=10)

        # Opciones para la adivinanza final (5 finales fijos)
        for i in range(1, 6):
            tk.Button(self.root, text=f"Final {i}", 
                      command=lambda i=i: self.mostrar_final(f"Este es el final {i}.")).pack(pady=5)

    def mostrar_final(self, final):
        """Muestra uno de los cinco finales fijos."""
        messagebox.showinfo("Final del juego", final)
        self.introduccion_screen()  # Reinicia el juego

    def clear_window(self):
        """Limpia la ventana actual."""
        for widget in self.root.winfo_children():
            widget.destroy()

# Inicializar la ventana principal
root = tk.Tk()
app = ClueGame(root)
root.mainloop()
