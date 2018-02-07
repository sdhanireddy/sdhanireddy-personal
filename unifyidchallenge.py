import requests
from PIL import Image
#from Crypto.PublicKey import RSA
import json

##http://docs.python-requests.org/en/master/user/quickstart/
##http://www.pythonforbeginners.com/gui/how-to-use-pillow
##https://en.wikibooks.org/wiki/Python_Imaging_Library/Editing_Pixels
##https://gist.github.com/lkdocs/6519378
##https://www.dlitz.net/software/pycrypto/api/current/Crypto.PublicKey.RSA._RSAobj-class.html
##https://www.dlitz.net/software/pycrypto/api/current/Crypto.PublicKey.RSA-module.html#generate
##https://api.random.org/json-rpc/1/basic
##https://api.random.org/json-rpc/1/introduction
##http://www.jsonrpc.org/specification


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

def get_blobs(n):
    url = 'https://api.random.org/json-rpc/1/invoke'
    if n%8 != 0:
        print('n must be divisible by 8')
        return
    api_key =  'e221573e-0626-4d0a-a743-01d239b7bab7' ##for the beta API with json-rpc
    params = {'apiKey': api_key,
                'n': 1,
                'size': n
            }
    payload = {'jsonrpc': '2.0',
                'method': 'generateBlobs',
    			'params': params,
    			'id': 438
    		}
    header = {'content-type': 'application/json-rpc'}
    resp = requests.post(url, data=json.dumps(payload),headers=header)
    try:
        resp.raise_for_status()
    except:
        print(resp.json()['error'])
        resp.raise_for_status()
    return resp.json()['result']['random']['data'][0]

def image(width, length):
    ### don't create image unless RNG request successful
    try:
        random_lst = map(lambda x: int(x), get_lst(0,255,width*length*3))
    except:
        return

    #####taken from wikibooks PIl reference above
    img = Image.new( 'RGB', (width, length), 'black') # create a new black image
    pixels = img.load() # create the pixel map
    for i in range(width):    # for every col:
        for j in range(length):    # For every row
            pixels[i,j] = (next(random_lst), next(random_lst), next(random_lst))
    img.show()

###I couldn't pip install pycrypto because I had some errors so I can't test this,
###but this is what I got from the sources above
def generate_RSA(bits=2048):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    try:
        assert bits%256==0 and bits>=1024, 'Incorrect number of bits'
    except AssertionError:
        return

    new_key = RSA.generate(bits, e=65537, randfunc=get_blobs)
    public_key = new_key.publickey().exportKey('PEM')
    private_key = new_key.exportKey('PEM')
    return private_key, public_key
