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
import os
console = Console()
import json
info = json.loads(config("ACCESS_TOKENS"))
print(info)
size = int(os.get_terminal_size()[0])
def options(headerText, choices): 
    print(headerText)
    i = 0
    for ch in choices:
        i += 1
        print(f"({i}) {ch}") 
    ans = ""
    while True:
        try: 
            num = int(input())-1
            ans = choices[num]
            break
        except:
            pass
    print(f"[bold]You chose[/bold] {ans}")
    return num
def promptAccounts():
    index = options("[bold]Accounts:[/bold] (Enter number to continue)", [info[i]['name'] for i in range(len(info))])
    return info[index]
#def promptPage():
#    index = options("[bold]Where to Post:[/bold] (Enter number to continue)", [info[i]['name'] for i in range(len(info))])
#    return info[index]['pageId']
def choosePost(posts):
    choices = []
    for i in range(min(len(posts), 10)):
        clipmsg = posts[i]['message'].split('\n')[0]
        choices.append(f"[white]{(clipmsg)[:(size-6)]}[/white]")
    choices.append(f"[#FFB6C1]Generate New Post[/#FFB6C1]")
    index = options("[bold]Pick a post:[/bold]", choices)
    if(index == len(choices)-1):
        index = -1 
    return index
    
def generateComment(graph, post):
    comments = generateCommentGPT2(post['message'], num=5)
    for i in range(len(comments)):
        print(f"COMMENT {i+1}: [#03c6fc]{comments[i]}[/#03c6fc]\n----")
    print(f"Which comment to post? (respond number or NO)")
    ans = input()
    done = False 
    for i in range(len(comments)):
        if ans ==str(i+1)+"":
            print(f"Posted comment")
            makeComment(graph, post, comments[i])
            done = True 
    if not done:
        print("Okay, will not comment.")
def main():
    os.system("clear")
    console.rule("[bold blue]Welcome to SHARE, the MIT Confessions Bot")
    print()
    print("[cyan]Login Info")
    login = promptAccounts()
    graph = setAccount(login)
    posts = convert(getPosts(graph, login['pageId']))['data']
    while True:
        index = choosePost(posts)
        if index == -1:
            postRandomConfessions(graph)
            posts = convert(getPosts(graph, login['pageId']))['data']
            continue
        post = posts[index]
        print(f"\n----\nCONFESSION: [#f5a6ff]{post['message']}[/#f5a6ff]\n----)")
        index = options("[bold]What type of Comment?[/bold] (Enter number to continue)", ["GPT2 Generated Comment", "Write My Own"])
        if index == 0:
            generateComment(graph, post)
        else:
            print("[#03c6fc]Type Comment:[/#03c6fc]")
            comment = input() 
            makeComment(graph, post, comment)
            print("[white]Posted[/white]")

    
    


if __name__ == '__main__':
    main()

