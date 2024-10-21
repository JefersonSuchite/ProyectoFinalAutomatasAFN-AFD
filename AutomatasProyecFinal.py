import tkinter as tk  # Importa la biblioteca tkinter para crear interfaces gráficas.
from tkinter import ttk, scrolledtext, filedialog, messagebox  # Importa widgets específicos de tkinter.
import re  # Importa la biblioteca de expresiones regulares.
from collections import deque  # Importa deque para estructuras de datos de cola.
import os  # Importa la biblioteca para operaciones del sistema.

class Automata:
    def __init__(self):
        # Inicializa el autómata con estados, estado inicial, estados finales, alfabeto y transiciones.
        self.states = set()  # Conjunto para almacenar los estados del autómata.
        self.initial_state = set()  # Conjunto para almacenar el estado inicial.
        self.final_states = set()  # Conjunto para almacenar los estados finales.
        self.alphabet = set()  # Conjunto para almacenar el alfabeto del autómata.
        self.transitions = {}  # Diccionario para almacenar las transiciones entre estados.

    def add_transition(self, state, symbol, next_states):
        # Añade una transición entre un estado y un símbolo a uno o más estados siguientes.
        if state not in self.transitions:  # Si el estado no tiene transiciones, inicializa su entrada.
            self.transitions[state] = {}
        self.transitions[state][symbol] = set(next_states)  # Añade el símbolo y los siguientes estados.

    def epsilon_closure(self, states):
        # Calcula el cierre épsilon de un conjunto de estados.
        closure = set(states)  # Crea un conjunto inicial con los estados proporcionados.
        stack = list(states)  # Crea una pila con los estados para procesarlos.
        while stack:  # Mientras haya estados en la pila.
            state = stack.pop()  # Extrae un estado de la pila.
            if state in self.transitions and '$' in self.transitions[state]:  # Si hay transiciones épsilon.
                for next_state in self.transitions[state]['$']:  # Para cada estado siguiente en la transición épsilon.
                    if next_state not in closure:  # Si el estado siguiente no está en el cierre.
                        closure.add(next_state)  # Añade el estado siguiente al cierre.
                        stack.append(next_state)  # Añade el estado siguiente a la pila para procesar sus transiciones.
        return closure  # Devuelve el conjunto de cierre épsilon.

