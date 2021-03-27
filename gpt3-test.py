import os
import openai

openai.api_key = # idk how to get it from environ but I pasted it in

# generates comments(s) responding to the last confession 
def comment(prompt, engine='davinci', temp=0.7, max_tokens=64, top_p=1, freq_penalty=0, pres_penalty=0):
    
    # response to the latest confession based on the prompt
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt, 
        temperature=temp,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=freq_penalty,
        presence_penalty=pres_penalty,
    )
    print(response)
    return response['choices'][0]['text']

    # note might need to do something with stop sequences, will figure it out later...

def respond():
    # read previous saved confessions from the prompt 
    f = open('prompt.txt', 'r')
    prompt = f.read()
    f.close()

    # for now, we can manually input some confessions to test, but will chagne this to loading in confessions from like the confessions of the day later...
    while(True):
        prompt += input('CONFESSION: ')
        prompt += comment(prompt)
        print(prompt)
        break

    # save the generated responses to serve as prompts for later -- idk if this is a good idea maybe should just keep prompt file as ground truth and then another file for generated comments 
    f = open('prompt.txt', 'w')
    f.write(prompt)

respond()