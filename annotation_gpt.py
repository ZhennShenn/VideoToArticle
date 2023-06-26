import openai
import re

# set up your OpenAI API credentials
openai.api_key = ""

# read the text from the file
with open('text.txt', 'r') as f:
    text = f.read()

# split the text into chunks of allowed length
chunk_size = 250
text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# submit prompt to the GPT API to add punctuation to each chunk separately
responses = []
for chunk in text_chunks:
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Напиши аннотацию к тексту: \"{chunk}\".",
        temperature=0.1,
        max_tokens=2048
    )
    responses.append(response)

# concatenate the responses into a single punctuated text
annotation = ""
for response in responses:
    annotation += response.choices[0].text.strip()


# write the punctuated text to a new file
with open('annotation.txt', 'w') as f:
    f.write(annotation)

