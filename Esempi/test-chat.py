from openai import OpenAI

Client = OpenAI(api_key="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") #Nostra Api-key

chat_history = [] #Una lista vuota con tutte le domande che faremo

#Avviamo un ciclo infinito che chiudiamo quando l'utente scrive "stop" (righe 12-14)
while True:
    user_input = input("\nInserisci il tuo messaggio: ")
    chat_history.append({"role": "user", "content": user_input}) #Aggiungiamo la richiesta appena fatta alla lista

    if user_input.lower() == "stop":
        print("Conversazione terminata.")
        break

    #--Finita la parte relativa alla domanda. Ora ci occupiamo della risposta--

    stream = Client.chat.completions.create(
        model = "gpt-3.5-turbo-0125", #Qui inseriamo il modello di intellingenza artificiale che deisderiamo
        messages = chat_history, #Qui gli diamo la cronologia della chat così da avere un contesto e poter cercare informazioni anche nei vecchi prompt
        stream = True #Abilitiamo la ricezione in tempo reale della risposta
        )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")