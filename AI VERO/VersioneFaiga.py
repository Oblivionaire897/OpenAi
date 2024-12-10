import customtkinter
from tkinter import filedialog
from openai import OpenAI

import tkinter as tk
from tkinter import simpledialog
from tkinter import scrolledtext
from tkinter import font
from tkinter import Menu
from tkinter import messagebox
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

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CHAT GPT FIGO PAZZO SGRAVATO")
        self.geometry(f"{1000}x{700}")
        self.wm_attributes('-fullscreen', False)
        self.state('normal')


        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Left Sidebar
        self.frame_left_sidebar = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.frame_left_sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.frame_left_sidebar.grid_rowconfigure(5, weight=1)

        self.logo_label_left = customtkinter.CTkLabel(self.frame_left_sidebar, text="OpenAIO", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label_left.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Primo frame: Api key e system message
        self.frame_inputs = customtkinter.CTkFrame(self.frame_left_sidebar)
        self.frame_inputs.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="nsew")
        
        self.api_key_label = customtkinter.CTkLabel(self.frame_inputs, text="API Key:")
        self.api_key_label.grid(row=0, column=0, padx=10, pady=(10, 0))
        
        self.api_key_frame = customtkinter.CTkFrame(self.frame_inputs)
        self.api_key_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.api_key_frame.grid_columnconfigure(0, weight=1)

        self.api_key_input = customtkinter.CTkEntry(self.api_key_frame, width=150)
        self.api_key_input.grid(row=0, column=0, sticky="ew")

        self.confirm_button = customtkinter.CTkButton(self.api_key_frame, text="OK", width=40, command=self.conferma_apikey)
        self.confirm_button.grid(row=0, column=1, padx=(5, 0))

        self.file_input_label = customtkinter.CTkLabel(self.frame_inputs, text="File Input:")
        self.file_input_label.grid(row=2, column=0, padx=10, pady=(10, 0))
        
        self.file_input = customtkinter.CTkButton(self.frame_inputs, text="Choose File", command=self.file_input_event)
        self.file_input.grid(row=3, column=0, padx=10, pady=(0, 10))

        self.or_label = customtkinter.CTkLabel(self.frame_inputs, text="oppure")
        self.or_label.grid(row=4, column=0, padx=10, pady=(0, 10))
        
        self.text_area = customtkinter.CTkTextbox(self.frame_inputs, height=100)
        self.text_area.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.confirm_file_button = customtkinter.CTkButton(self.frame_inputs, text="Conferma", command=self.confirm_file_event)
        self.confirm_file_button.grid(row=6, column=0, padx=10, pady=(0, 10))

        # Secondo frame: Reset, Reset 2, Esporta
        self.frame_buttons = customtkinter.CTkFrame(self.frame_left_sidebar)
        self.frame_buttons.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.frame_buttons.grid_columnconfigure(0, weight=1)

        self.sidebar_button_1 = customtkinter.CTkButton(self.frame_buttons, text="Reset", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.sidebar_button_2 = customtkinter.CTkButton(self.frame_buttons, text="Reset 2", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.export_optionmenu = customtkinter.CTkOptionMenu(self.frame_buttons, values=["TXT", "JSON", "PDF"], command=self.export_option_event)
        self.export_optionmenu.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.export_optionmenu.set("Esporta")

        # Esci
        self.free_button = customtkinter.CTkButton(self.frame_left_sidebar, text="Esci", command=self.exit_button_event)
        self.free_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Right Sidebar
        self.frame_right_sidebar = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.frame_right_sidebar.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.frame_right_sidebar.grid_rowconfigure(4, weight=1)

        # tabview
        self.tabview = customtkinter.CTkTabview(self.frame_right_sidebar, width=200, height=150)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.add("Temi")
        self.tabview.add("Manuale")
        self.tabview.tab("Temi").grid_columnconfigure(0, weight=1) 
        self.tabview.tab("Manuale").grid_columnconfigure(0, weight=1)

        # Tab Temi
        self.pulsante_chiaro = customtkinter.CTkButton(self.tabview.tab("Temi"), text="Tema Chiaro", command=lambda: self.change_theme("light"))
        self.pulsante_chiaro.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.pulsante_scuro = customtkinter.CTkButton(self.tabview.tab("Temi"), text="Tema Scuro", command=lambda: self.change_theme("dark"))
        self.pulsante_scuro.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.pulsante_ocean = customtkinter.CTkButton(self.tabview.tab("Temi"), text="Tema Ocean", command=lambda: self.change_theme("ocean"))
        self.pulsante_ocean.grid(row=2, column=0, padx=20, pady=(20, 10))

        self.pulsante_green = customtkinter.CTkButton(self.tabview.tab("Temi"), text="Tema Verde", command=lambda: self.change_theme("green"))
        self.pulsante_green.grid(row=3, column=0, padx=20, pady=(20, 10))

        # Nuovo box per temperature e tokens
        self.frame_parameters = customtkinter.CTkFrame(self.frame_right_sidebar)
        self.frame_parameters.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")

        self.temperature_label = customtkinter.CTkLabel(self.frame_parameters, text="Temperature:")
        self.temperature_label.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.temperature_slider = customtkinter.CTkSlider(self.frame_parameters, from_=0.1, to=2.0, number_of_steps=20)
        self.temperature_slider.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.tokens_label = customtkinter.CTkLabel(self.frame_parameters, text="Tokens:")
        self.tokens_label.grid(row=2, column=0, padx=10, pady=(10, 0))

        self.tokens_input = customtkinter.CTkEntry(self.frame_parameters, width=100)
        self.tokens_input.grid(row=3, column=0, padx=10, pady=(0, 10))

        self.confirm_parameters_button = customtkinter.CTkButton(self.frame_parameters, text="Conferma", command=self.confirm_parameters_event)
        self.confirm_parameters_button.grid(row=4, column=0, padx=10, pady=(10, 10))

        # Personalizzazione manuale

        self.color_customization_frame = customtkinter.CTkFrame(self.tabview.tab("Manuale"))
        self.color_customization_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")

        self.question_color_label = customtkinter.CTkLabel(self.color_customization_frame, text="Colore delle Domande:")
        self.question_color_label.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.question_color_button = customtkinter.CTkButton(self.color_customization_frame, text="Scegli Colore")
        self.question_color_button.grid(row=1, column=0, padx=10, pady=(0, 10))

        self.background_color_label = customtkinter.CTkLabel(self.color_customization_frame, text="Colore dello Sfondo:")
        self.background_color_label.grid(row=2, column=0, padx=10, pady=(10, 0))

        self.background_color_button = customtkinter.CTkButton(self.color_customization_frame, text="Scegli Colore")
        self.background_color_button.grid(row=3, column=0, padx=10, pady=(0, 10))

        self.box_color_label = customtkinter.CTkLabel(self.color_customization_frame, text="Colore dei Box:")
        self.box_color_label.grid(row=4, column=0, padx=10, pady=(10, 0))

        self.box_color_button = customtkinter.CTkButton(self.color_customization_frame, text="Scegli Colore")
        self.box_color_button.grid(row=5, column=0, padx=10, pady=(0, 10))

        self.sidebar_color_label = customtkinter.CTkLabel(self.color_customization_frame, text="Colore delle Sidebar:")
        self.sidebar_color_label.grid(row=6, column=0, padx=10, pady=(10, 0))

        self.sidebar_color_button = customtkinter.CTkButton(self.color_customization_frame, text="Scegli Colore")
        self.sidebar_color_button.grid(row=7, column=0, padx=10, pady=(0, 10))

        self.confirm_colors_button = customtkinter.CTkButton(self.color_customization_frame, text="Conferma Colori")
        self.confirm_colors_button.grid(row=8, column=0, padx=10, pady=(10, 10))

        # Center Text Area and Input
        self.center_frame = customtkinter.CTkFrame(self, corner_radius=3)
        self.center_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="nsew")
        self.center_frame.grid_rowconfigure(0, weight=1)
        self.center_frame.grid_columnconfigure(0, weight=1)

        self.text_display = customtkinter.CTkTextbox(self.center_frame, state="disabled", wrap="word")
        self.text_display.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")

        self.input_frame = customtkinter.CTkFrame(self.center_frame, corner_radius = 500)
        self.input_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.text_input = customtkinter.CTkEntry(self.input_frame)
        self.text_input.grid(row=0, column=0, padx=(0, 10), pady=(0, 0), sticky="ew")

        self.send_button = customtkinter.CTkButton(self.input_frame, text="Invia", command=self.invio_messaggio)
        self.send_button.grid(row=0, column=1, pady=(0, 0), sticky="e")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def file_input_event(self):
        file_path = filedialog.askopenfilename()
        print(f"File selected: {file_path}")

    def confirm_file_event(self):
        file_path = filedialog.askopenfilename()
        print(f"File confirmed: {file_path}")

    def verifica_apikey(apikey):
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
            messagebox.showerror("Errore di Connessione", f"Errore durante la connessione all'API: {e}")
            return False
        
    def conferma_apikey(self):
        api_key = self.api_key_input.get()

        global client

        if api_key == "Steam":
            api_key = "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"
            client = OpenAI(api_key=api_key)
        else:
            client = OpenAI(api_key=api_key)

        if self.verifica_apikey():
            messagebox.showinfo("Conferma", "API key valida")
        else:
            messagebox.showerror("Errore", "API key errata. Prova a ricontrollarla.")
    
    def invio_messaggio(self):

        message = self.text_input.get()
        if message:
            self.text_display.configure(state="normal")
            self.text_display.insert("end", f"You: {message}\n")
            self.text_display.configure(state="disabled")
            self.text_input.delete(0, "end")
        
        if message.lower() == "stop":
            if messagebox.askyesno("Spegnimento", "Sei sicuro di voler uscire?"):
                app.quit()
            else:
                return
        else:
            chat_history.append({"role": "user", "content": message})

            self.text_input.configure(state="disabled")
            self.send_button.configure(state="disabled")
            self.user_input_entry.unbind("<Return>")
            self.user_input_entry.grid_forget()
            self.waiting_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

            loading_thread = threading.Thread(target=loading_animation)
            loading_thread.start()
            app.iconbitmap(os.path.join(os.path.dirname(__file__), "Icone", "fumetto_puntini.ico"))
            full_response = ""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=chat_history,
                stream=True,
                temperature=self.api_settings["temperature"],
                max_tokens=self.api_settings["tokens"]
            )
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content

            self.stop_loading.set()
            loading_thread.join()
            app.iconbitmap(os.path.join(os.path.dirname(__file__), "Icone", "fumetto.ico"))

            if full_response:
                self.text_display.configure(state="normal")
                self.text_display.insert("end", f"AI: {full_response}\n")
                self.text_display.configure(state="disabled")

            self.waiting_label.grid_forget()
            self.user_input_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
            self.user_input_entry.configure(state="normal")
            self.send_button.configure(state="normal")
            self.user_input_entry.bind("<Return>", self.send_button)

        def loading_animation(self):
            messages = ["S", "St", "Sti", "Stia", "Stiam", "Stiamo",
                        "Stiamo g", "Stiamo ge", "Stiamo gen", "Stiamo gene", "Stiamo gener", "Stiamo genera", "Stiamo generan", "Stiamo generand", "Stiamo generando",
                        "Stiamo generando l", "Stiamo generando la",
                        "Stiamo generando la t", "Stiamo generando la tu", "Stiamo generando la tua",
                        "Stiamo generando la tua r", "Stiamo generando la tua ri", "Stiamo generando la tua ris", "Stiamo generando la tua risp", "Stiamo generando la tua rispo", "Stiamo generando la tua rispos", "Stiamo generando la tua rispost", "Stiamo generando la tua risposta",
                        "Stiamo generando la tua risposta.", "Stiamo generando la tua risposta..", "Stiamo generando la tua risposta..."]
            i = 0

            while not self.stop_loading.is_set():
                self.text_display.configure(state="normal")
                self.text_display.insert(messages[i % len(messages)], "loading")
                time.sleep(0.05)
                self.text_display.configure(state="disabled")
                self.text_input.delete(0, "end")
                i += 1

    def export_option_event(self, choice):
        print(f"Selected export option: {choice}")
       

    def change_theme(self, theme):
        if theme == "light":
            customtkinter.set_appearance_mode("Light")
        elif theme == "dark":
            customtkinter.set_appearance_mode("Dark")
        elif theme == "ocean":
            customtkinter.set_default_color_theme("blue")
        elif theme == "green":
            customtkinter.set_default_color_theme("green")

    def confirm_parameters_event(self):
        temperature = self.temperature_slider.get()
        tokens = self.tokens_input.get()
        print(f"Temperature confirmed: {temperature}")
        print(f"Tokens confirmed: {tokens}")

    def exit_button_event(self):
        self.quit()

if __name__ == "__main__":

    chat_history = []

    app = App()
    app.mainloop()
