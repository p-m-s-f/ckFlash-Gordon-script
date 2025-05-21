from urllib.parse import unquote #used to undo JavaScript URL encoding
import re #used to identify & isolate different parts of a URL
import base64 #used to decode/encode filenames associated with strip images
import requests #used to GET strip images from the Comics Kingdom website
import shutil #used to write GET response into .jpg files

#This script works by guessing at a range of numbers associated with a strip image URL, which changes only once per week. Therefore,
#I think it makes more sense to define the encoded URL as a global variable, rather than supplying it as a command line input.
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
    from BASE64 easier, it means adding '.jpg' back on the
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
    Given a URL linking to a comic strip, replaces the old image name
    in the URL with a new image name before returning the new URL.
    Note that the new image name may not actually link to an image, and
    that the URL is always expected to be the location of a jpeg image.
    '''
    startIndex = url.find(oldImageName)
    url = url[:startIndex] + newImageName + ".jpg"
    return url


def create_url(imageName, newImageNumber, url):
    '''
    Given a even digit image number, creates an image name using the
    number as a suffix (following the "ckFlash Gordon-ENG-xxxxxxx" format),
    encodes the image name in BASE64, and adds a ".jpg" file suffix to create
    a filename. A new URL is created based on the URL provided, with
    the newly created filename in place of the old one.
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
    .jpg stored at the provided address) However, if there is no image at the
    provided URL, no attempt to download is made.

    I learned of shutil--and borrowed this particular implimentation--from
    this stack overflow post: https://stackoverflow.com/a/18043472
    '''

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(imageName + '.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    del response


def get_week(imageName, imageNumber, url):
    '''
    This is the 'guessing' function. When provided the image number associated with the
    encoded URL's Flash Gordon strip, it guesses at possible image numbers corresponding
    to the rest of the week's strips. Guesses are made within a set range, provided by the
    RANGE variable. Strip numbers are set at increments of two, so guesses are also made
    in increments of two. These strip numbers are not linear--that is, they do not necessarily
    grow larger or smaller throughout the week. They are randomized within this certain range.
    
    Sunday strips fall outside the range of daily strips, and the week's range changes each week.
    Therefore, this script is at its most useful during the beginning of the week (when it can
    retrieve five new strips) than at the end (where the six retrieved strips have already been
    publically released). However, one can access next week's strip range by copying the URL of
    the image which is part of a Comics Kingdom embed.
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
    url = reformat_url()
    imageName = get_image_name(url)
    imageNumber = get_image_number(imageName)
    get_week(imageName, imageNumber, url)
    
    
if __name__ == "__main__":
    main()