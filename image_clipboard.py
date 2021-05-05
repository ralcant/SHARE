import platform

def windows_copy_local_image_to_clipboard(path):
    """
    Copy a jpg image to the clipboard. Windows only. 
    Taken from https://clay-atlas.com/us/blog/2020/10/30/python-en-pillow-screenshot-copy-clipboard/
    """
    system = platform.system()
    assert system == "Windows", "Only can run this clipboard function in Windows OS"
    try:
        import win32clipboard #need pywin32
        import win32clipboard as clip
        import win32con
        from io import BytesIO
        from PIL import ImageGrab, Image

        image = Image.open(path)
        output = BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:] #TODO: why 14?
        output.close()
        clip.OpenClipboard()
        clip.EmptyClipboard()
        clip.SetClipboardData(win32con.CF_DIB, data)
        clip.CloseClipboard()
        print("Copied image to clipboard!")
    except:
        print("There was an error while copying the image to the clipboard. You might need to download it yourself. Sorry!")
def copy_local_image_to_clipboard(path):
    system = platform.system()
    if system == "Windows":
        return windows_copy_local_image(path)
    elif system == "Java":
        pass
    elif system == "Linux":
        pass 
    else:
        print("Lol what system do you have") 
if __name__ == "__main__":
    windows_copy_local_image("images/testxd.jpg")