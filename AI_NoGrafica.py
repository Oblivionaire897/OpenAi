import tkinter as tk #User interface
from tkinter import simpledialog 
from tkinter import scrolledtext
from tkinter import font
from tkinter import Menu
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import colorchooser
from openai import OpenAI
import PyTaskbar
import ctypes
import fitz
import os
import threading
import time
import json

def invio_messaggio():

    user_message = user_input_var.get()
    if user_message.lower() == "stop":
        if messagebox.askyesno("Spegnimento", "Sei sicuro di voler uscire?"):
            root.quit()
        else:
            return
    else:
        chat_history.append({"role": "user", "content": user_message})
        Aggiorna_textbox("Tu: " + user_message, "user")
        lista_esportare.append({"role": "user", "content": user_message})
        user_input_var.set("")

        user_input_entry.configure(state="disabled")
        send_button.configure(state="disabled")
        user_input_entry.unbind("<Return>")
        user_input_entry.grid_forget()
        waiting_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        loading_thread = threading.Thread(target=loading_animation)
        loading_thread.start()
        root.iconbitmap(os.path.join(os.path.dirname(__file__), "Icone", "fumetto_puntini.ico"))
        prog.setState('loading')
        full_response = ""
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=chat_history,
                stream=True,
                temperature=api_settings["temperature"],
                max_tokens=api_settings["tokens"]
            )
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
        except Exception as e:
                Aggiorna_textbox("Errore API: " + str(e), "system")

        lista_esportare.append({"role": "Chat-GPT", "content": full_response})

        stop_loading.set()
        loading_thread.join()
        root.iconbitmap(os.path.join(os.path.dirname(__file__), "Icone", "fumetto.ico"))
        prog.setState("normal")

        if full_response:
            Aggiorna_textbox("OpenAI: " + full_response, "assistant")
            chat_history.append({"role": "assistant", "content": full_response})

        waiting_label.grid_forget()
        user_input_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        user_input_entry.configure(state="normal")
        send_button.configure(state="normal")
        user_input_entry.bind("<Return>", Invio)

def loading_animation():
    messages = ["S", "St", "Sti", "Stia", "Stiam", "Stiamo",
                "Stiamo g", "Stiamo ge", "Stiamo gen", "Stiamo gene", "Stiamo gener", "Stiamo genera", "Stiamo generan", "Stiamo generand", "Stiamo generando",
                "Stiamo generando l", "Stiamo generando la",
                "Stiamo generando la t", "Stiamo generando la tu", "Stiamo generando la tua",
                "Stiamo generando la tua r", "Stiamo generando la tua ri", "Stiamo generando la tua ris", "Stiamo generando la tua risp", "Stiamo generando la tua rispo", "Stiamo generando la tua rispos", "Stiamo generando la tua rispost", "Stiamo generando la tua risposta",
                "Stiamo generando la tua risposta.", "Stiamo generando la tua risposta..", "Stiamo generando la tua risposta..."]
    i = 0

    while not stop_loading.is_set():
        Aggiorna_textbox(messages[i % len(messages)], "loading")
        time.sleep(0.05)
        text_area.configure(state="normal")
        text_area.delete("end-2l", "end-1l")
        text_area.configure(state="disabled")
        i += 1

    stop_loading.set()


def Aggiorna_textbox(message, tag):
    log_message(tag, message)
    text_area.configure(state="normal")
    text_area.insert(tk.END, message + "\n", tag)
    text_area.see(tk.END)
    text_area.configure(state="disabled")

def Invio(event=None):
    global stop_loading
    stop_loading = threading.Event()
    threading.Thread(target=invio_messaggio).start()

def ConfigureAPI():
    while True:
        api_key = simpledialog.askstring("Chi sei?", "Inserisci la chiave API:", parent=root, )

        global client
        
        client = OpenAI(api_key=api_key)
        if verifica_api_key():
            break
        else:
            messagebox.showerror("Errore", "API key errata. Prova a ricontrollarla.")
        

