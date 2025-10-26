# -*- coding: utf-8 -*-
import pyautogui
import time
import os
import csv
import tkinter as tk
import sys
from datetime import datetime
import traceback
# import select # Ya no es necesario para la espera
import msvcrt # Módulo para entrada de consola en Windows

# Añadir manejo de excepciones para interrupciones
import signal
signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))

# Intentar importar la biblioteca para SAP GUI
try:
    import win32com.client
    SAP_GUI_SCRIPTING_AVAILABLE = True
except ImportError:
    print("AVISO: win32com no está instalado. No se podrán capturar mensajes directamente de SAP GUI.")
    print("Instala con: pip install pywin32")
    SAP_GUI_SCRIPTING_AVAILABLE = False

# --- Configuración ---
OUTPUT_FOLDER = r"C:\Volar\python\capturas_sap_test"
INPUT_CSV = r"C:\Volar\python\input\transacciones.csv"
# INPUT_FOLDER = r"C:\Volar\python\input" # No se usa si INPUT_CSV es ruta completa

# Posición para hacer clic en el monitor primario (referencia)
PRIMARY_MONITOR_X = 50
PRIMARY_MONITOR_Y = 50

# Tiempo entre capturas/verificaciones durante espera de usuario
WAIT_TIME = 5

# --- Variables Globales ---
ERRORS_DETECTED = False
DUMP_ERRORS = False
SBAR_DIALOG_ERRORS = False
transacciones_con_error = []
log_filename = "" # Se define en main al iniciar


