import facebook
import pyperclip
import sys, os
from rich import print
from decouple import config
from confessionscommenter.image_clipboard import get_temporary_filename, save_image_locally

ACCESS_TOKEN = config("ACCESS_TOKEN") #long-lived acces token
PAGE_ID = 100691552123875 #id of https://www.facebook.com/Fake-MIT-Confessions-100691552123875
# pagegraph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version = 3.1)
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
def enablePrint():
    sys.stdout = sys.__stdout__
def setAccount(info={'access_token': ACCESS_TOKEN, 'pageId': PAGE_ID}):
    return facebook.GraphAPI(access_token=info['access_token'], version = 3.1) #what version should we use?   
def postComment(graph, post, comment):
    try:
        blockPrint()
        res = graph.put_comment(object_id =f"{PAGE_ID}_{post['id']}", message =comment)
        enablePrint()
        print('Comment posted!')
        story_fbid, comment_id = res['id'].split("_")
        comment_link = f"https://facebook.com/permalink.php?story_fbid={story_fbid}&id={PAGE_ID}&comment_id={comment_id}"
        print(f"Yay! Comment posted. See the result here: {comment_link}")
        return comment_link
    except:
        enablePrint()
        pyperclip.copy(comment)
        print(f"[bold]Copied to clipboard, paste here: {post['link']} [/bold]")
        return None
def post_local_meme_facebook(graph, post_id, meme_local, extra_message="", remove_local=True):
    """Post a local image to a given post"""
    comment= "Interesting. This reminded me of https://www.youtube.com/watch?v=Lrj2Hq7xqQ8" #Curiosity killed the cat
    res = graph.put_comment(object_id= f"{PAGE_ID}_{post_id}", message= comment) #create comment
    comment_info = graph.put_photo( #put an image (and a new comment) in the created comment
        image = open(meme_local, 'rb'), 
        album_path = res['id'], 
        message= extra_message
    )
    story_fbid, comment_id = res['id'].split("_")
    meme_link = f"https://facebook.com/permalink.php?story_fbid={story_fbid}&id={PAGE_ID}&comment_id={comment_id}"
    print(f"Yay! Meme posted. See it here: {meme_link}")
    if remove_local:
        os.remove(meme_local)
    return meme_link #link to the fb post

def post_image_from_url(graph, url, post_id, extra_message="Generated meme ;)", remove_local=True, local_filename=None):
    if local_filename is None:
        filename = get_temporary_filename(file_dir="meme_dir")
    else:
        filename = local_filename #check if local_filename is a valid path
    save_image_locally(url, filename)
    post_local_meme_facebook(graph, post_id, filename, extra_message=extra_message, remove_local=remove_local) #TODO: Maybe put a default link to our page or sth


#-------------------------Below things that are not currently used but might be helpful later---------------------------------------#

# def makePost(graph, message):
#     """Makes a post on the page with the given message"""
#     print(f"Making post: {message}")
#     graph.put_object(parent_object=PAGE_ID, connection_name='feed', message=message)
# def makePostPrompt(graph, message):
#     """Makes a post on the page with the given message.. but prompts us first if its okay"""
#     print(f"\n----\nCONFESSION: [#f5a6ff]{message}[/#f5a6ff]")
#     print(f"\nIs this post okay? (respond YES or NO):")
#     ans = input()
#     if ans == "YES":
#         makePost(graph, message)
#         return True 
#     else:
#         print("Okay, will not make post.")
#         return False
# def commentRandomly(graph, generateComment=generateComment, num=1, prompt=True, secondPrompt=True, pageId=PAGE_ID):
#     """Comments on every confession on the page using generateComment"""
#     posts = convert(getPosts(pageId)) #TODO: Make it use facebook-scraper
#     for post in posts['data']:
#         if prompt:
#             print(f"Want to post a comment on confession \n[#f5a6ff]{post['message']}[/#f5a6ff]? ({len(post['message'])/4 + 100} tokens) (YES or NO):")
#             ans = input()
#             if ans == "NO":
#                 continue 
#         comments =  generateComment(post['message'], num)
#         print(f"CONFESSION: [#f5a6ff]{post['message']}[/#f5a6ff]")
#         for i in range(len(comments)):
#             print(f"COMMENT {i+1}: [#03c6fc]{comments[i]}[/#03c6fc]")
#         if secondPrompt or (len(comments) > 1):
#             print(f"Which comment to post? (respond number or NO)")
#             ans = input()
#             done = False 
#             for i in range(len(comments)):
#                 if ans ==str(i+1)+"":
#                     print(f"Posted comment")
#                     graph.put_comment(object_id = post['id'], message =comments[i])
#                     done = True 
#             if not done:
#                 print("Okay, will not comment.")
#         else:
#             graph.put_comment(object_id = post['id'], message =comments[0])
    
if __name__ == '__main__':
    pass
