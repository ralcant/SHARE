from test import getPosts 
from test import makePostPrompt
import json



def readData():
    """Loads all confessions from data.json"""
    confessions = []
    with open('data.json') as f:
        confessions = json.load(f)
    return renumber(confessions)

def renumber(confessions):
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



def postSomeConfessions():
    confessions = readData()
    # print(confessions[:5])
    for i in range(15):
        makePostPrompt(confessions[i]['message'])

def main():
    pass

    

   
if __name__ == '__main__':
    main()
