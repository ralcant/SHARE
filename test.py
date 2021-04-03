import requests
import json
import facebook
import string 
from decouple import config

ACCESS_TOKEN = config("ACCESS_TOKEN") #long-lived acces token
# ACCESS_TOKEN = "EAADVGvvhhvABAPJBOf3HZATKd0hGBugwVdrPU0JlM8VvFiNQLU6HFRnmhovf20QSZBiWxGdKSRYdjoZAOSnnKixaq4hFXRPcXgZCnTPxHNRypldziDTQl8JWonup9n1zwzcek3L4iVzVD8ZA68l7zxPBpH3iSHDmXs8X4RNL3nmeokfgIj3Xsl2xqpb35klAZD" #access token with commenting rights
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
    """Get all of the posts on the page"""
    posts = graph.request(f"/{PAGE_ID}/published_posts")
    return posts 

def generateComment(message):
    """Function to generate a comment based on a given message.."""
    return f"Hahaha this is a great confession!!! I really relate to this.. especially the part about \"{message[:10]}\" really moved me reading about it..."

def commentRandomly(generateComment=generateComment, prompt=True, secondPrompt=True):
    """Comments on every confession on the page using generateComment"""
    posts = convert(getPosts())
    for post in posts['data']:
        if prompt:
            print(f"Want to post a comment on confession {post['message']}? ({len(post['message'])/4 + 100} tokens) (YES or NO):")
            ans = input()
            if ans == "NO":
                continue 
        comment =  generateComment(post['message'])
        print(f"\n----\nCONFESSION: {post['message']}\n----\nCOMMENT: {comment}\n----")
        if secondPrompt:
            print(f"Is this comment okay? (respond YES or NO)")
            ans = input()
            if ans == "YES":
                print(f"Posted comment")
                graph.put_comment(object_id = post['id'], message =comment)
            else:
                print("Okay, will not comment.")
        else:
            graph.put_comment(object_id = post['id'], message =comment)
        

def makePost(message):
    """Makes a post on the page with the given message"""
    print(f"Making post: {message}")
    graph.put_object(parent_object='me', connection_name='feed', message=message)

def makePostPrompt(message):
    """Makes a post on the page with the given message.. but prompts us first if its okay"""
    print(f"\nIs this post okay? (respond YES or NO): {message}")
    ans = input()
    if ans == "YES":
        makePost(message)
    else:
        print("Okay, will not make post.")

def getCommentsFromPost(post_id):
    """Get the comments from a given post"""
    comments = graph.get_connections(id=post_id, connection_name='comments')
    return convert(comments['data']) #TODO: Should the sanitization be now or later? (to only the 'message field)

def postDemo():
    """Prints all the posts (and their comments!) on the page"""
    posts = getPosts()
    sanitized_posts = convert(posts) #TODO: Is there a way to not get rid of emojis and strange characters? 
    print(sanitized_posts)
    print("\n============ Posts retrieved ====================\n")
    for post in sanitized_posts['data']:
        print("Post:")
        print("\t"+post['message']) 
        print("Comments:")
        all_comments = getCommentsFromPost(post['id'])
        for i, comment in enumerate(all_comments):
            print(f"\t{i}."+comment['message'])
        print()

def main():
    postDemo()
   
if __name__ == '__main__':
    main()