def log_message(log_file, message):
    """
    Writes a message to a log file with a timestamp and prints it to the console.

    This function attempts to create the log directory if it does not exist, checks for write permissions,
    and handles exceptions gracefully. If the log file or its directory cannot be written to, it prints an alert
    and the log entry to the console instead.

    Args:
        log_file (str): The path to the log file where the message will be written.
        message (str): The message to log.

    Side Effects:
        - Writes the message with a timestamp to the specified log file.
        - Prints the message to the console.
        - Prints alerts to the console if directory creation or file writing fails.
    """
    """Escribe un mensaje en el archivo de log y lo muestra en pantalla"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    try:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
             try: os.makedirs(log_dir)
             except Exception as e_mkdir: print(f"ALERTA: No se pudo crear dir log {log_dir}: {e_mkdir}"); print(log_entry); return
        write_permission = False
        if os.path.exists(log_file): write_permission = os.access(log_file, os.W_OK)
        elif log_dir and os.path.exists(log_dir): write_permission = os.access(log_dir, os.W_OK)
        if not write_permission and (os.path.exists(log_file) or (log_dir and os.path.exists(log_dir))):
            print(f"ALERTA: Sin permisos escritura log: {log_file if os.path.exists(log_file) else log_dir}"); print(log_entry); return
        with open(log_file, 'a', encoding='utf-8') as f: f.write(log_entry + "\n")
    except Exception as e: print(f"Error escribiendo log ({log_file}): {e}"); print(log_entry); return
    print(message)


# --- FUNCIÓN CAPTURE_SCREEN CORREGIDA ---
# --- FUNCIÓN CAPTURE_SCREEN CORREGIDA (Reemplaza la existente) ---
def capture_screen(prefix, log_filename_func=None):
    """
    Captures a screenshot of the entire screen and saves it with a specified prefix.
    The screenshot is saved in a directory named after the transaction code extracted from the prefix.
    If the directory does not exist, it is created. Logging is performed to a specified log file or a global log file.
    Args:
        prefix (str): Prefix for the screenshot filename. The transaction code is extracted from this prefix.
        log_filename_func (str, optional): Path to the log file to use for logging messages. If not provided, uses the global log_filename.
    Returns:
        str or None: The path to the saved screenshot if successful, or None if an error occurred.
    """
    """Captura la pantalla completa y la guarda con el prefijo especificado"""
    global log_filename # Acceder al global si no se pasa argumento
    log_to_use = log_filename_func if log_filename_func else log_filename

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        # Intenta obtener el código base de la transacción del prefijo
        transaction_code = prefix.split('_')[0]
    except IndexError:
        transaction_code = "general" # Código por defecto si no hay '_'

    DIR_TRANS = os.path.join(OUTPUT_FOLDER, transaction_code)
    screenshot_path = os.path.join(DIR_TRANS, f"{prefix}_{timestamp}.png")

    # Verifica si el directorio DIR_TRANS existe
    if not os.path.exists(DIR_TRANS):
        try:
            os.makedirs(DIR_TRANS)
            msg = f"Directorio '{DIR_TRANS}' creado."
            # --- SINTAXIS CORREGIDA ---
            if log_to_use:
                log_message(log_to_use, msg)
            else:
                print(msg)
            # --- FIN CORRECCIÓN ---
        except Exception as e:
             msg = f"Error creando directorio {DIR_TRANS}: {e}"
             # --- SINTAXIS CORREGIDA ---
             if log_to_use:
                 log_message(log_to_use, msg)
             else:
                 print(msg)
             # --- FIN CORRECCIÓN ---
             return None # No se puede guardar captura si no se crea el directorio

    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        msg = f"Captura guardada: {screenshot_path}"
        # --- SINTAXIS CORREGIDA (ya estaba bien, pero asegurar formato) ---
        if log_to_use:
            log_message(log_to_use, msg)
        # --- FIN CORRECCIÓN ---
        # No imprimir cada captura en consola, solo en log
        return screenshot_path
    except Exception as e:
        msg = f"Error al capturar pantalla: {e}"
        # --- SINTAXIS CORREGIDA ---
        if log_to_use:
            log_message(log_to_use, msg)
        else:
            print(msg)
        # --- FIN CORRECCIÓN ---
        return None
# --- FIN FUNCIÓN CAPTURE_SCREEN CORREGIDA ---
# --- FIN FUNCIÓN CAPTURE_SCREEN CORREGIDA ---

def focus_primary_monitor():
    """
    Moves the mouse cursor to the primary monitor's coordinates and clicks to focus it.

    Returns:
        bool: True if the operation was successful, False otherwise.

    Logs:
        If an error occurs and 'log_filename' is set, logs the error message using 'log_message'.
        Otherwise, prints the error message to the console.
    """
    """Método simple para enfocar el monitor primario"""
    global log_filename
    try:
        pyautogui.moveTo(PRIMARY_MONITOR_X, PRIMARY_MONITOR_Y, duration=0.5); pyautogui.click(); time.sleep(0.5)
        return True
    except Exception as e:
        msg = f"Error al enfocar monitor: {e}"; (log_message(log_filename, msg) if log_filename else print(msg)); return False

def call_transaction_YBC_0007(transaction_code, log_filename_func):
    """
    Executes the SAP transaction YBC_0007 using GUI automation.

    This function automates the process of opening the YBC_0007 transaction in SAP, interacting with its interface,
    and capturing screenshots before and after the transaction execution. It logs each significant step and handles
    exceptions by logging error details.

    Args:
        transaction_code (str): The code of the transaction to be executed, used for directory and logging purposes.
        log_filename_func (callable): A function or callable used for logging messages throughout the process.

    Returns:
        bool: True if the transaction was executed successfully, False if an exception occurred.
    """
    """Llama a la transacción YBC_0007"""
    # (Implementación sin cambios)
    try:
        DIR_TRANS = os.path.join(OUTPUT_FOLDER, transaction_code); log_message(log_filename_func, f"Dir YBC_0007: {DIR_TRANS}")
        # volver_pagina_principal() # Comentado
        log_message(log_filename_func, "Abriendo YBC_0007..."); pyautogui.hotkey('ctrl', 'n'); time.sleep(2)
        pyautogui.write("YBC_0007"); pyautogui.press('enter'); time.sleep(8)
        capture_screen(f"{transaction_code}_YBC_0007_inicial", log_filename_func)
        log_message(log_filename_func, "Interactuando con YBC_0007..."); screen_width, screen_height = pyautogui.size()
        fichero_x = int(screen_width * 0.4); fichero_y = int(screen_height * 0.14)
        log_message(log_filename_func, f"Clic Fichero: ({fichero_x}, {fichero_y})"); pyautogui.click(fichero_x, fichero_y); time.sleep(1)
        pyautogui.hotkey('ctrl', 'a'); time.sleep(0.5); pyautogui.press('delete'); time.sleep(0.5)
        log_message(log_filename_func, f"Escribiendo ruta: {DIR_TRANS}"); pyautogui.write(DIR_TRANS); time.sleep(1)
        log_message(log_filename_func, "Esperando 3s antes de F8..."); time.sleep(3)
        log_message(log_filename_func, "Presionando F8..."); pyautogui.press('f8'); time.sleep(3)
        capture_screen(f"{transaction_code}_YBC_0007_resultado", log_filename_func); time.sleep(5)
        # volver_pagina_principal() # Comentado
        return True
    except Exception as e:
        error_details = traceback.format_exc(); log_message(log_filename_func, f"Error YBC_0007: {e}\n{error_details}")
        # try: volver_pagina_principal() # Comentado
        # except: pass
        return False


def get_error_text_from_sap_gui(transaction_code, log_filename_func):
    """
    Obtains error text directly from the SAP GUI interface for a given transaction.

    This function interacts with the SAP GUI via scripting to detect and extract error messages,
    such as DUMPs or status bar messages, that occur during the execution of a transaction.
    It captures relevant error information, saves screenshots, and logs messages as needed.

    Args:
        transaction_code (str): The SAP transaction code being executed.
        log_filename_func (callable): A function or lambda that returns the log filename for logging purposes.

    Returns:
        str or None: The file path to the saved DUMP error information if a DUMP is detected,
                     or None if only a status bar message is found or no error is detected.

    Side Effects:
        - Sets global flags (ERRORS_DETECTED, DUMP_ERRORS, SBAR_DIALOG_ERRORS) based on error detection.
        - Captures screenshots and saves error details to files in the transaction-specific output directory.
        - Logs messages about the error detection process and any issues encountered.

    Notes:
        - Requires SAP GUI scripting to be available and win32com to be installed.
        - Handles multiple SAP GUI connections and sessions, checking up to 5 windows per session.
        - Searches for error keywords in window titles and extracts detailed error information if a DUMP is found.
        - If no DUMP is found, checks the status bar for error messages.
        - All exceptions are logged, and the function is robust to most SAP GUI scripting errors.
    """
    """Obtiene el texto de error directamente de la interfaz de SAP GUI"""
    # (Implementación sin cambios)
    global ERRORS_DETECTED, DUMP_ERRORS, SBAR_DIALOG_ERRORS; ERRORS_DETECTED = True
    capture_screen(f"{transaction_code}_error_detallado", log_filename_func)
    DIR_TRANS = os.path.join(OUTPUT_FOLDER, transaction_code)
    if not os.path.exists(DIR_TRANS):
        try: os.makedirs(DIR_TRANS)
        except Exception as e: log_message(log_filename_func, f"Error creando dir {DIR_TRANS}: {e}"); return None
    if not SAP_GUI_SCRIPTING_AVAILABLE: log_message(log_filename_func, "win32com no instalado."); return None
    try:
        SapGuiAuto = win32com.client.GetObject("SAPGUI"); application = SapGuiAuto.GetScriptingEngine
        if application.Children.Count == 0: log_message(log_filename_func, "No hay conexiones SAP."); return None
        log_message(log_filename_func, "Conexión SAP GUI OK.")
        dump_file_path = None
        for conn_idx in range(application.Children.Count):
            connection = application.Children(conn_idx)
            for sess_idx in range(connection.Children.Count):
                try:
                    session = connection.Children(sess_idx); dump_found_in_session = False
                    for window_id in range(5): # Check windows 0-4
                        try:
                            window = session.findById(f"wnd[{window_id}]")
                            if window and hasattr(window, 'text'):
                                window_title = window.text; error_keywords = ["Error", "excepción", "DUMP", "tiempo de ejecución", "runtime", "ABAP error"]
                                if any(keyword.lower() in window_title.lower() for keyword in error_keywords):
                                    log_message(log_filename_func, f"Ventana error: wnd[{window_id}] - {window_title}")
                                    if ("DUMP" in window_title.upper() or "TIEMPO DE EJECUCIÓN" in window_title.upper() or "RUNTIME" in window_title.upper()):
                                        DUMP_ERRORS = True; log_message(log_filename_func, "Error DUMP detectado")
                                        error_data = [f"Título: {window_title}"] # Captura simplificada DUMP
                                        try:
                                            possible_elements=[f"wnd[{window_id}]/usr/lbl[{r},{c}]" for r in range(5) for c in range(10)]+[f"wnd[{window_id}]/usr/txtRSTXT-TEXTFELD{i}" for i in range(1,4)]
                                            for elem_path in possible_elements:
                                                try: elem=session.findById(elem_path); error_data.append(elem.text) if elem and hasattr(elem,'text') and elem.text else None
                                                except: continue
                                        except Exception as table_error: log_message(log_filename_func, f"Error tabla DUMP: {table_error}")
                                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S"); dump_file_path = os.path.join(DIR_TRANS, f"{transaction_code}_dump_error_{timestamp}.txt")
                                        with open(dump_file_path, 'w', encoding='utf-8') as f: f.write("\n".join(error_data)); log_message(log_filename_func, f"Info DUMP guardada: {dump_file_path}"); dump_found_in_session = True; break
                        except: continue # Ignore window find error
                    if dump_found_in_session: break # Exit session loop if DUMP found
                    # Check status bar only if no DUMP was found in this session
                    if not dump_found_in_session:
                        try:
                            sbar = session.findById("wnd[0]/sbar")
                            if sbar and hasattr(sbar, 'text') and sbar.text:
                                sbar_text = sbar.text.strip()
                                if sbar_text: log_message(log_filename_func, f"Mensaje sbar: {sbar_text}"); SBAR_DIALOG_ERRORS = True; timestamp = datetime.now().strftime("%Y%m%d_%H%M%S"); sbar_file_path = os.path.join(DIR_TRANS, f"{transaction_code}_sbar_msg_{timestamp}.txt");
                                with open(sbar_file_path, 'w', encoding='utf-8') as f: f.write(f"Mensaje sbar:\n{sbar_text}"); log_message(log_filename_func, f"Mensaje sbar guardado: {sbar_file_path}")
                        except: pass # Ignore sbar errors
                except: continue # Ignore session errors
            if dump_found_in_session: return dump_file_path # Return DUMP file path if found
        return None # Return None if only sbar message or no specific error window found
    except Exception as e: log_message(log_filename_func, f"Error capturando texto SAP: {e}\n{traceback.format_exc()}"); return None


def get_sap_message():
    """
    Attempts to retrieve the message from the SAP status bar using SAP GUI Scripting.

    Returns:
        str: The message from the SAP status bar if available, or an appropriate error message if not.

    Notes:
        - Requires SAP GUI Scripting to be enabled and available.
        - Iterates through all active SAP GUI connections and sessions to find the status bar message.
        - Returns specific messages if SAP GUI Scripting is unavailable, no active connections are found, or no status bar message is present.
        - Logs or prints errors encountered during execution.
    """
    """Intenta obtener el mensaje de la barra de estado de SAP"""
    # (Implementación sin cambios)
    global log_filename;
    if not SAP_GUI_SCRIPTING_AVAILABLE: return "SAP GUI Scripting no disponible"
    try:
        SapGuiAuto = win32com.client.GetObject("SAPGUI"); application = SapGuiAuto.GetScriptingEngine
        if application.Children.Count == 0: return "No hay conexiones SAP GUI activas"
        for conn_index in range(application.Children.Count):
            connection = application.Children(conn_index)
            for sess_index in range(connection.Children.Count):
                try:
                    session = connection.Children(sess_index); sbar_paths = ["wnd[0]/sbar", "wnd[1]/sbar"]
                    for path in sbar_paths:
                        try: sbar = session.findById(path); message = sbar.text.strip(); return message if message else ""
                        except: continue
                except: continue
        return "No se encontró mensaje en barra de estado"
    except Exception as e: msg = f"Error al leer mensaje de SAP: {str(e)}"; (log_message(log_filename, msg) if log_filename else print(msg)); return msg


# --- FUNCIÓN DETECTAR ERROR CON CORRECCIÓN EN SBAR KEYWORDS ---
def detectar_error_pantalla():
    """
    Checks for visible error screens or critical messages in the SAP GUI session.
    This function inspects all active SAP GUI sessions and their windows to detect the presence of error conditions.
    It performs the following checks:
    1. Window Titles: Scans up to 5 windows per session for titles containing high-priority error keywords (e.g., "Error", "excepción", "DUMP", "runtime").
    2. Status Bar (sbar): Checks the status bar text in the first two windows for critical error keywords (e.g., "interrumpido", "cancelado", "dump"), while ignoring certain non-critical phrases.
    Returns:
        bool: True if a critical error is detected in any window title or status bar, False otherwise.
    Side Effects:
        Logs debug and detection messages using the global `log_filename` if set, or prints to stdout.
    Raises:
        Handles and logs all exceptions internally; does not propagate exceptions.
    """
    """Verifica si hay una pantalla de error visible o mensaje CRÍTICO en sbar"""
    global log_filename
    log_msg_func = lambda msg: log_message(log_filename, msg) if log_filename else print(msg)

    if not SAP_GUI_SCRIPTING_AVAILABLE: return False
    try:
        SapGuiAuto = win32com.client.GetObject("SAPGUI"); application = SapGuiAuto.GetScriptingEngine
        if application.Children.Count == 0: return False

        for conn_index in range(application.Children.Count):
            connection = application.Children(conn_index)
            for sess_index in range(connection.Children.Count):
                try:
                    session = connection.Children(sess_index)
                    log_msg_func(f"DEBUG: Verificando errores en Conn[{conn_index}]/Sess[{sess_index}]")

                    # 1. Verificar títulos (Prioridad alta)
                    for window_id in range(5):
                        try:
                            window = session.findById(f"wnd[{window_id}]")
                            if window and hasattr(window, 'text'):
                                window_title = window.text; log_msg_func(f"DEBUG: Título wnd[{window_id}]: '{window_title}'")
                                error_keywords_title = ["Error", "excepción", "DUMP", "tiempo de ejecución", "runtime", "ABAP error"] # Más estricto para títulos
                                if any(keyword.lower() in window_title.lower() for keyword in error_keywords_title):
                                    log_msg_func(f"DETECTADO (Título): Ventana error '{window_title}' en wnd[{window_id}]")
                                    return True # Error real detectado
                        except: continue

                    # 2. Verificar Sbars (MENOS sensible ahora)
                    for win_idx_sbar in range(2): # Chequear wnd[0] y wnd[1]
                        try:
                            sbar = session.findById(f"wnd[{win_idx_sbar}]/sbar")
                            if sbar and hasattr(sbar, 'text'):
                                sbar_text = sbar.text.strip(); log_msg_func(f"DEBUG: Texto sbar wnd[{win_idx_sbar}]: '{sbar_text}'")
                                if sbar_text:
                                    # *** LISTA CORREGIDA: Solo keywords que indican interrupción ***
                                    error_keywords_sbar = ["interrumpido", "cancelado", "no autorizado", "dump", "runtime", "terminado"]
                                    if any(keyword.lower() in sbar_text.lower() for keyword in error_keywords_sbar):
                                         ignore_phrases = ["Objeto bloqueado por usuario", "no modificable", "modificado"]
                                         if not any(phrase.lower() in sbar_text.lower() for phrase in ignore_phrases):
                                            log_msg_func(f"DETECTADO (Sbar wnd[{win_idx_sbar}] CRÍTICO): '{sbar_text}'")
                                            return True # Error CRÍTICO detectado en sbar
                        except Exception as e_sbar: log_msg_func(f"DEBUG: No se pudo acceder sbar wnd[{win_idx_sbar}]: {e_sbar}"); pass
                except Exception as session_error: log_msg_func(f"DEBUG: Error procesando sesión {sess_index}: {session_error}"); continue
        return False
    except Exception as e: log_msg_func_fallback = lambda msg: log_message(log_filename, msg) if log_filename else print(msg); log_msg_func_fallback(f"ERROR general en detectar_error_pantalla: {e}\n{traceback.format_exc()}"); return False


def volver_pagina_principal():
    """
    Attempts to return to the SAP Easy Access screen. (Currently INACTIVE)

    This function is a placeholder and does not perform any actions to navigate
    to the SAP Easy Access screen. It logs or prints a message indicating that
    the function was called but is inactive.

    Returns:
        bool: Always returns True.
    """
    """Intenta volver a SAP Easy Access (INACTIVA)."""
    # (Implementación sin cambios, sigue INACTIVA)
    global log_filename; msg_prefix = "volver_pagina_principal (INACTIVA):"
    if log_filename: log_message(log_filename, f"{msg_prefix} Llamada pero acciones desactivadas.")
    else: print(f"{msg_prefix} Llamada pero acciones desactivadas.")
    return True


def leer_transacciones_csv(ruta_csv):
    """
    Lee los códigos de transacción desde un archivo CSV.

    Esta función intenta leer un archivo CSV especificado por `ruta_csv`, donde se espera que cada fila contenga al menos un código de transacción en la primera columna. El archivo debe estar delimitado por punto y coma (';') y contener un encabezado en la primera fila, que será ignorado. Por cada fila válida, se agrega un diccionario con la clave 'codigo' y el valor correspondiente al código de transacción.

    Parámetros:
        ruta_csv (str): Ruta al archivo CSV que contiene los códigos de transacción.

    Retorna:
        list[dict]: Una lista de diccionarios, cada uno con la clave 'codigo' correspondiente a un código de transacción leído del archivo.
                    Si el archivo no existe, está vacío, solo contiene el encabezado, o ocurre un error, retorna una lista vacía.

    Efectos secundarios:
        - Imprime mensajes de advertencia o error en consola.
        - Si `log_filename` está definido globalmente, registra mensajes en el archivo de log.

    Excepciones:
        - Maneja internamente excepciones como archivo inexistente, archivo vacío, errores de lectura y otros errores inesperados.
    """
    """Lee los códigos de transacción desde un archivo CSV"""
    # (Implementación sin cambios)
    global log_filename; transacciones = []
    try:
        if not os.path.exists(ruta_csv): msg = f"ERROR CRÍTICO: CSV no existe: {ruta_csv}"; print(msg); (log_message(log_filename, msg) if log_filename else None); return []
        with open(ruta_csv, 'r', encoding='utf-8') as archivo:
            lector_csv = csv.reader(archivo, delimiter=';'); header = next(lector_csv, None)
            if not header: raise StopIteration
        with open(ruta_csv, 'r', encoding='utf-8') as archivo: # Reabrir para leer datos
            lector_csv = csv.reader(archivo, delimiter=';'); next(lector_csv, None) # Saltar header de nuevo
            line_count = 1
            for fila in lector_csv:
                line_count += 1
                if fila and len(fila) > 0 and fila[0].strip(): transacciones.append({'codigo': fila[0].strip()})
                else: msg = f"ADVERTENCIA: Fila {line_count} ignorada: {fila}"; print(msg); (log_message(log_filename, msg) if log_filename else None)
        if not transacciones: msg = f"ADVERTENCIA: No se leyeron tx válidas de {ruta_csv}"; print(msg); (log_message(log_filename, msg) if log_filename else None)
        return transacciones
    except StopIteration: msg = f"ADVERTENCIA: CSV '{ruta_csv}' vacío o solo encabezado."; print(msg); (log_message(log_filename, msg) if log_filename else None); return []
    except Exception as e:
        msg = f"Error inesperado leyendo CSV ({ruta_csv}): {e}"; print(msg); details = traceback.format_exc(); print(f"Detalles: {details}")
        if log_filename: log_message(log_filename, msg); log_message(log_filename, f"Detalles: {details}")
        return []


def cerrar_ventana_error():
    """
    Attempts to close an error or dialog window in SAP by simulating key presses.

    This function uses pyautogui to send a sequence of key presses ('enter', 'esc', 'f12'),
    with delays between each, to close any open error or dialog windows in the SAP GUI.
    It logs the process if a log filename is set, otherwise prints messages to the console.

    Returns:
        bool: True if the key press sequence was executed without exceptions, False otherwise.
    """
    """Intenta cerrar una ventana de error/diálogo en SAP"""
    # (Implementación sin cambios)
    global log_filename; msg_prefix = "cerrar_ventana_error:"
    if log_filename: log_message(log_filename, f"{msg_prefix} Intentando cerrar ventana...")
    else: print(f"{msg_prefix} Intentando cerrar ventana...")
    try:
        pyautogui.press('enter'); time.sleep(1); pyautogui.press('esc'); time.sleep(1); pyautogui.press('f12'); time.sleep(1)
        if log_filename: log_message(log_filename, f"{msg_prefix} Intentos completados.")
        else: print(f"{msg_prefix} Intentos completados.")
        return True
    except Exception as e:
        if log_filename: log_message(log_filename, f"{msg_prefix} Error: {e}")
        else: print(f"{msg_prefix} Error: {e}"); return False

"""
    Waits for user confirmation (ENTER key) in the command prompt while periodically capturing screenshots and checking for critical errors.

    This function enters a loop where it:
    - Periodically captures the screen and logs the action.
    - Checks for critical errors using `detectar_error_pantalla`. If a critical error is detected, it logs the error, optionally dumps error information, closes the error window, and exits the loop.
    - Waits for the user to press ENTER in the command prompt or for a timeout (`WAIT_TIME`) to elapse before repeating the cycle.
    - Handles Ctrl+C (SIGINT) to exit the program gracefully.

    Args:
        transaction_code (str): The SAP transaction code currently being processed, used for logging and screenshot naming.
        log_filename_func (Callable): A function or callable used to determine the log filename for logging actions.

    Returns:
        bool: 
            - True if the user pressed ENTER to continue or if the loop exited for an unknown reason.
            - False if a critical error was detected during the wait.

    Side Effects:
        - Updates global error tracking variables.
        - Logs detailed debug information.
        - Captures screenshots and error dumps as needed.
        - May exit the program if Ctrl+C is detected.