def estrai_testo_da_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def NuovaChat():
    text_area.configure(state="normal")
    text_area.delete("1.0", tk.END)
    text_area.configure(state="disabled")

    finestra_SystemMessage = tk.Toplevel(root)
    finestra_SystemMessage.title("Chi sono io")
    finestra_SystemMessage.geometry("500x100")

    frame = tk.Frame(finestra_SystemMessage)
    frame.pack(pady=10, padx=10, fill=tk.X, expand=True)

    tk.Label(frame, text="Inserisci il messaggio di sistema o carica da un file PDF:").pack(anchor="w")

    text_var = tk.StringVar()
    text_entry = tk.Entry(frame, textvariable=text_var, width=40)
    text_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
    text_entry.bind("<Return>", lambda event: submit())

    def submit():
        input_text = text_var.get()
        if input_text:
            system_message = input_text
            chat_history.insert(0, {"role": "system", "content": system_message + "Non usare per nessun motivo emoji nei messaggi."})
            finestra_SystemMessage.destroy()
        else:
            messagebox.showwarning("Attenzione", "Nessun testo inserito. Riprova.")

    def load_file():
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            system_message = estrai_testo_da_pdf(file_path)
            text_var.set(system_message)
            submit()

    load_button = tk.Button(frame, text="Carica File", command=load_file)
    load_button.pack(side="right")

def verifica_api_key():
    try:
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Rispondi al test."}
            ],
            temperature=0.7,
            max_tokens=5,
        )
        return True
    except Exception as e:
        print(e)
        messagebox.showerror("Errore di Connessione", f"Errore durante la connessione all'API: {e}")
        return False

def esporta_chat_pdf():
    file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Please select a file name for saving:", filetypes=[("PDF files", "*.pdf")])

    chat = fitz.open()
    pagina = chat.new_page()

    margine_x = 36
    margine_y = 36
    larghezza_pagina = 595
    altezza_riga = 13.8
    font = "helv"
    dimensione_font = 11
    larghezza_testo = larghezza_pagina - 2 * margine_x

    y = margine_y

    for item in lista_esportare:
        if item['role'] == "user":
                role = "Tu:"
        else:
            if item['role'] == "assistant":
                role = "Chat-GPT" 
        content = item['content']
        testo_slice = f'{role} {content}'

        text_color = (0.19, 0.68, 0.47) if role == "Chat-GPT:" else (0, 0, 0)

        words = testo_slice.split()
        wrapped_lines = []
        line = ""
        for word in words:
            if fitz.get_text_length(line + " " + word, font, dimensione_font) < larghezza_testo:
                line += " " + word if line else word
            else:
                wrapped_lines.append(line)
                line = word
        if line:
            wrapped_lines.append(line)

        for wrapped_line in wrapped_lines:
            pagina.insert_text((margine_x, y), text=wrapped_line, fontname=font, fontsize=dimensione_font, color=text_color)
            y += altezza_riga
            if y > (792 - margine_y):
                pagina = chat.new_page()
                y = margine_y

    chat.save(f"{file_path}.pdf")
    chat.close()
    messagebox.showinfo("Successo", "Chat esportata correttamente in PDF.")

def esporta_chat_testo():
    file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Please select a file name for saving:", filetypes=[("Text files", "*.txt")])
    file_path += ".txt"
    with open(file_path, 'w') as file:
        for item in lista_esportare:
            if item['role'] == "user":
                role = "Tu:"
            else:
                if item['role'] == "assistant":
                    role = "Chat-GPT" 
            content = item['content']
            file.write(f"{role} {content}\n")
    messagebox.showinfo("Successo", "Chat esportata correttamente in formato testuale.")

def esporta_chat_json():
    file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Please select a file name for saving:", filetypes=[("JSON files", "*.json")])
    file_path += ".json"
    with open(file_path, 'w') as file:
        json.dump(lista_esportare, file, indent=4)
    messagebox.showinfo("Successo", "Chat esportata correttamente in formato JSON.")

def log_message(role, message):
    with open("chat_log.txt", "a") as file:
        file.write(f"{role}: {message}\n")

def set_theme(theme):
    global font_colore_ai, font_colore_user, background_color_var

    if theme == 'Ocean':
        style.configure('.', background='#01547E', foreground='white', font=(Roboto, 12))
        style.configure('TButton', background='#2E8BC0', foreground='white')
        style.configure('TLabel', background='#224870', foreground='white')
        style.configure('TEntry', fieldbackground='#224870', foreground='white')

        font_colore_ai = "#00FFFF"
        font_colore_user = "#FFA500"
        background_color_var = "#ADD8E6"

    elif theme == 'Scuro':
        style.configure('.', background='#333333', foreground='white', font=(Roboto, 12))
        style.configure('TButton', background='#555555', foreground='white')
        style.configure('TLabel', background='#333333', foreground='white')
        style.configure('TEntry', fieldbackground='#333333', foreground='white')

        font_colore_ai = "#00FFFF"
        font_colore_user = "#FFA500"
        background_color_var = "#ADD8E6"

    elif theme == 'Verde':
        style.configure('.', background='#2F4F2F', foreground='white', font=(Roboto, 12))
        style.configure('TButton', background='#8FBC8F', foreground='white')
        style.configure('TLabel', background='#2F4F2F', foreground='white')
        style.configure('TEntry', fieldbackground='#2F4F2F', foreground='white')

        font_colore_ai = "#00FFFF"
        font_colore_user = "#FFA500"
        background_color_var = "#ADD8E6"

    elif theme == "Classic":
        style.configure('.', background='#FFFFFF', foreground='black', font=(Roboto, 12))
        style.configure('TButton', background='#FFFFFF', foreground='black')
        style.configure('TLabel', background='#FFFFFF', foreground='black')
        style.configure('TEntry', fieldbackground='#FFFFFF', foreground='black')

        font_colore_ai = "#008000"
        font_colore_user = "#000000"
        background_color_var = "#808080"
        
    refresh_ui()

