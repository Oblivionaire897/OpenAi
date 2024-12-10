from openai import OpenAI

client = OpenAI(api_key="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")

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Parlami dell'attuale monarca del Regno Unito?"}
    ],
    temperature=0.7,
    max_tokens=10,
)

print(completion.choices[0].message.content)