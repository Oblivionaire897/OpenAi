from openai import OpenAI

client = OpenAI(api_key="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")

response = client.images.generate(
    model="dall-e-3",
    prompt="a futuristic city skyline at sunset",
    n=1,
    quality="standard",
    size="1024x1024"
)

# Salvare l'immagine o fare altre operazioni
image_data = response['data'][0]['url']
print("Generated Image URL:", image_data)
