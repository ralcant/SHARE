import requests
import json
import facebook
import string 

ACCESS_TOKEN = "EAADVGvvhhvABAH5i9Q4AecOrdZAYHtZCpRd14ATZCvHmSCf3dEIeC4zoQxbR4T5lZAGrRMJR5arEwiFkjHXZAajZCXgDb4UAZCW1RVhfYZBLscUJ53eZAOblp0BEd4BHerlk0El89zIqfpG0JJZAwbit6gW7vsG4sZCZBgjFAQQioSd8pKvgF59ZC4JTHenDjLyyRiPiNLk2EZBE5KZAgZDZD"
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

def main():
    # r = requests.get(f"https://graph.facebook.com/v10.0/{PAGE_ID}/published_posts?access_token={ACCESS_TOKEN}") #not sure whether to get the /feed instead of /published_posts
    # s = unicodedata(r.text).encode("utf-8")
    # print(s)
    # print(r.text.encode("utf-8"))
    # print(r.text.encode("utf-8")[494:502])
    # x = json.loads(r.text.encode("utf-8"))
    # print(x)

    posts = graph.request(f"/{PAGE_ID}/published_posts")
    # posts = graph.get_connections(id=PAGE_ID, connection_name="feed") #seems to have a similar effect 
    sanitized_posts = convert(posts) #TODO: Is there a way to not get rid of emojis and strange characters? 
    print(sanitized_posts)
    print("\n============ Posts retrieved ====================\n")
    for post in sanitized_posts['data']:
        print(post['message']) 
        print()
    # print(posts.encode("utf-8"))
    # print(posts.encoding)
    # print(posts['data'][2]['message']) #this cannot be printed coz it contains emojis: https://www.facebook.com/permalink.php?story_fbid=100723348787362&id=100691552123875
if __name__ == '__main__':
    main()