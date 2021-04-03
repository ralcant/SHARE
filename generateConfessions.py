from test import getPosts 
from test import makePostPrompt
import json
import openai 
import torch
from test import commentRandomly
from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline, set_seed
from decouple import config

generator = pipeline('text-generation', model='gpt2')

# penai.api_key = config("OPENAI_ACCESS_TOKEN")
# tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# model = GPT2LMHeadModel.from_pretrained('gpt2')

def readData():
    """Loads all confessions from data.json"""
    confessions = []
    with open('data.json') as f:
        confessions = json.load(f)
    return renumber(confessions)

def renumber(confessions):
    """Renumbers the confessions from 1 to whatever"""
    newConfessions = []
    counter = 0
    for confession in confessions:
        counter += 1
        
        newMsg = ""
        try:
            pos = confession['message'].index(" ")
            newMsg = f"#{counter} {confession['message'][(pos+1):]}"
        except:
            # print(f"Error: {confession}")
            pass
        
        confession['message'] = newMsg 
        newConfessions.append(confession) 
    return newConfessions

def getPrompt():
    confessions = readData() 
    prompt = []
    for i in range(len(confessions)):
        prompt.append(confessions[i]['message'])
    return prompt

def postSomeConfessions():
    confessions = readData()
    # print(confessions[:5])
    for i in range(15):
        makePostPrompt(confessions[i]['message'])

def generateConfessionGPT3():
    # be careful when running this.. uses tokens!! not free!!
    # prompt = getPrompt()
    # response = openai.Completion.create(
    #    engine="davinci",
    #    prompt=prompt,
    #    max_tokens=50,
    #    n=5
    #)
    # print(response)
    #for choice in response['choices']:
    #    makePostPrompt(choice['text'])
    pass

def generateCommentGPT2(msg):
    q = msg[(msg.index(" ")+1):]
    prompt = f"Human: {q}\nAI:" 
    text = generator(prompt, max_length=100, num_return_sequences=1)
    # print(text)
    return text[0]['generated_text'][len(prompt):]
    # makePostPrompt(text)

def commentWithGPT3():
    commentRandomly(generateCommentGPT3)

def commentWithGPT2():
    commentRandomly(generateCommentGPT2, prompt=False)


def generateCommentGPT3(msg):
    q = msg[(msg.index(" ")+1):]
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Human: {q}\nAI: ",
        stop=["\nHuman:"],
        max_tokens=100
    )

    return response.choices[0].text.strip()

def main():
    commentWithGPT2()
    # pass

    

   
if __name__ == '__main__':
    main()
