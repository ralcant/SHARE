import requests
import json
import facebook
import string 

ACCESS_TOKEN = "EAADVGvvhhvABAPJBOf3HZATKd0hGBugwVdrPU0JlM8VvFiNQLU6HFRnmhovf20QSZBiWxGdKSRYdjoZAOSnnKixaq4hFXRPcXgZCnTPxHNRypldziDTQl8JWonup9n1zwzcek3L4iVzVD8ZA68l7zxPBpH3iSHDmXs8X4RNL3nmeokfgIj3Xsl2xqpb35klAZD"
PAGE_ID = 100691552123875 #id of https://www.facebook.com/Fake-MIT-Confessions-100691552123875

graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version = 3.1) #what version should we use?

def sanitize(s): #Taken from https://stackoverflow.com/a/8689826/14127936
    """Sanitize the input s by only keeping punctuation, digits, ascii letters and whitespace"""
    return ''.join(filter(lambda x: x in string.printable, s))

def convert(input): #From answer https://stackoverflow.com/questions/13101653/python-convert-complex-dictionary-of-strings-from-unicode-to-ascii
    """Recursively sanitize keys and elements of lists, tuples and dictionaries"""
    #TODO: Is this necessary? can we assume that the only place that needs to be sanitized is the 'message' parameter?
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.items()}
    elif isinstance(input, list) or isinstance(input, tuple):
        return [convert(element) for element in input]
    else: #assumed to be a string
        return sanitize(input)

def getPosts():
    posts = graph.request(f"/{PAGE_ID}/published_posts")
    return posts 

def generateComment(message):
    return f"Hahaha this is a great confession!!! I really relate to this.. especially the part about \"{message[:10]}\" really moved me reading about it..."

def commentRandomly():
    posts = convert(getPosts())
    for post in posts['data']:
        comment =  generateComment(post['message'])
        print(f"Posting comment {comment} on confession {post['message']}")
        graph.put_comment(object_id = post['id'], message =comment)

def postDemo():
    posts = getPosts()
    sanitized_posts = convert(posts) #TODO: Is there a way to not get rid of emojis and strange characters? 
    print(sanitized_posts)
    print("\n============ Posts retrieved ====================\n")
    for post in sanitized_posts['data']:
        print(post['message']) 
        print()

def main():
    # postDemo()
    commentRandomly()
   
if __name__ == '__main__':
    main()