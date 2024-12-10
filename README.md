
# Chat Magika con AI - Versione NoGrafica & ConGrafica

## Indice
- [Introduzione](#introduzione)
- [Versioni del Programma](#versioni-del-programma)
  - [Versione NoGrafica](#versione-nografica)
  - [Versione ConGrafica](#versione-congrafica)
- [Caratteristiche Principali](#caratteristiche-principali)
- [Dipendenze](#dipendenze)
- [Installazione](#installazione)
- [Come Utilizzarlo](#come-utilizzarlo)
  - [Interazione con AI](#interazione-con-ai)
  - [Esportazione della Chat](#esportazione-della-chat)
  - [Personalizzazione](#personalizzazione)
  - [Configurazione API](#configurazione-api)
- [Shortcut da Tastiera](#shortcut-da-tastiera)
- [Requisiti di Sistema](#requisiti-di-sistema)
- [Struttura del Codice](#struttura-del-codice)
  
---

## Introduzione
**Chat Magika con AI** è un'applicazione Python progettata per facilitare l'interazione con i modelli di intelligenza artificiale OpenAI. Offre due versioni tra cui scegliere:
1. **Versione NoGrafica**: Interfaccia tradizionale e semplice basata su `tkinter`.
2. **Versione ConGrafica**: Interfaccia avanzata e moderna basata su `customtkinter`.

---

## Versioni del Programma

### Versione NoGrafica
La **Versione NoGrafica** è minimalista, leggera e utilizza librerie standard come `tkinter`.

#### Funzionalità
- Gestione delle API con un'interfaccia semplice.
- Esportazione della chat in formato **PDF**, **TXT** o **JSON**.
- Personalizzazione di font e colori.
- Shortcut da tastiera per azioni rapide (es. nuova chat, cambio API Key).

### Versione ConGrafica
La **Versione ConGrafica** porta un'interfaccia più raffinata grazie a `customtkinter`, ottimizzando l'aspetto visivo e la gestione delle funzionalità.

#### Funzionalità
- Barre laterali per gestire input, temi e parametri.
- Personalizzazione avanzata:
  - Cambia temi (Chiaro, Scuro, Ocean, Verde).
  - Modifica colori di sfondi, box e sidebar.
- Slider e input per configurare parametri come temperatura e token.
- Layout centrale moderno per visualizzare conversazioni.

---

## Caratteristiche Principali
- **Interazione con AI**: Comunicazione diretta con modelli GPT tramite API OpenAI.
- **Esportazione dati**: Salva conversazioni in diversi formati.
- **Personalizzazione completa**:
  - Cambia temi, font e colori.
  - Modifica layout e impostazioni API.
- **Compatibilità multipiattaforma**: Funziona su vari sistemi operativi.

---

## Dipendenze
### Librerie Python
- `tkinter` (per NoGrafica)
- `customtkinter` (per ConGrafica)
- `fitz` (PyMuPDF): Per manipolazione dei file PDF.
- `openai`: Per la comunicazione con l'API.
- `pytaskbar`: Per l'integrazione con la barra delle applicazioni (opzionale su Windows).
- Altre librerie native: `json`, `os`, `time`, `threading`, `ctypes`.

---

## Installazione
1. **Clona il repository** o scarica i file sorgenti.
2. Installa le dipendenze richieste:
   ```bash
   pip install openai pymupdf customtkinter pytaskbar
   ```
3. Avvia la versione desiderata:
   - Per la **Versione NoGrafica**:
     ```bash
     python AI_NoGrafica.py
     ```
   - Per la **Versione ConGrafica**:
     ```bash
     python AI_ConGrafica.py
     ```

---

## Come Utilizzarlo

### Interazione con AI
1. Inserisci il messaggio nel campo di input.
2. Premi **Invia** o utilizza il tasto **Enter**.
3. Visualizza la risposta dell'AI nella finestra principale.

---

### Esportazione della Chat
- Esporta la chat selezionando il formato:
  - **PDF**: Salva la conversazione in un documento leggibile.
  - **TXT**: Esporta come file di testo semplice.
  - **JSON**: Salva la conversazione in formato strutturato.

---

### Personalizzazione
- Modifica il tema accedendo a `Personalizzazione > Cambia Tema`.
- Personalizza i colori e i font tramite il menu dedicato.

---

### Configurazione API
- Cambia la chiave API tramite il menu `Chat > Cambia API Key`.
- Configura parametri come temperatura e token tramite il menu `Personalizzazione > Impostazioni API`.

---

## Shortcut da Tastiera
- **Ctrl + N**: Avvia una nuova chat.
- **Ctrl + K**: Cambia la chiave API.
- **Ctrl + Q**: Esci dall'applicazione.

---

## Requisiti di Sistema
- **Sistema Operativo**:
  - Windows (consigliato per PyTaskbar).
  - Altri OS: Compatibile ma con funzionalità limitate.
- **Python**: Versione 3.7 o superiore.

---

## Struttura del Codice
### Funzioni Principali
- **`invio_messaggio()`**: Gestisce l'invio di messaggi e riceve risposte dall'AI.
- **`esporta_chat_pdf()`**: Esporta la chat in formato PDF.
- **`esporta_chat_testo()`**: Esporta la chat in formato TXT.
- **`esporta_chat_json()`**: Salva la chat in formato JSON.
- **`ConfigureAPI()`**: Configura la chiave API per OpenAI.
- **`set_theme()`**: Cambia il tema grafico della GUI.
- **`NuovaChat()`**: Resetta la conversazione corrente.
