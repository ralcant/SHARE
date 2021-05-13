from confessionscommenter.commandline_utils import generateComments, options, choosePost
from confessionscommenter.meme_utils import MemeGenerator
from confessionscommenter.general_utils import getPosts, convert

from facebook_utils import ACCESS_TOKEN, setAccount, postComment, post_image_from_url #, postRandomConfessions

import os
from rich import print
from rich.console import Console
from decouple import config
import shutil
console = Console()
import json
ACCESS_TOKEN = config('ACCESS_TOKEN')
PAGE_ID = 100691552123875
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
print(shutil.get_terminal_size())
size = int(shutil.get_terminal_size()[0])
def main():
    os.system("clear")
    console.rule("[bold blue]Welcome to SHARE, the MIT Confessions Bot")
    print()
    print("[cyan]We are using the 'Fake MIT Confessions' Page")
    graph = setAccount(info={"access_token": ACCESS_TOKEN, "pageId": PAGE_ID})
    memer = MemeGenerator()
    posts = convert(getPosts(title="Fake-MIT-Confessions-100691552123875")) #Maybe save it on disk so that you don't make too many calls to facebook scraper? Otherwise it ends up returning no answers :(
    if len(posts) == 0:
        print("There doesn't seem to be any post here!. If you are using facebook-scraper then you might need to wait")
        return
    while True:
        index = choosePost(posts)
        if index == 0:
            break
        post = posts[index-1]
        print(f"CONFESSION: [#f5a6ff]{post['message']}[/#f5a6ff]")
        index = options(
            "[bold]What type of Comment?[/bold] (Enter number to continue)", 
            [
                "GPT2 Generated Comment", 
                "Automatically generate meme for this post", 
                "Generate meme for post with input text"
            ])
        if index == 0:
            new_comment = generateComments(post)
            """Extra"""
            if new_comment is not None:
                postComment(graph, post, new_comment)  
        elif index == 1:
            generatable_memes = memer.get_generatable_memes_info()['memes']
            names = [f"{meme['name']}. See examples at https://imgflip.com/meme/{meme['id']}" for meme in generatable_memes]
            i = options("[#03c6fc]Choose from the meme list:[/#03c6fc]", names)
            meme_info, _ = memer.generate_captions(generatable_memes[i]['id'], post['message'], generatable_memes[i]['box_count'])
            print(f"[bold]Posted meme!. See it here: {meme_info['data']['url']}[/bold]")

            """Extra"""
            print(f"Would you like this meme on facebook? (YES or NO)")
            if input() == "YES":
                print("Now publishing to facebook...")
                post_image_from_url(graph, meme_info['data']['url'], post['id'], extra_message="Generated meme ;)", remove_local=True) #TODO: Maybe put a default link to our page or sth
            else:
                print("OK, will not post.")
        elif index == 2:
            memes = memer.get_popular_memes()
            names = [f"{meme['name']}. See examples at https://imgflip.com/meme/{meme['id']}" for meme in memes]
            i = options("[#03c6fc]Choose from the meme list:[/#03c6fc]", names)
            captions = []
            print(f"[#f5a6ff]This meme requires [red]{memes[i]['box_count']}[/red] texts[/#f5a6ff]")
            for j in range(1, memes[i]['box_count']+1):
                print(f"[#03c6fc]Type meme text #{j}[/#03c6fc]: ", end="")   
                text = input()
                captions.append(text)
            meme_info, _ = memer.create_meme(memes[i]['id'], captions)
            print(f"[bold]See meme here: {meme_info['data']['url']}[/bold]")
            
            """Extra"""
            print("Now publishing to facebook...")
            post_image_from_url(graph, meme_info['data']['url'], post['id'], extra_message="Generated meme ;)", remove_local=True) #TODO: Maybe put a default link to our page or sth
            
        elif index == 3:
            print("[#03c6fc]Type Comment:[/#03c6fc] ", end="")
            comment = input()
            if len(comment) == 0:
                continue
            postComment(graph, post, comment)
        else:
            pass
if __name__ == '__main__':
    main()