class AutomataProgram:
    def __init__(self, root):
        # Inicializa la ventana principal del programa.
        self.root = root  # Asigna la ventana raíz a un atributo.
        self.root.title("Programa de Autómatas")  # Establece el título de la ventana.
        self.afn = Automata()  # Crea una instancia de Automata para el AFN.
        self.afd = None  # Inicializa el AFD como None.
        self.regex = ""  # Inicializa una cadena vacía para la expresión regular.
        self.afd_counter = 1  # Contador para los archivos AFD generados.
        self.gramatica_counter = 1  # Contador para las gramáticas generadas.
        self.gramatica_actual = ""  # Variable para almacenar la gramática actual.
        
        # Aplicar un tema moderno a la ventana.
        self.root.configure(bg='#f5f5f5')  # Establece el fondo claro para la ventana principal.
        
        self.create_widgets()  # Llama a la función para crear los widgets de la interfaz.

    def create_widgets(self):
        # Crea y organiza los widgets en la ventana.
        
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="10")  # Crea un marco principal con relleno.
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))  # Coloca el marco en la cuadrícula.
        self.root.columnconfigure(0, weight=1)  # Configura el peso de la columna para expandirse.
        self.root.rowconfigure(0, weight=1)  # Configura el peso de la fila para expandirse.

        # Estilo para los botones
        style = ttk.Style()  # Crea un estilo nuevo.
        style.configure('Accent.TButton', font=('Helvetica', 12), background='white', foreground='black')  # Configura el estilo del botón.
        style.map('Accent.TButton', foreground=[('active', '#1411d8')], background=[('active', '#009688')])  # Cambia colores al activarse.

        # Marco de entrada de expresión regular
        regex_frame = ttk.LabelFrame(main_frame, text="Expresión Regular", padding="10", style="TFrame")  # Crea un marco para la entrada de expresión regular.
        regex_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))  # Coloca el marco en la cuadrícula.
        
        self.regex_entry = ttk.Entry(regex_frame, width=50, font=('Arial', 12), foreground='#003366')  # Campo de entrada para la expresión regular.
        self.regex_entry.grid(row=0, column=0, padx=5, pady=5)  # Coloca el campo en la cuadrícula.
        
        ttk.Button(regex_frame, text="Cargar desde archivo", command=self.load_file, style='Accent.TButton').grid(row=0, column=1, padx=5, pady=5)  # Botón para cargar expresiones desde un archivo.

        # Operaciones
        operations_frame = ttk.Frame(main_frame, padding="10")  # Crea un marco para las operaciones.
        operations_frame.grid(row=1, column=0, sticky=(tk.W, tk.N))  # Coloca el marco en la cuadrícula.

        self.style_buttons(operations_frame)  # Aplica estilos a los botones en el marco de operaciones.
        
        # Área de resultados con estilo
        self.result_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=20, bg='#f0f8ff', font=('Courier', 11), fg='#2f4f4f', state=tk.DISABLED)  # Área de texto para mostrar resultados.
        self.result_text.grid(row=1, column=1, rowspan=5, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))  # Coloca el área de texto en la cuadrícula.

        # Frame para validar cadenas (oculto al principio)
        self.validar_frame = ttk.LabelFrame(main_frame, text="Validar Cadenas", padding="10")  # Marco para validar cadenas.
        self.validar_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))  # Coloca el marco en la cuadrícula.
        self.validar_frame.grid_remove()  # Oculta el marco inicialmente.

        self.cadena_entry = ttk.Entry(self.validar_frame, width=30, font=('Arial', 12))  # Campo de entrada para la cadena a validar.
        self.cadena_entry.grid(row=0, column=0, padx=5, pady=5)  # Coloca el campo en la cuadrícula.
        ttk.Button(self.validar_frame, text="Validar", command=self.validar_cadena, style='Accent.TButton').grid(row=0, column=1, padx=5, pady=5)  # Botón para validar la cadena ingresada.

    def style_buttons(self, frame):
        # Aplica estilos visuales a los botones importantes en el marco dado.
        ttk.Button(frame, text="Generar AFN", command=self.generar_afn, style='Accent.TButton').grid(row=0, column=0, pady=5)  # Botón para generar AFN.
        ttk.Button(frame, text="Convertir a AFD", command=self.conversion_afd, style='Accent.TButton').grid(row=1, column=0, pady=5)  # Botón para convertir AFN a AFD.
        ttk.Button(frame, text="Validar Cadenas", command=self.show_validar_cadenas, style='Accent.TButton').grid(row=2, column=0, pady=5)  # Botón para validar cadenas.
        ttk.Button(frame, text="Mostrar Gramática", command=self.mostrar_gramatica, style='Accent.TButton').grid(row=3, column=0, pady=5)  # Botón para mostrar la gramática.
        ttk.Button(frame, text="Grabar", command=self.grabar, style='Accent.TButton').grid(row=4, column=0, pady=5)  # Botón para grabar resultados.
        ttk.Button(frame, text="Salir", command=self.root.quit, style='Accent.TButton').grid(row=5, column=0, pady=5)  # Botón para salir del programa.

    def load_file(self):
        # Abre un cuadro de diálogo para cargar un archivo de texto con la expresión regular.
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])  # Permite al usuario seleccionar un archivo.
        if filename:  # Si se seleccionó un archivo.
            try:
                with open(filename, 'r') as file:  # Intenta abrir el archivo en modo lectura.
                    self.regex = file.read().strip()  # Lee el contenido del archivo y elimina espacios en blanco.
                    self.regex_entry.delete(0, tk.END)  # Borra el campo de entrada de expresión regular.
                    self.regex_entry.insert(0, self.regex)  # Inserta la expresión regular leída en el campo.
                self.log(f"Expresión regular cargada: {self.regex}", 'info')  # Registra un mensaje de éxito.
            except Exception as e:  # Si ocurre un error al abrir el archivo.
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")  # Muestra un mensaje de error.

    def generar_afn(self):
        # Genera un autómata finito no determinista (AFN) a partir de la expresión regular ingresada.
        self.regex = self.regex_entry.get()  # Obtiene la expresión regular del campo de entrada.
        if not self.regex:  # Si el campo de entrada está vacío.
            messagebox.showwarning("Advertencia", "Primero ingrese una expresión regular.")  # Muestra una advertencia.
            return  # Sale de la función.
        
        self.log("Generando AFN", 'action')  # Registra la acción de generación del AFN.
        self.afn = self.regex_to_afn(self.regex)  # Convierte la expresión regular en un AFN.
        self.log("AFN generado exitosamente.", 'success')  # Registra un mensaje de éxito.
        self.show_afn()  # Muestra el AFN generado.

    def regex_to_afn(self, regex):
        # Convierte una expresión regular en un autómata finito no determinista (AFN).
        afn = Automata()  # Crea una nueva instancia de Automata.
        stack = []  # Inicializa una pila para manejar los estados.
        state_counter = 0  # Contador para los estados.

        for char in regex:  # Itera sobre cada carácter de la expresión regular.
            if char in '()*+|':  # Si el carácter es un operador especial.
                if char == '(':  # Si es un paréntesis de apertura.
                    stack.append(state_counter)  # Apila el contador de estado.
                elif char == ')':  # Si es un paréntesis de cierre.
                    start = stack.pop()  # Desapila el inicio de la expresión.
                    afn.add_transition(start, '$', {state_counter})  # Añade una transición ε.
                elif char == '*':  # Si es el operador Kleene.
                    start = stack.pop()  # Desapila el estado de inicio.
                    afn.add_transition(start, '$', {state_counter})  # Crea transición ε al nuevo estado.
                    afn.add_transition(state_counter, '$', {start})  # Permite bucle al estado de inicio.
                    stack.append(start)  # Vuelve a apilar el estado de inicio.
                elif char == '+':  # Si es el operador de suma.
                    start = stack.pop()  # Desapila el estado de inicio.
                    afn.add_transition(state_counter, '$', {start})  # Crea transición ε al estado de inicio.
                    stack.append(start)  # Apila el estado de inicio.
                elif char == '|':  # Si es el operador OR.
                    alt_start = stack.pop()  # Desapila el estado alternativo.
                    afn.add_transition(alt_start - 1, '$', {state_counter})  # Conecta el estado alternativo.
            else:  # Si el carácter es un símbolo del alfabeto.
                afn.add_transition(state_counter, char, {state_counter + 1})  # Añade una transición normal.
                afn.alphabet.add(char)  # Añade el símbolo al alfabeto del autómata.
                stack.append(state_counter)  # Apila el estado actual.
                state_counter += 1  # Incrementa el contador de estado.

        afn.initial_state = {0}  # Establece el estado inicial en el estado 0.
        afn.final_states = {state_counter}  # Establece el estado final en el último estado.
        afn.states = set(range(state_counter + 1))  # Crea un conjunto de todos los estados.
        return afn  # Devuelve el AFN generado.

    def show_afn(self):
        # Muestra los detalles del AFN generado en el área de resultados.
        self.log("Detalles del AFN:", 'action')  # Registra la acción de mostrar detalles del AFN.
        self.log(f"Estados: {self.afn.states}", 'info')  # Muestra los estados del AFN.
        self.log(f"Estado inicial: {self.afn.initial_state}", 'info')  # Muestra el estado inicial.
        self.log(f"Estados finales: {self.afn.final_states}", 'info')  # Muestra los estados finales.
        self.log(f"Alfabeto: {self.afn.alphabet}", 'info')  # Muestra el alfabeto del AFN.
        self.log("Transiciones:", 'info')  # Indica que se mostrarán las transiciones.
        for state, transitions in self.afn.transitions.items():  # Itera sobre las transiciones.
            for symbol, next_states in transitions.items():  # Itera sobre los símbolos y los estados siguientes.
                self.log(f"  {state} -- {symbol} --> {next_states}", 'transition')  # Registra la transición.

    def conversion_afd(self):
        # Convierte el autómata finito no determinista (AFN) en un autómata finito determinista (AFD).
        if not self.afn:  # Si no se ha generado un AFN.
            messagebox.showwarning("Advertencia", "Primero genere un AFN.")  # Muestra una advertencia.
            return  # Sale de la función.

        self.log("Convirtiendo AFN a AFD", 'action')  # Registra la acción de conversión.
        self.afd = self.afn_to_afd()  # Convierte el AFN a AFD.
        self.save_afd_to_file()  # Guarda el AFD en un archivo.
        self.log(f"AFD generado y guardado en AFD{self.afd_counter}.TXT", 'success')  # Registra el éxito de la conversión.
        self.afd_counter += 1  # Incrementa el contador para el siguiente archivo AFD.
        self.show_afd()  # Muestra el AFD generado.

    def afn_to_afd(self):
        # Convierte un AFN en un AFD utilizando el algoritmo de subconjuntos.
        afd = Automata()  # Crea una nueva instancia de Automata para el AFD.
        initial_state = frozenset(self.afn.epsilon_closure(self.afn.initial_state))  # Calcula el cierre épsilon del estado inicial del AFN.
        states_queue = deque([initial_state])  # Inicializa una cola con el estado inicial.
        states_dict = {initial_state: 0}  # Diccionario para mapear estados del AFD a índices.
        state_counter = 1  # Contador para los estados del AFD.
        while states_queue:  # Mientras haya estados en la cola
            current_state = states_queue.popleft()  # Obtener el estado actual de la cola
            for symbol in self.afn.alphabet:  # Iterar sobre cada símbolo del alfabeto
                next_state = frozenset()  # Inicializar el conjunto del siguiente estado
                # Iterar sobre los estados en el estado actual
                for state in current_state:
                    # Comprobar si el estado actual tiene transiciones para el símbolo
                    if state in self.afn.transitions and symbol in self.afn.transitions[state]:
                        # Obtener el cierre épsilon de los estados alcanzables
                        next_state |= self.afn.epsilon_closure(self.afn.transitions[state][symbol])

                if next_state:  # Si hay un estado siguiente (no vacío)
                    # Si el siguiente estado no ha sido visto antes
                    if next_state not in states_dict:
                        states_dict[next_state] = state_counter  # Asignar un nuevo número de estado
                        states_queue.append(next_state)  # Agregar el nuevo estado a la cola
                        state_counter += 1  # Incrementar el contador de estados

                    # Agregar una transición al AFD desde el estado actual al siguiente estado
                    afd.add_transition(states_dict[current_state], symbol, {states_dict[next_state]})
                    
            # Agregar el estado actual al conjunto de estados del AFD
            afd.states.add(states_dict[current_state])
            # Comprobar si el estado actual es un estado final
            if current_state & self.afn.final_states:
                afd.final_states.add(states_dict[current_state])  # Agregar estado final al AFD

        # Configurar el estado inicial del AFD
        afd.initial_state = {0}
        afd.alphabet = self.afn.alphabet  # Definir el alfabeto del AFD
        return afd  # Retornar el AFD generado

    def save_afd_to_file(self):
        """Guarda el AFD en un archivo de texto."""
        filename = f"AFD{self.afd_counter}.TXT"  # Nombre del archivo para guardar
        with open(filename, 'w') as file:  # Abrir el archivo en modo escritura
            # Escribir los estados del AFD en el archivo
            file.write(f"Estados = {{{','.join(map(str, self.afd.states))}}}\n")
            file.write(f"Alfabeto = {{{','.join(self.afd.alphabet)}}}\n")
            file.write(f"Estado inicial = {self.afd.initial_state}\n")
            file.write(f"Estados finales = {{{','.join(map(str, self.afd.final_states))}}}\n")
            file.write("Transiciones:\n")  # Encabezado para las transiciones
            # Escribir cada transición en el archivo
            for state, transitions in self.afd.transitions.items():
                for symbol, next_states in transitions.items():
                    file.write(f"  {state} -- {symbol} --> {','.join(map(str, next_states))}\n")

    def show_afd(self):
        """Muestra detalles del AFD en el área de resultados."""
        self.log("Detalles del AFD:", 'action')  # Log para indicar que se mostrarán detalles
        self.log(f"Estados: {self.afd.states}", 'info')  # Mostrar estados del AFD
        self.log(f"Estado inicial: {self.afd.initial_state}", 'info')  # Mostrar estado inicial
        self.log(f"Estados finales: {self.afd.final_states}", 'info')  # Mostrar estados finales
        self.log(f"Alfabeto: {self.afd.alphabet}", 'info')  # Mostrar alfabeto
        self.log("Transiciones:", 'info')  # Encabezado para transiciones
        # Mostrar cada transición del AFD
        for state, transitions in self.afd.transitions.items():
            for symbol, next_states in transitions.items():
                self.log(f"  {state} -- {symbol} --> {next_states}", 'transition')

    def show_validar_cadenas(self):
        """Muestra el marco para validar cadenas."""
        self.validar_frame.grid()  # Mostrar el marco de validación

    def validar_cadena(self):
        """Valida una cadena contra el AFD."""
        if not self.afd:  # Comprobar si existe un AFD
            messagebox.showwarning("Advertencia", "Primero convierta el AFN a AFD.")  # Advertencia si no hay AFD
            return

        cadena = self.cadena_entry.get()  # Obtener la cadena ingresada
        if not cadena:  # Comprobar si la cadena está vacía
            messagebox.showwarning("Advertencia", "Ingrese una cadena para validar.")  # Advertencia si está vacía
            return

        self.log(f"Validando cadena: {cadena}", 'action')  # Log para indicar la validación
        current_state = list(self.afd.initial_state)[0]  # Obtener el estado inicial

        # Iterar sobre cada símbolo en la cadena
        for symbol in cadena:
            if symbol not in self.afd.alphabet:  # Comprobar si el símbolo está en el alfabeto
                self.log(f"El símbolo {symbol} no pertenece al alfabeto.", 'error')  # Log de error
                return

            # Comprobar si hay transición para el símbolo desde el estado actual
            if current_state not in self.afd.transitions or symbol not in self.afd.transitions[current_state]:
                self.log("Cadena rechazada.", 'error')  # Log de error si la cadena es rechazada
                return

            # Actualizar el estado actual basado en la transición
            current_state = list(self.afd.transitions[current_state][symbol])[0]

        # Comprobar si el estado actual es un estado final
        if current_state in self.afd.final_states:
            self.log("Cadena aceptada.", 'success')  # Log de éxito si la cadena es aceptada
        else:
            self.log("Cadena rechazada.", 'error')  # Log de error si la cadena es rechazada

    def mostrar_gramatica(self):
        """Genera y muestra la gramática basada en el AFD."""
        self.log("Generando gramática...", 'action')  # Log para indicar la generación de gramática
        self.gramatica_actual = self.generar_gramatica()  # Generar la gramática
        self.log(self.gramatica_actual, 'info')  # Mostrar la gramática generada

    def generar_gramatica(self):
        """Genera la gramática a partir del AFD."""
        if not self.afd:  # Comprobar si existe un AFD
            return "Primero debe generar un AFD."  # Mensaje si no hay AFD
        
        gramatica = "Gramática generada a partir del AFD:\n"  # Encabezado para la gramática
        # Iterar sobre cada estado y sus transiciones
        for state, transitions in self.afd.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    gramatica += f"S{state} -> {symbol}S{next_state}\n"  # Regla de producción
            if state in self.afd.final_states:
                gramatica += f"S{state} -> ε\n"  # Regla para estado final
        return gramatica  # Retornar la gramática generada

    def grabar(self):
        """Guarda la gramática generada en un archivo de texto."""
        if not self.gramatica_actual:  # Comprobar si hay gramática generada
            messagebox.showwarning("Advertencia", "No hay gramática generada para guardar.")  # Advertencia si no hay gramática
            return

        self.log("Guardando gramática...", 'action')  # Log para indicar la guardado de gramática
        gramatica = f"G{self.gramatica_counter}.TXT"  # Nombre del archivo de gramática
        while os.path.exists(gramatica):  # Asegurarse de que el archivo no exista
            self.gramatica_counter += 1
            gramatica = f"G{self.gramatica_counter}.TXT"

        with open(gramatica, 'w') as file:  # Abrir el archivo en modo escritura
            file.write(self.gramatica_actual)  # Guardar la gramática en el archivo
        self.log(f"Gramática guardada en {gramatica}", 'success')  # Log de éxito al guardar

    def log(self, message, log_type='info'):
        """Registra mensajes en el área de resultados."""
        self.result_text.config(state=tk.NORMAL)  # Habilitar edición temporalmente
        if log_type == 'info':
            self.result_text.insert(tk.END, message + "\n", 'info')  # Registrar información
        elif log_type == 'success':
            self.result_text.insert(tk.END, message + "\n", 'success')  # Registrar éxito
        elif log_type == 'error':
            self.result_text.insert(tk.END, message + "\n", 'error')  # Registrar error
        elif log_type == 'action':
            self.result_text.insert(tk.END, message + "\n", 'action')  # Registrar acción
        elif log_type == 'transition':
            self.result_text.insert(tk.END, message + "\n", 'transition')  # Registrar transición
        self.result_text.see(tk.END)  # Desplazar hacia abajo el área de texto
        self.result_text.config(state=tk.DISABLED)  # Deshabilitar la edición nuevamente
        
    def configure_text_tags(self):
        """Configura las etiquetas de formato para el área de texto."""
        self.result_text.tag_configure('info', foreground='#1f4e79')  # Color para información
        self.result_text.tag_configure('success', foreground='#4CAF50', font=('Courier', 11, 'bold'))  # Color para éxito
        self.result_text.tag_configure('error', foreground='#FF5252', font=('Courier', 11, 'bold'))  # Color para errores
        self.result_text.tag_configure('action', foreground='#FF9800', font=('Courier', 11, 'italic'))  # Color para acciones
        self.result_text.tag_configure('transition', foreground='#009688', font=('Courier', 11))  # Color para transiciones

if __name__ == "__main__":
    root = tk.Tk()
    programa = AutomataProgram(root)
    programa.configure_text_tags()  # Configurar formato del área de texto
    root.mainloop()
