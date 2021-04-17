from test import getPosts 
from test import makePostPrompt
import json
# import openai 
# import torch
from test import commentRandomly
from transformers import pipeline
import random
# from decouple import config
# import gpt_2_simple as gpt2
# import os
# import requests


generator = pipeline('text-generation', model='gpt2')

# openai.api_key = config("OPENAI_ACCESS_TOKEN")
# tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# odel = GPT2LMHeadModel.from_pretrained('gpt2')

#model_name = "124M"
#if not os.path.isdir(os.path.join("models", model_name)):
#	print(f"Downloading {model_name} model...")
#	gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/


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

def postSomeConfessions(i, j):
    confessions = readData()
    # print(confessions[:5])
    for k in range(i, j):
        makePostPrompt(confessions[k]['message'])

def postRandomConfessions():
    while True:
        val = makePostPrompt(random.choice(confessions)['message'])
        if val:
            break

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

def generateCommentGPT2(msg, num=1):
    q = msg[(msg.index(" ")+1):]
    prompt = f"{q}\n RESPONSE: " 
    text = generator(prompt, max_length=len(prompt.split(" "))+100, num_return_sequences=num)
    # print(text)
    return [text[i]['generated_text'][len(prompt):] for i in range(num)]
    # makePostPrompt(text)

def commentWithGPT3():
    commentRandomly(generateCommentGPT3)

def commentWithGPT2(num=1):
    commentRandomly(generateCommentGPT2, num=num, prompt=False)

def commentWithFinetunedGPT2():
    pass

def generateCommentGPT3(msg):
    q = msg[(msg.index(" ")+1):]
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Human: {q}\nAI: ",
        stop=["\nHuman:"],
        max_tokens=100
    )

    return [response.choices[0].text.strip()]

def main():
    commentWithGPT2(num=5)
    

   
if __name__ == '__main__':
    main()
