import requests
import urllib 
import shutil
from test import *


class MemeGenerator:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.api_root = "https://api.imgflip.com"
    def get_all_memes(self):
        data = requests.get(f"{self.api_root}/get_memes").json()
        return data['data']['memes']
    def create_and_post_meme(self, meme_id, post_id, top_text="", bottom_text="", extra_message=""):
        res = self.create_meme(meme_id, [top_text, bottom_text]) #create meme in the imgflip server
        local_image = "images/aaaaa.jpg" # TODO: Make it random, different for different pictures
        res = self.save_local_meme(res, local_image) # race condition?
        res = self.post_local_meme_facebook(post_id, local_image, extra_message)
        print(res)
        return res
    def create_meme(self, meme_id, text_list):
        text_template = {f"text{i}": text for i, text in enumerate(text_list)}
        data = {
            'template_id': meme_id, #drake hotline bling
            'username': "mit_meme_creator",
            'password': "mit_meme_password",
            **text_template
        }
        created_meme = requests.post(f"{self.api_root}/caption_image", data=data).json()
        return created_meme
    def save_local_meme(self, meme_data, filename):
        # Save the meme locally
        r = requests.get(meme_data['data']['url'], stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        return 
    def post_local_meme_facebook(self, post_id, meme_location, extra_message=""):
        comment= "here an image should goooo" #this comment will be edited
        res = graph.put_comment(object_id= post_id, message= comment ) #create comment
        comment_info = graph.put_photo( #put an image (and a new comment) in the created comment
            image=open(meme_location, 'rb'), 
            album_path=res['id'], 
            message= extra_message
        )
        return res #info about the facebook post

def demo():
    meme_generator = MemeGenerator("mit_meme_creator", "mit_meme_password")
    # print(meme_generator.get_all_memes())
    res = meme_generator.create_meme(meme_id=3218037, text_list=["Here I'd put real-people confessions", "If I only had one"])
    print(res)
    res = meme_generator.save_local_meme(res, "images/testxd.jpg")
    print(res)
    posts = convert(getPosts())
    for post in posts['data']:
        res = meme_generator.post_local_meme_facebook(post_id=post['id'], meme_location="images/testxd.jpg", extra_message="Will this work?")
        print(res)
        break
if __name__ == "__main__":
    print(demo())