# Proyecto de Autómatas Finito No Determinista a Determinista (AFN a AFD)

Este proyecto es una aplicación de escritorio desarrollada en Python con la biblioteca `tkinter` para convertir un Autómata Finito No Determinista (AFN) a un Autómata Finito Determinista (AFD) y realizar la validación de cadenas. También permite generar y mostrar gramáticas.

## Características

- **Ingreso de Expresión Regular**: Permite ingresar una expresión regular y generar el AFN correspondiente.
- **Conversión de AFN a AFD**: Genera un AFD a partir del AFN creado y lo guarda en un archivo.
- **Validación de Cadenas**: Valida si una cadena pertenece al lenguaje descrito por el AFD generado.
- **Mostrar Gramática**: Genera y muestra la gramática asociada al AFD.
- **Interfaz Gráfica**: Utiliza `tkinter` para proporcionar una interfaz de usuario sencilla e interactiva.

## Instalación

1. Clona este repositorio en tu máquina local.
    ```bash
    git clone https://github.com/JefersonSuchite/ProyectoFinalAutomatasAFN-AFD
    ```
2. Instala las dependencias necesarias. La principal biblioteca es `tkinter`, la cual normalmente está preinstalada en Python. Si necesitas instalarla, ejecuta:
    ```bash
    sudo apt-get install python3-tk
    ```
3. Ejecuta el archivo principal `main.py` para iniciar la aplicación.
    ```bash
    python main.py
    ```

## Uso

1. **Ingreso de Expresión Regular**:
   - Ingresa una expresión regular en el campo de texto o cárgala desde un archivo `.txt`.
   - Haz clic en "Generar AFN" para crear el Autómata Finito No Determinista (AFN).

2. **Conversión de AFN a AFD**:
   - Tras generar el AFN, selecciona la opción "Convertir a AFD" para realizar la conversión.
   - El AFD generado se guarda en un archivo `AFD<TU_NUMERO>.TXT`.

3. **Validación de Cadenas**:
   - Ingresa una cadena en el campo correspondiente y selecciona "Validar Cadenas" para verificar si la cadena es aceptada por el AFD.

4. **Mostrar Gramática**:
   - La gramática correspondiente al AFD se puede generar seleccionando "Mostrar Gramática" y se despliega en la interfaz.

## Archivos Generados

- **AFD<TU_NUMERO>.TXT**: Archivo de texto que contiene los detalles del AFD generado, incluyendo los estados, transiciones, alfabeto y estados finales.

## Requisitos

- Python 3.x
- `tkinter` (para la interfaz gráfica)
- `re` (para trabajar con expresiones regulares)

## Autor

Desarrollado por Grupo 4
Willians Navas
Jeferson Suchite
Kimberly Villeda

