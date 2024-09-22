import openai

# Initialize the OpenAI client with your API key
openai.api_key = "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"
# Generate a completion using GPT-3.5 Turbo
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud."},
        {"role": "user", "content": "What is coding?"}
    ]
)

# Print the assistant's response
print(completion.choices[0].message['content'])
