from decouple import config
from test import getPosts
from test import convert
from test import makeComment
from test import setAccount
import facebook
from rich import print
from rich.console import Console
from generateConfessions import generateCommentGPT2
from generateConfessions import postRandomConfessions
from meme_utils import MemeGenerator
import os
import pyperclip
from facebook_scraper import get_posts
import shutil
console = Console()
import json

try:
    api_key = config('WATSON_KEY') 
    from ibm_watson import ToneAnalyzerV3
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


    url = config('WATSON_URL')

    # authentication + setup for ibm_watson tone analyzer
    authenticator = IAMAuthenticator(apikey=api_key)
    tone_analyzer = ToneAnalyzerV3(version='2017-09-21', authenticator=authenticator)
    tone_analyzer.set_service_url(url)
except:
    pass
info = json.loads(config("ACCESS_TOKENS"))
print(info)
print(shutil.get_terminal_size())
size = int(shutil.get_terminal_size()[0])
memer = MemeGenerator("mit_meme_creator", "mit_meme_password")
def options(headerText, choices, start=0): 
    print(headerText)
    i = start
    for index in range(start, min(start+10, len(choices))):
        i += 1
        print(f"[blue]({i})[/blue] [white]{choices[index]}[/white]") 
    i += 1
    if(i != len(choices)+1):
        print(f"({i}) See More")
    ans = ""
    while True:
        try: 
            num = int(input())-1
            ans = choices[num]
            break
        except:
            pass
    
    if(num+1 == i):
        print("START: "+str(start))
        return options(headerText, choices, start+10)
    print(f"[bold]You chose[/bold] {ans}")
    return num
def promptAccounts():
    #index = options("[bold]Accounts:[/bold] (Enter number to continue)", [info[i]['name'] for i in range(len(info))])
    return info[1]#index]
#def promptPage():
#    index = options("[bold]Where to Post:[/bold] (Enter number to continue)", [info[i]['name'] for i in range(len(info))])
#    return info[index]['pageId']
def choosePost(posts):
    choices = []
    choices.append(f"[#FFB6C1]Generate New Post[/#FFB6C1]")
    choices.append(f"[#FFB6C1]Quit[/#FFB6C1]")
    #for i in range(min(len(posts), 10)): <-- wait we only do this for max 10 possts?
     #   tone = ""
    #    try:
     #       tone = '[' + tone_analyzer.tone(posts[i]['message']).get_result()['document_tone']['tones'][0]['tone_id'].upper() + ']'
     #   except:
     #       pass
     #   clipmsg = posts[i]['message'].split('\n')[0]
     #   choices.append(f"[white]{ (tone + clipmsg)[:(size-6)]}[/white]")
    
    for i in range(len(posts)):
        clipmsg = posts[i]['message'].split('\n')[0]
        choices.append(f"[white]{(clipmsg)[:(size-6)]}[/white]")
    
    index = options("[bold]Pick a post:[/bold]", choices)
    return index
    
def generateComment(graph, post, link=''):
    comments = generateCommentGPT2(post['message'], num=5)
    for i in range(len(comments)):
        print(f"COMMENT {i+1}: [#03c6fc]{comments[i]}[/#03c6fc]\n----")
    print(f"Which comment to post? (respond number or NO)")
    ans = input()
    done = False 
    comment_link = None
    for i in range(len(comments)):
        if ans ==str(i+1)+"":
            print(f"Posting comment...")
            comment_link = makeComment(graph, post, comments[i])
            done = True 
    if not done:
        print("Okay, will not comment.")
    return comment_link
def getPostsWrapper(index, graph=None, login=None):
    # return convert(getPosts(graph, login['pageId']))['data'] # fix the get_posts bug?!? then change this back
    if index == 0:
        return convert(getPosts(graph, login['pageId']))['data']
    else: #index=1, for now just beaverconfessions
        posts = []
        for post in get_posts('beaverconfessions',pages=5):
            new_post = {}
            new_post['message'] = convert(post['post_text'])
            new_post['link'] = post['post_url']
            new_post['id'] = post['post_id']
            posts.append(new_post)
        return posts
def main():
    os.system("clear")
    console.rule("[bold blue]Welcome to SHARE, the MIT Confessions Bot")
    print()
    print("[cyan]Login Info")
    login = promptAccounts()
    graph = setAccount(login)
    memer = MemeGenerator("mit_meme_creator", "mit_meme_password", graph)
    page_index = options('Pick a Page:', ['Fake MIT Confessions', 'Real MIT Confessions'])
    posts = getPostsWrapper(page_index, graph, login)
    while True:
        index = choosePost(posts)
        if index == 1:
            break
        if index == 0:
            postRandomConfessions(graph)
#            posts = convert(getPosts(graph, login['pageId']))['data']
            posts = getPostsWrapper(page_index)
            continue
        # print(post)
        
        post = posts[index-2]
        print(f"CONFESSION: [#f5a6ff]{post['message']}[/#f5a6ff]\n----)")
        index = options("[bold]What type of Comment?[/bold] (Enter number to continue)", ["GPT2 Generated Comment", "Write My Own", "Write custom message with meme"])
        if index == 0:
            generateComment(graph, post)
        elif index == 1:
            print("[#03c6fc]Type Comment:[/#03c6fc]")
            comment = input()
            if len(comment) == 0:
                comment = "no comment" 
            comment_link = makeComment(graph, post, comment)
            if comment_link != None:
                print(f"[bold]Posted. See it here {comment_link} [/bold]")
        else:
            memes = memer.get_all_memes()
            names = [meme['name'] for meme in memes]
            i = options("[#03c6fc]Choose from the meme list:[/#03c6fc]", names)
            print("[#03c6fc]Type meme top text[/#03c6fc]")   
            top_text = input()
            print("[#03c6fc]Type meme bottom text[/#03c6fc]") 
            bottom_text = input()
            print("[#03c6fc]Type extra message[/#03c6fc]") 
            extra_message = input()

            meme_link = memer.create_and_post_meme(memes[i]['id'], post['id'], top_text, bottom_text, extra_message)
            print(f"[bold]Posted meme!. See it here: {meme_link}[/bold]")    


if __name__ == '__main__':
    main()

