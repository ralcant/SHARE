import requests
import urllib 
import shutil
from test import *

def main():
    #Get all memes
    # r = requests.get("https://api.imgflip.com/get_memes")
    # data = r.json()
    # print(data['data']['memes']) 

    # Create a memem given some text
    # data = {
    #     'template_id': 181913649, #drake hotline bling
    #     'username': "mit_meme_creator",
    #     'password': "mit_meme_password",
    #     'text0': "Using the web browser to create a meme ",
    #     'text1': "Using the API to do it",
    # }
    # r = requests.post("https://api.imgflip.com/caption_image", data=data)
    # response = r.json() 

    # Save the meme locally
    # r = requests.get("https://i.imgflip.com/554hdu.jpg", stream=True)
    # if r.status_code == 200:
    #     with open("test_1.jpg", 'wb') as f:
    #         r.raw.decode_content = True
    #         shutil.copyfileobj(r.raw, f)

    # Post it on facebook 
    # posts = convert(getPosts())
    # for post in posts['data']:
    #     print(post)
    #     comment="here an image should goooo" #this comment will be edited
    #     res = graph.put_comment(object_id = post['id'], message =comment ) #create comment
    #     graph.put_photo( #put an image (and a new comment) in the created comment
    #         image=open("test_1.jpg", 'rb'), 
    #         album_path=res['id'], 
    #         message="this should be a comment XD and a picture"
    #     )
    #     break


if __name__ == "__main__":
    print(main())