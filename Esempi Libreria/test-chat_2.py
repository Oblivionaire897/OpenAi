#Per i commenti alle altre righe di codice, guardare il file "test-chat.py"

from openai import OpenAI

Client = OpenAI(api_key="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")

chat_history = []

chat_history.insert(0, {"role": "system", "content": "usa un tono da teenager"}) #Diamo un contesto al nostro assistente

while True:
    user_input = input("\nInserisci il tuo messaggio: ")
    chat_history.append({"role": "user", "content": user_input})

    if user_input.lower() == "stop":
        print("Conversazione terminata.")
        break

    stream = Client.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        messages = chat_history,
        stream = True
        )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")