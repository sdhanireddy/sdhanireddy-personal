import requests
from PIL import Image

##http://docs.python-requests.org/en/master/user/quickstart/
##http://www.pythonforbeginners.com/gui/how-to-use-pillow
##https://en.wikibooks.org/wiki/Python_Imaging_Library/Editing_Pixels

api_key =  'e221573e-0626-4d0a-a743-01d239b7bab7' ##for the beta API with json-rpc

def quota():
    url = 'https://www.random.org/quota'
    payload = {'format': 'plain'}
    return requests.get(url, params = payload).text.strip()

def get_lst(lower, upper, size):
    url = 'https://www.random.org/integers'
    payload = {'format': 'plain',
            'num': str(size),
            'min': str(lower),
            'max': str(upper),
            'col': '1',
            'rnd': 'new',
            'base': '10'
            }
    resp = requests.get(url, params = payload)
    try:
        resp.raise_for_status()
    except: #HTTPError as err:
        #raise err(resp.text)
        print(resp.text)
        resp.raise_for_status()
    return resp.text.split()

def image(width, length):
    ### don't create image unless RNG request successful
    try:
        random_lst = map(lambda x: int(x), get_lst(0,255,width*length*3))
    except:
        return

    #####taken from wikibooks PIl reference above
    img = Image.new( 'RGB', (width, length), "black") # create a new black image
    pixels = img.load() # create the pixel map
    for i in range(width):    # for every col:
        for j in range(length):    # For every row
            pixels[i,j] = (next(random_lst), next(random_lst), next(random_lst))
    img.show()
