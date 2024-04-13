import openai

# Set your OpenAI API key
openai.api_key = "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"

# Now you can make API requests
com = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello, how can I assist you today?"}
    ]
)

print(com["choices"][0]["message"]["content"])