"""
def wait_capture_and_get_user_confirmation(transaction_code, log_filename_func):
    """
    Maneja la espera del usuario usando msvcrt, tomando capturas periódicas.
    Espera Enter en CMD. Solo sale antes si detectar_error_pantalla devuelve True (ERROR CRÍTICO).
    """
    # (Implementación con logging DEBUG sin cambios funcionales)
    global ERRORS_DETECTED, DUMP_ERRORS, SBAR_DIALOG_ERRORS, WAIT_TIME, transacciones_con_error
    log_message(log_filename_func, f"DEBUG: Entrando wait_capture_... para {transaction_code}")
    print(f"\nTransacción {transaction_code} en pantalla."); prompt_message = "-> Presione ENTER en esta ventana (CMD) para continuar..."
    print(prompt_message); screenshot_counter = 0; error_occurred_while_waiting = False; exit_reason = "TIMEOUT_OR_UNKNOWN"
    while True:
        screenshot_counter += 1; screenshot_prefix = f"{transaction_code}_esperando_usuario_{screenshot_counter}"
        log_message(log_filename_func, f"DEBUG: Ciclo {screenshot_counter}, captura...")
        capture_screen(screenshot_prefix, log_filename_func)
        log_message(log_filename_func, f"DEBUG: Llamando detectar_error_pantalla...")
        error_detectado = detectar_error_pantalla() # Llama a la versión CORREGIDA
        log_message(log_filename_func, f"DEBUG: Resultado detectar_error_pantalla: {error_detectado}")
        if error_detectado: # Solo si es un error CRÍTICO según la nueva lógica
            log_message(log_filename_func, "¡ERROR CRÍTICO DETECTADO DURANTE ESPERA!"); print("\n¡ERROR CRÍTICO DETECTADO DURANTE ESPERA!")
            ERRORS_DETECTED = True; error_occurred_while_waiting = True
            if transaction_code not in transacciones_con_error: transacciones_con_error.append(transaction_code)
            log_message(log_filename_func, f"DEBUG: Llamando get_error_text..."); error_file = get_error_text_from_sap_gui(transaction_code, log_filename_func)
            if DUMP_ERRORS: log_message(log_filename_func, "DUMP. Llamando YBC..."); call_transaction_YBC_0007(transaction_code, log_filename_func)
            else: log_message(log_filename_func, "NO DUMP. No se llama YBC.")
            log_message(log_filename_func, f"DEBUG: Llamando cerrar_ventana_error..."); cerrar_ventana_error()
            exit_reason = "ERROR_DETECTED"; log_message(log_filename_func, f"DEBUG: Saliendo bucle por error detectado."); break
        # --- Bucle espera msvcrt ---
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Esperando {WAIT_TIME}s o presione ENTER en CMD...", end='\r')
        start_time = time.time(); enter_pressed_in_cmd = False
        while time.time() - start_time < WAIT_TIME:
            if msvcrt.kbhit():
                try:
                    char = msvcrt.getch(); log_message(log_filename_func, f"DEBUG: Tecla CMD: {char}")
                    if char == b'\r': enter_pressed_in_cmd = True; exit_reason = "ENTER_PRESSED"; log_message(log_filename_func, f"DEBUG: Enter CMD."); print(" " * 80, end='\r'); break
                    elif char == b'\x03': print("\nCtrl+C detectado. Saliendo..."); log_message(log_filename_func, "Ctrl+C detectado."); sys.exit(1)
                except Exception as e_getch: log_message(log_filename_func, f"DEBUG: Error msvcrt: {e_getch}"); break
            time.sleep(0.1)
        if enter_pressed_in_cmd: log_message(log_filename_func, f"DEBUG: Saliendo bucle por Enter."); break
        # else: log_message(log_filename_func, f"DEBUG: Timeout {WAIT_TIME}s.") # Log muy verboso
    # Fin while True
    print(" " * 80, end='\r'); log_message(log_filename_func, f"DEBUG: Saliendo wait_capture... Razón: {exit_reason}")
    if error_occurred_while_waiting: log_message(log_filename_func, "Retornando False (error detectado)"); return False
    elif enter_pressed_in_cmd: log_message(log_filename_func, "Retornando True (Enter CMD)"); return True
    else: log_message(log_filename_func, "ADVERTENCIA: Saliendo espera por razón desconocida."); return True # Fallback


def show_instructions_popup():
    """
    Displays a popup window with step-by-step instructions for running the SAP script.
    The popup includes instructions for connecting to the VPN, logging into QS4, editing the transactions file,
    navigating to the input directory, and running the script. The user is prompted to either continue or exit.
    If no response is given within 30 seconds, the script continues automatically.
    Returns:
        bool: True if the user chooses to continue or if the timeout occurs.
              Exits the script if the user chooses to exit.
    Logs:
        - Logs the display of instructions, user actions, timeouts, and any errors encountered.
    """
    """Muestra un popup con las instrucciones paso a paso"""
    # (Implementación sin cambios)
    global log_filename; log_message(log_filename, "Mostrando instrucciones..."); print("Mostrando instrucciones...")
    dialog_result = {"continue": False, "exit": False}; root = None
    def on_continue(): dialog_result["continue"] = True; root.quit()
    def on_exit(): dialog_result["exit"] = True; root.quit()
    def on_timeout():
        if not dialog_result["continue"] and not dialog_result["exit"]: log_message(log_filename, "Timeout diálogo."); print("Timeout diálogo. Continuando..."); dialog_result["continue"] = True
        try: root.quit()
        except: pass
    try:
        root = tk.Tk(); root.title("Script Prueba SAP"); root.attributes("-topmost", True)
        instructions =         instructions = """Paso a Paso
