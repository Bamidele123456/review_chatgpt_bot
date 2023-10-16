import openai
openai.api_key = "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"


prompt = "Topography temperate grasslands, vegetation is rivers,trees and lakes."
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.5,
    max_tokens=70,
    top_p=1.0,
    frequency_penalty=0.8,
    presence_penalty=0.0,
    messages=[
        {"role": "system", "content": "You are a remote viewing assistant and you are to choose target location with  the topography and vegetation given then ask remote viewing questions about the location one question at a time"},
        {"role": "user", "content": prompt},
    ]
)

# Extract the response from OpenAI and format it as a JSON object
print(response['choices'][0]['message']['content'])
