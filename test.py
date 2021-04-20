import requests
import json
import facebook
import string 
from rich import print
from decouple import config

ACCESS_TOKEN = config("ACCESS_TOKEN") #long-lived acces token
# ACCESS_TOKEN = "EAADVGvvhhvABAPJBOf3HZATKd0hGBugwVdrPU0JlM8VvFiNQLU6HFRnmhovf20QSZBiWxGdKSRYdjoZAOSnnKixaq4hFXRPcXgZCnTPxHNRypldziDTQl8JWonup9n1zwzcek3L4iVzVD8ZA68l7zxPBpH3iSHDmXs8X4RNL3nmeokfgIj3Xsl2xqpb35klAZD" #access token with commenting rights
PAGE_ID = 100691552123875 #id of https://www.facebook.com/Fake-MIT-Confessions-100691552123875

def setAccount(info={'access_token': ACCESS_TOKEN, 'pageId': PAGE_ID}):
    return facebook.GraphAPI(access_token=info['access_token'], version = 3.1) #what version should we use?
    

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

def getPosts(graph, MY_PAGE_ID=PAGE_ID):
    """Get all of the posts on the page"""
    posts = graph.request(f"/{MY_PAGE_ID}/published_posts")
    return posts 

def generateComment(message):
    """Function to generate a comment based on a given message.."""
    return [f"Hahaha this is a great confession!!! I really relate to this.. especially the part about \"{message[:10]}\" really moved me reading about it..."]


def makeComment(graph, post, comment):
    res = graph.put_comment(object_id = post['id'], message =comment)
    story_fbid, comment_id = res['id'].split("_")
    comment_link = f"https://facebook.com/permalink.php?story_fbid={story_fbid}&id={post['id']}&comment_id={comment_id}"
    return comment_link
def commentRandomly(graph, generateComment=generateComment, num=1, prompt=True, secondPrompt=True, pageId=PAGE_ID):
    """Comments on every confession on the page using generateComment"""
    posts = convert(getPosts(pageId))
    for post in posts['data']:
        if prompt:
            print(f"Want to post a comment on confession \n[#f5a6ff]{post['message']}[/#f5a6ff]? ({len(post['message'])/4 + 100} tokens) (YES or NO):")
            ans = input()
            if ans == "NO":
                continue 
        comments =  generateComment(post['message'], num)
        print(f"\n----\nCONFESSION: [#f5a6ff]{post['message']}[/#f5a6ff]\n----)")
        for i in range(len(comments)):
            print(f"COMMENT {i+1}: [#03c6fc]{comments[i]}[/#03c6fc]\n----")
        if secondPrompt or (len(comments) > 1):
            print(f"Which comment to post? (respond number or NO)")
            ans = input()
            done = False 
            for i in range(len(comments)):
                if ans ==str(i+1)+"":
                    print(f"Posted comment")
                    graph.put_comment(object_id = post['id'], message =comments[i])
                    done = True 
            if not done:
                print("Okay, will not comment.")
        else:
            graph.put_comment(object_id = post['id'], message =comments[0])
        

def makePost(graph, message):
    """Makes a post on the page with the given message"""
    print(f"Making post: {message}")
    graph.put_object(parent_object='me', connection_name='feed', message=message)

def makePostPrompt(graph, message):
    """Makes a post on the page with the given message.. but prompts us first if its okay"""
    print(f"\n----\nCONFESSION: [#f5a6ff]{message}[/#f5a6ff]")
    print(f"\nIs this post okay? (respond YES or NO):")
    ans = input()
    if ans == "YES":
        makePost(graph, message)
        return True 
    else:
        print("Okay, will not make post.")
        return False

def getCommentsFromPost(graph, post_id):
    """Get the comments from a given post"""
    comments = graph.get_connections(id=post_id, connection_name='comments')
    return convert(comments['data']) #TODO: Should the sanitization be now or later? (to only the 'message field)

def postDemo(pageId=PAGE_ID):
    """Prints all the posts (and their comments!) on the page"""
    posts = getPosts(pageId)
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