import openai

# Set up your OpenAI API key
api_key = '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'
openai.api_key = api_key

# Function to generate Python code using ChatGPT
def generate_python_code(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Example prompt
prompt = "Generate a Python function that takes a list of numbers as input and returns the sum of all even numbers."

# Generate Python code based on the prompt
generated_code = generate_python_code(prompt)