def refresh_ui():
    text_area.configure(background=style.lookup('.', 'background'),
                        foreground=style.lookup('.', 'foreground'),
                        font=style.lookup('.', 'font'))
    user_input_entry.configure(background=style.lookup('TEntry', 'fieldbackground'),
                            foreground=style.lookup('TEntry', 'foreground'))
    send_button.configure(background=style.lookup('TButton', 'background'),
                        foreground=style.lookup('TButton', 'foreground'))
    
    text_area.tag_configure("assistant", foreground=font_colore_ai)
    text_area.tag_configure("user", foreground=font_colore_user)
    text_area.tag_configure("system", foreground=background_color_var)
    text_area.tag_configure("loading", foreground=background_color_var)

def setup_shortcuts():
    root.bind('<Control-n>', lambda event: NuovaChat())
    root.bind('<Control-k>', lambda event: ConfigureAPI())
    root.bind('<Control-q>', lambda event: root.quit())

def change_color(tag):
    color = colorchooser.askcolor()[1]
    if tag == "ai":
        global font_colore_ai
        font_colore_ai = color
    elif tag == "user":
        global font_colore_user
        font_colore_user = color
    refresh_ui()

def personalizza():
    finestra_personalizza = tk.Toplevel(root)
    finestra_personalizza.title("Personalizza")
    finestra_personalizza.geometry("400x300")
    finestra_personalizza.resizable(False, False)
    finestra_personalizza.iconbitmap(os.path.join(os.path.dirname(__file__), "Icone", "pennello.ico"))

    def change_font():
        font_family = font_family_var.get()
        font_size = font_size_var.get()
        text_area.config(font=(font_family, font_size))
        user_input_entry.config(font=(font_family, font_size))

    font_frame = tk.LabelFrame(finestra_personalizza, text="Font")
    font_frame.pack(fill="x", padx=10, pady=10)

    font_family_var = tk.StringVar(value="Arial")
    font_size_var = tk.IntVar(value=10)

    font_families = list(font.families())

    tk.Label(font_frame, text="Tipo di Font:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    tk.OptionMenu(font_frame, font_family_var, *font_families).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(font_frame, text="Dimensione:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    tk.Spinbox(font_frame, from_=6, to=60, textvariable=font_size_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    tk.Button(font_frame, text="Conferma", command=change_font).grid(row=2, column=0, columnspan=2, pady=10)
    color_frame = tk.LabelFrame(finestra_personalizza, text="Colori")
    color_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(color_frame, text="Colore AI:").grid(row=0, column=0, padx=5, pady=5)
    tk.Button(color_frame, text="Cambia", command=lambda: change_color("ai")).grid(row=0, column=1, padx=5, pady=5)

    tk.Label(color_frame, text="Colore Utente:").grid(row=1, column=0, padx=5, pady=5)
    tk.Button(color_frame, text="Cambia", command=lambda: change_color("user")).grid(row=1, column=1, padx=5, pady=5)

def ImpostazioniAPI():
    def update_tokens_temperature():
        try:
            tokens = int(tokens_entry.get())
            temperature = float(temperature_entry.get())
            api_settings["tokens"] = tokens
            api_settings["temperature"] = temperature
            with open('00_api_settings.json', 'w') as file:
                json.dump(api_settings, file)
            messagebox.showinfo("Successo", "Impostazioni API aggiornate con successo.")
        except ValueError:
            messagebox.showerror("Errore", "Valori non validi. Assicurati di inserire numeri validi.")
            ImpostazioniAPI()
    finestra_api = tk.Toplevel(root)
    finestra_api.iconbitmap(os.path.join(os.path.dirname(__file__), "Icone", "pennello.ico"))
    finestra_api.title("Impostazioni API")
    finestra_api.geometry("300x200")

    tk.Label(finestra_api, text="Max Tokens:").pack(pady=5)
    tokens_entry = tk.Entry(finestra_api)
    tokens_entry.pack(pady=5)
    tokens_entry.insert(0, api_settings.get("tokens", 300))
    tk.Label(finestra_api, text="Temperature:").pack(pady=5)
    temperature_entry = tk.Scale(finestra_api, from_=0, to=2, orient="horizontal", resolution=0.1)
    temperature_entry.pack(pady=5)
    temperature_entry.set(api_settings.get("temperature", 0.7))

    tk.Button(finestra_api, text="Aggiorna", command=update_tokens_temperature).pack(pady=10)

def reset():
    global lista_esportare
    global chat_history
    if messagebox.askyesno("Clear Chat", "Sei sicuro di voler eliminare tutta la chat?"):
        lista_esportare.clear()
        chat_history = [chat_history[0]]
        text_area.configure(state="normal")
        text_area.delete("1.0", tk.END)
        text_area.configure(state="disabled")

def get_tkinter_window_handle(window):
    window.update_idletasks()
    window_id = window.winfo_id()
    hwnd = ctypes.windll.user32.GetParent(window_id)
    return hwnd

chat_history = []
lista_esportare=[]

root = tk.Tk()
root.lift()
root.iconbitmap(default = os.path.join(os.path.dirname(__file__), "Icone", "interrogativo.ico"))
root.iconbitmap(os.path.join(os.path.dirname(__file__), "Icone", "fumetto.ico"))
style = ttk.Style(root)
available_themes = style.theme_names()
style.theme_use('default')

hwnd = get_tkinter_window_handle(root)

root.title("Chat magika con AI")
Roboto = font.Font(family="Roboto", size=11)
root.option_add("*Font", Roboto)

ConfigureAPI()

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)

menu = Menu(root)
root.config(menu=menu)
file_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Chat", menu=file_menu)
file_menu.add_command(label="Nuova Chat", command=NuovaChat)
file_menu.add_command(label="Reset Conversazione", command=reset)
file_menu.add_command(label="Cambia API Key", command=ConfigureAPI)
file_menu.add_separator()
export_menu = tk.Menu(root, tearoff=0)
export_menu.add_command(label="Esporta in PDF", command=esporta_chat_pdf)
export_menu.add_command(label="Esporta in TXT", command=esporta_chat_testo)
export_menu.add_command(label="Esporta in JSON", command=esporta_chat_json)
file_menu.add_cascade(label="Esporta Chat", menu=export_menu)
file_menu.add_separator()
file_menu.add_command(label="Esci", command=root.quit)

theme_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Personalizzazione", menu=theme_menu)
theme_menu.add_command(label="Classic", command=lambda: set_theme("Classic"))
theme_menu.add_command(label="Ocean", command=lambda: set_theme("Ocean"))
theme_menu.add_command(label="Scuro", command=lambda: set_theme("Scuro"))
theme_menu.add_command(label="Verde", command=lambda: set_theme("Verde"))
theme_menu.add_separator()
theme_menu.add_command(label="Impostazioni API", command=ImpostazioniAPI)
theme_menu.add_command(label="Personalizza", command=personalizza)

text_area = scrolledtext.ScrolledText(root, height=20, width=50, state="disabled", wrap=tk.WORD, padx=10, pady=10)
text_area.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

font_colore_ai = "#008000"
font_colore_user = "#000000"
background_color_var = "#808080"

text_area.tag_configure("assistant", foreground=font_colore_ai)
text_area.tag_configure("user", foreground=font_colore_user)
text_area.tag_configure("system", foreground=background_color_var)
text_area.tag_configure("loading", foreground=background_color_var)

user_input_var = tk.StringVar()
user_input_entry = tk.Entry(root, textvariable=user_input_var)
user_input_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
user_input_entry.bind("<Return>", Invio)

waiting_label = tk.Label(root, text="Aspetta che l'AI finisca", font=(Roboto, 12))

immagine_bottone = PhotoImage(file=os.path.join(os.path.dirname(__file__), "Icone", "Invio.png"))
send_button = tk.Button(root, image=immagine_bottone, text=" Invia", command=Invio, compound=tk.LEFT)
send_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

api_settings = {'temperature': 0.7, 'tokens': 50} #Sono i predefiniti. Non cancellare questa riga

prog = PyTaskbar.Progress(hwnd=hwnd)
prog.init()

setup_shortcuts()

NuovaChat()

root.mainloop()