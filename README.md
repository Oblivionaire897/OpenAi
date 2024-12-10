# Chat Magika con AI

## Descrizione
**Chat Magika con AI** è un'applicazione Python con interfaccia grafica (GUI) che consente di interagire con un'intelligenza artificiale OpenAI. L'app offre funzioni per la gestione di conversazioni, esportazione di dati e personalizzazione visiva, garantendo un'esperienza interattiva e personalizzabile.

---

## Funzionalità Principali
- 🧠 **Interazione con AI**: Chatta con un modello GPT tramite API OpenAI.
- 📂 **Esportazione**: Salva le conversazioni in **PDF**, **TXT** o **JSON**.
- 🎨 **Personalizzazione Tema**: Cambia tema (Classic, Ocean, Scuro, Verde) o definisci i colori manualmente.
- ✍️ **Modifica Font**: Personalizza stile e dimensione del testo.
- 🔑 **Gestione API**: Configura chiave API e parametri avanzati (es. temperatura e token massimi).
- 🔄 **Supporto Multithreading**: Animazione di caricamento durante l'elaborazione delle risposte.
- ⌨️ **Shortcut da Tastiera**: Esegui azioni rapide con combinazioni di tasti (es. nuova chat o modifica API key).

---

## Dipendenze
### Librerie Python
- **tkinter**: Per la gestione della GUI.
- **fitz (PyMuPDF)**: Per la manipolazione e lettura dei file PDF.
- **openai**: Per la comunicazione con le API OpenAI.
- **PyTaskbar**: Per l'integrazione con la barra delle applicazioni su Windows.
- **json, os, time, threading, ctypes**: Librerie standard di Python.

---

## Configurazione Iniziale
1. Assicurati di avere una chiave API OpenAI valida.
2. Inserisci la chiave al primo avvio oppure tramite la voce di menu `Cambia API Key`.

---

## Come Utilizzarlo
### Interazione con AI
1. Inserisci il tuo messaggio nel campo di input.
2. Premi **Invia** o utilizza il tasto **Enter**.
3. La risposta dell'AI verrà mostrata nell'area di testo principale.

### Esportazione della Chat
- Vai su `Chat > Esporta Chat` e seleziona il formato desiderato:
  - **PDF**: Genera un documento con la conversazione.
  - **TXT**: Esporta come file di testo semplice.
  - **JSON**: Salva in formato strutturato per elaborazioni future.

### Personalizzazione
- Cambia il tema andando su `Personalizzazione > Cambia Tema`.
- Modifica font e colori tramite `Personalizzazione > Personalizza`.

### Configurazione API
- Cambia la chiave API tramite `Chat > Cambia API Key`.
- Imposta i parametri di temperatura e token massimi tramite `Personalizzazione > Impostazioni API`.

---

## Shortcut da Tastiera
- **Ctrl + N**: Avvia una nuova chat.
- **Ctrl + K**: Cambia la chiave API.
- **Ctrl + Q**: Chiudi l'applicazione.

---

## Struttura dell'Interfaccia
- **Area di Testo Principale**: Mostra la cronologia della conversazione.
- **Campo di Input**: Inserisci il messaggio da inviare.
- **Pulsanti**: Per inviare messaggi o interagire con l'applicativo.
- **Menu**:
  - **Chat**: Nuova chat, reset, cambio API Key, esportazione.
  - **Personalizzazione**: Cambia tema, font e colori.

---

## Requisiti di Sistema
- **Sistema Operativo**: Windows (consigliato per PyTaskbar), adattabile ad altri OS.
- **Python**: Versione 3.7 o superiore.
- **Librerie**: Installabili tramite `pip install`.

---

## Struttura del Codice
### Funzioni Principali
- **`invio_messaggio()`**: Gestisce l'invio dei messaggi e riceve le risposte dall'AI.
- **`esporta_chat_pdf()`**: Esporta la chat in un file PDF.
- **`esporta_chat_testo()`**: Esporta la chat in un file di testo.
- **`esporta_chat_json()`**: Esporta la chat in formato JSON.
- **`ConfigureAPI()`**: Configura la chiave API per l'AI.
- **`NuovaChat()`**: Avvia una nuova chat, resettando la cronologia.
- **`set_theme(theme)`**: Cambia il tema della GUI.

---

## Installazione
1. Clona il repository o scarica il file sorgente.
2. Installa le dipendenze richieste:
   ```bash
   pip install openai pymupdf pytaskbar
