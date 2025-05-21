from urllib.parse import unquote
import re
import base64
import requests
import shutil #picked up from https://stackoverflow.com/a/18043472

#it's easiest just to change the URL in the code itself since I'm making this for myself.
ENCODED_URL = "https://comicskingdom.com/_next/image?url=https%3A%2F%2Fwp.comicskingdom.com%2Fcomicskingdom-redesign-uploads-production%2F2025%2F05%2FY2tGbGFzaCBHb3Jkb24tRU5HLTUxMTU0MTU.jpg&w=3840&q=75"
RANGE = 12 #establishing how wide a range we want to set on either side of our link fishing scheme. 12 seems to be wide enough.
COMIC_PREFIX = "ckFlash Gordon-ENG-" #the prefix of the comic one wants to download--in this case, it's the prefix for Flash Gordon.


def reformat_url():
    '''
    Reformats a Comics Kingdom image URL by decoding the
    JavaScript-encoding, and removing all but the actual
    address of the image.
    '''
    url = unquote(ENCODED_URL)
    startIndex = url.find("url=") + 4
    endIndex = url.find(".jpg") + 4
    url = url[startIndex:endIndex]
    return url


def get_image_name(url):
    '''
    Gets the filename for the image stored at the URL.
    Though slicing off the file suffix makes decoding
    from BASE64 easier, it means adding '.jpeg' back on the
    end when we want to actually retrieve the file.
    '''
    imageName = re.search("/[0-9]{2}/.+.jpg$", url).group(0)[4:-4]
    return imageName


def get_image_number(imageName):
    '''
    Decodes the image name from BASE64 and returns the number
    associated with the image. The image name follows the format:
    "ckFlash Gordon-ENG-xxxxxxx", where the x's represent a 7 digit integer.
    '''
    imageName += " =="
    imageNameBASE64 = imageName.encode("ascii")
    imageNameDecoded = base64.b64decode(imageNameBASE64)
    imageNameDecoded = imageNameDecoded.decode("ascii")

    imageNumber = int(re.search("[0-9]+", imageNameDecoded).group(0))
    return imageNumber


def replace_image_name(oldImageName, newImageName, url):
    '''
    TODO: document
    '''
    startIndex = url.find(oldImageName)
    #print("new url is:", url)
    url = url[:startIndex] + newImageName + ".jpg"
    #print("old url is:", url)
    return url


def create_url(imageName, newImageNumber, url):
    '''
    TODO: document
    '''
    imageNameDecoded = COMIC_PREFIX + str(newImageNumber)
    imageNameBytes = imageNameDecoded.encode("ascii")
    imageNameBytesBASE64 = base64.b64encode(imageNameBytes)
    imageNameEncoded = imageNameBytesBASE64.decode("ascii")[:-1]
    newURL = replace_image_name(imageName, imageNameEncoded, url)
    return newURL


def get_image(url, imageName):
    '''
    Downloads image from URL provided; makes get request to provided address
    and stores the raw socket response (stream=True). Next, shutil's copyfileobj
    method copies the contents of this file-like object (the raw response) into
    an actual file (filename.jpg, where filename is the original filename of the
    .jpg stored at the provided address)
    If there is no image stored at the provided address, function returns. (is there a better way to phrase that?)
    '''
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(imageName + '.jpg', 'wb') as out_file: #i know it's dumb to add .jpg back to the end after removing it--cut me some slack, alright?
            shutil.copyfileobj(response.raw, out_file)
    del response #deleting request/filelike object


def get_week(imageName, imageNumber, url):
    '''
    TODO: document
    '''
    i = 2
    while (i <= RANGE):
        imageNumberGuessUp = imageNumber + i
        imageNumberGuessDown = imageNumber - i

        urlGuessUp = create_url(imageName, imageNumberGuessUp, url)
        urlGuessDown = create_url(imageName, imageNumberGuessDown, url)

        nameGuessUp = get_image_name(urlGuessUp)
        nameGuessDown = get_image_name(urlGuessDown)

        get_image(urlGuessUp, nameGuessUp)
        get_image(urlGuessDown, nameGuessDown)

        i += 2

    get_image(url, imageName)    
    return


def main ():
    '''
    TODO: write some documentation lol.
    '''
    url = reformat_url()
    imageName = get_image_name(url)
    imageNumber = get_image_number(imageName)
    get_week(imageName, imageNumber, url)
    
    
if __name__ == "__main__":
    main()