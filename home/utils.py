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

# # Example prompt
# prompt = "Generate a Python function that takes a list of numbers as input and returns the sum of all even numbers."

# # Generate Python code based on the prompt
# generated_code = generate_python_code(prompt)


from mail.models import History

import requests


def update_read_status(acc):
    all_mails = History.objects.filter(user=acc.user)
    for i in all_mails:
        url = 'https://supersent.in/api/get-read-status/'
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'api_key': acc.api_key,
            'identifier': str(i.id)
        }

        response = requests.get(url, headers=headers, json=data)
        total_opened = response.json().get("total_opend")
        print(response.text)
        try:
            i.total_opened = total_opened
            i.save()
        except Exception as e:
            print("Error : ",e)

    return