-----------------------------------------------------
1) Debe estar conectado a la VPN
2) Debe conectarse a QS4 con usuario/password
3) Editar transacciones.csv y agregar las transacciones a probar.
4) Ir al directorio C:\\Volar\\python\\input
5) Ejecutar python sap_ultimasmod.py

¿Desea continuar con la ejecución?
(Si no responde en 30 segundos, el script continuará automáticamente)"""
        frame = tk.Frame(root, padx=20, pady=20); frame.pack(fill="both", expand=True)
        tk.Label(frame, text=instructions, justify=tk.LEFT, padx=20, pady=20).pack()
        button_frame = tk.Frame(frame); button_frame.pack(pady=20)
        tk.Button(button_frame, text="Continuar", command=on_continue, width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Salir", command=on_exit, width=10).pack(side=tk.LEFT, padx=10)
        root.update_idletasks(); width=root.winfo_width(); height=root.winfo_height(); x=(root.winfo_screenwidth()//2)-(width//2); y=(root.winfo_screenheight()//2)-(height//2)
        root.geometry(f'{width}x{height}+{x}+{y}'); root.after(30000, on_timeout)
        try: root.mainloop()
        except Exception as e: log_message(log_filename, f"Error mainloop: {e}")
        try: root.destroy()
        except: pass
        if dialog_result["exit"]: log_message(log_filename, "Usuario salió popup."); print("Saliendo."); sys.exit(0)
        return True
    except Exception as e: log_message(log_filename, f"Error popup: {e}\n{traceback.format_exc()}"); print(f"Error popup: {e}"); return True


def create_initial_setup():
    """
    Creates the initial folder structure and an example CSV file required for the application.

    This function performs the following actions:
    - Creates the base directory, input directory, and output directory if they do not already exist.
    - Creates an example CSV file with predefined transaction entries if it does not exist.
    - Prints status messages for each operation performed.

    Returns:
        bool: True if the setup was completed successfully, False otherwise.
    """
    """Crea la estructura de carpetas inicial y el archivo CSV de ejemplo"""
    # (Implementación sin cambios)
    print("Configuración inicial..."); base_dir=r"C:\Volar\python"; input_dir=os.path.join(base_dir,"input"); output_dir=OUTPUT_FOLDER; csv_path=INPUT_CSV
    try:
        for dir_path in [base_dir, input_dir, output_dir]:
            if not os.path.exists(dir_path): print(f"Creando {dir_path}..."); os.makedirs(dir_path); print("Creada.")
            else: print(f"Carpeta {dir_path} ya existe.")
        if not os.path.exists(csv_path):
            print(f"Creando CSV {csv_path}...");
            with open(csv_path,'w',newline='',encoding='utf-8') as f: writer=csv.writer(f,delimiter=';'); writer.writerow(['Transaccion']); writer.writerow(['VA01']); writer.writerow(['YBC_0007']); writer.writerow(['SE38'])
            print("CSV Creado.")
        else: print(f"CSV {csv_path} ya existe.")
        print("Configuración inicial OK."); return True
    except Exception as e: print(f"Error setup inicial: {e}\n{traceback.format_exc()}"); return False


# --- Definición de main() ---
def main():
    """
    Función principal que orquesta la ejecución del script de automatización para pruebas en SAP GUI.
    Esta función realiza las siguientes tareas principales:
    - Crea la carpeta de salida para logs y capturas si no existe.
    - Inicializa el archivo de log y registra información relevante del entorno.
    - Verifica y crea la estructura inicial necesaria para la ejecución.
    - Muestra instrucciones al usuario y espera confirmación para iniciar.
    - Lee la lista de transacciones a procesar desde un archivo CSV.
    - Itera sobre cada transacción, abriéndola en SAP GUI y realizando capturas de pantalla.
    - Detecta errores inmediatos tras abrir cada transacción y registra los detalles en el log.
    - Permite al usuario confirmar la continuación tras cada transacción, o interrumpe en caso de error crítico.
    - Al finalizar, muestra un resumen de las transacciones procesadas y los errores detectados.
    Variables globales utilizadas:
    - ERRORS_DETECTED: Bandera para indicar si se detectaron errores durante la ejecución.
    - DUMP_ERRORS, SBAR_DIALOG_ERRORS: Flags de control de errores específicos.
    - transacciones_con_error: Lista de transacciones que presentaron errores.
    - log_filename: Ruta del archivo de log generado.
    Requiere que SAP GUI esté abierto y con sesión iniciada antes de comenzar.
    """
    """Función principal del script"""
    global ERRORS_DETECTED, DUMP_ERRORS, SBAR_DIALOG_ERRORS, transacciones_con_error, log_filename

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(OUTPUT_FOLDER):
         try: os.makedirs(OUTPUT_FOLDER); print(f"Carpeta {OUTPUT_FOLDER} creada.")
         except Exception as e_mkdir_main: print(f"ERROR CRÍTICO: No se pudo crear {OUTPUT_FOLDER}: {e_mkdir_main}"); sys.exit(1)
    log_filename = os.path.join(OUTPUT_FOLDER, f"log_sap_test_{timestamp}.txt")
    print(f"Archivo de log: {log_filename}")

    log_message(log_filename, "\n" + "="*30 + " INICIO SCRIPT " + "="*30)
    log_message(log_filename, f"Versión Python: {sys.version}") # Log inicial
    log_message(log_filename, f"Hora Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_message(log_filename, f"SAP GUI Scripting: {SAP_GUI_SCRIPTING_AVAILABLE}")
    log_message(log_filename, f"Tiempo Captura Periódica: {WAIT_TIME}s")

    transacciones_con_error = []

    log_message(log_filename, "\nVerificando/Creando estructura inicial...")
    if not create_initial_setup(): log_message(log_filename, "ERROR CRÍTICO: Falló setup. Saliendo."); return

    log_message(log_filename, "\nMostrando instrucciones...")
    if not show_instructions_popup(): return

    log_message(log_filename, "\nLeyendo CSV...")
    transacciones = leer_transacciones_csv(INPUT_CSV)
    if not transacciones: log_message(log_filename, f"ERROR: No hay transacciones válidas en {INPUT_CSV}."); return
    log_message(log_filename, f"{len(transacciones)} transacciones encontradas.")
    for i, trans in enumerate(transacciones, 1): log_message(log_filename, f"  {i}. {trans['codigo']}")

    print("\n¡ATENCIÓN! SAP GUI debe estar abierto y con sesión iniciada.");
    log_message(log_filename, "Esperando confirmación inicial...")
    input("Presiona Enter en CMD para iniciar la primera transacción...")
    log_message(log_filename, "Usuario confirmó inicio.")

    # --- Bucle Principal ---
    for index, transaccion in enumerate(transacciones, 1):
        transaction_code = transaccion['codigo']
        log_message(log_filename, f"\n--- INICIO TX {index}/{len(transacciones)}: {transaction_code} ---")
        print(f"\n--- PROCESANDO: {transaction_code} ({index}/{len(transacciones)}) ---")

        DUMP_ERRORS = False; SBAR_DIALOG_ERRORS = False # Reiniciar flags

        log_message(log_filename, "Pausa 5s y enfoque..."); print("Pausa 5s y enfoque..."); time.sleep(5)
        if focus_primary_monitor(): log_message(log_filename, "Enfocado.")
        else: log_message(log_filename, "WARN: Falló enfoque.")

        log_message(log_filename, f"Abriendo {transaction_code}...");
        try:
            pyautogui.hotkey('ctrl', 'n'); time.sleep(2)
            pyautogui.write(transaction_code); pyautogui.press('enter'); time.sleep(5)
        except Exception as e_pyauto:
             log_message(log_filename, f"ERROR FATAL pyautogui abriendo {transaction_code}: {e_pyauto}"); ERRORS_DETECTED = True; transacciones_con_error.append(transaction_code); continue

        log_message(log_filename, "Captura inicial..."); capture_screen(f"{transaction_code}_01_inicial", log_filename)

        log_message(log_filename, "Verificando errores inmediatos...")
        error_inmediato = False
        if detectar_error_pantalla(): # Usa la versión CORREGIDA que es menos sensible a sbar
            log_message(log_filename, "¡ERROR INMEDIATO DETECTADO (Título/Sbar Crítico)!")
            ERRORS_DETECTED = True; error_inmediato = True
            if transaction_code not in transacciones_con_error: transacciones_con_error.append(transaction_code)
            error_file = get_error_text_from_sap_gui(transaction_code, log_filename) # Captura detalles
            if DUMP_ERRORS: log_message(log_filename, "DUMP. Llamando YBC..."); call_transaction_YBC_0007(transaction_code, log_filename)
            else: log_message(log_filename, "NO DUMP. No se llama YBC.")
            cerrar_ventana_error()
        else: log_message(log_filename, "No hubo errores críticos inmediatos.")

        # Espera activa si no hubo error crítico inmediato
        if not error_inmediato:
            proceed = wait_capture_and_get_user_confirmation(transaction_code, log_filename)
            # proceed es True si Enter en CMD, False si error crítico detectado en la espera

        # --- Fin TX ---
        # Llamada a volver_pagina_principal() SIGUE COMENTADA
        log_message(log_filename,"### Volver a página principal DESACTIVADO ###")

        log_message(log_filename, f"--- FIN TX: {transaction_code} ---")
        print(f"--- FIN PROCESO PARA: {transaction_code} ---")

    # --- FIN BUCLE FOR ---

    # --- Mensaje Final ---
    print("\n" + "="*60); log_message(log_filename, "\n" + "="*60)
    if ERRORS_DETECTED:
        log_message(log_filename, "FINALIZACIÓN: SE DETECTARON ERRORES.")
        print("FINALIZACIÓN: SE DETECTARON ERRORES.")
        log_message(log_filename, "Transacciones con errores:")
        print("Transacciones con errores:")
        if transacciones_con_error:
            for trans_err in set(transacciones_con_error): log_message(log_filename, f"- {trans_err}"); print(f"- {trans_err}")
        else: log_message(log_filename, "- (Ninguna registrada)"); print("- (Ninguna registrada)")
        log_message(log_filename, f"Revisar log: {log_filename}"); log_message(log_filename, f"Y capturas en: {OUTPUT_FOLDER}"); print(f"Revisar log y carpetas en {OUTPUT_FOLDER}")
    else:
        log_message(log_filename, "FINALIZACIÓN: ¡Prueba completada sin errores detectados!")
        print("FINALIZACIÓN: ¡Prueba completada sin errores detectados!")
    log_message(log_filename, "="*60 + "\n"); print("="*60)


# --- Bloque de ejecución principal ---
if __name__ == "__main__":
    log_filename_main = os.path.join(OUTPUT_FOLDER, f"log_sap_test_main_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    try:
        print("Iniciando script SAP Automation...")
        if not os.path.exists(OUTPUT_FOLDER):
             try: os.makedirs(OUTPUT_FOLDER)
             except Exception as e_mkdir_main: print(f"ERROR CRÍTICO: No se pudo crear {OUTPUT_FOLDER}: {e_mkdir_main}"); sys.exit(1)
        log_message(log_filename_main, "Script iniciado desde __main__.")
        main()
    except KeyboardInterrupt:
        print("\nScript interrumpido (Ctrl+C).")
        log_to_use = log_filename if 'log_filename' in globals() and log_filename and os.path.exists(os.path.dirname(log_filename)) else log_filename_main
        if os.path.exists(os.path.dirname(log_to_use)): log_message(log_to_use, "Interrumpido (Ctrl+C).")
    except Exception as e:
        print(f"\nError fatal INESPERADO __main__: {e}"); details = traceback.format_exc(); print("Detalles:", details)
        log_to_use = log_filename if 'log_filename' in globals() and log_filename and os.path.exists(os.path.dirname(log_filename)) else log_filename_main
        if os.path.exists(os.path.dirname(log_to_use)):
             log_message(log_to_use, f"Error fatal __main__: {e}\n{details}")
             capture_screen("error_fatal_main", log_to_use)
    finally:
        print("\n\nScript finalizado. Ventana abierta."); print("Presiona Ctrl+C para cerrar.")
        log_to_use = log_filename if 'log_filename' in globals() and log_filename and os.path.exists(os.path.dirname(log_filename)) else log_filename_main
        if os.path.exists(os.path.dirname(log_to_use)): log_message(log_to_use, "Bloque finally. Esperando Ctrl+C...")
        try:
            while True: time.sleep(10) # Mantener ventana
        except KeyboardInterrupt:
            print("\nVentana cerrada.")
            if os.path.exists(os.path.dirname(log_to_use)): log_message(log_to_use, "Ventana cerrada.")