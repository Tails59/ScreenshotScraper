from PIL import Image
from bs4 import BeautifulSoup
from io import BytesIO
import requests
import atexit
import cloudscraper
import settings
import random
import time
import string

letters = None
numbers = None
scraper = None


def start():
    global letters, numbers, scraper

    load()
    if letters is None or letters == '' or numbers is None or numbers == '':
        letters = 'aa'
        numbers = '0000'

    for iteration in range(1, settings.SEARCH_ITERATIONS):
        print("Attempt " + str(iteration))
        scraper = cloudscraper.create_scraper()
        page_content = make_request()
        get_image_from_response(page_content)
        generate_link()
        time.sleep(settings.SEARCH_DELAY / 1000)


def generate_link():
    global letters, numbers

    if settings.SEARCH_MODE == "RAND":
        letters = random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase)
        numbers = ''.join(random.choice(string.digits) for _ in range(4))
    elif settings.SEARCH_MODE == "SEQ":
        return


def save():
    if settings.SEARCH_MODE == "RAND":
        return

    global letters, numbers

    with open('last.txt', 'w') as save_file:
        save_file.write(letters + "\n" + numbers)
        save_file.close()


def load():
    if settings.SEARCH_MODE == "RAND":
        generate_link()
        return

    global letters, numbers
    with open('last.txt', 'r') as save_file:
        lines = save_file.readlines()
        save_file.close()

    letters = lines[0].strip()
    numbers = lines[1]


def make_request():
    url = "https://prnt.sc/" + letters + numbers
    response = scraper.get(url)
    status = response.status_code

    # do some error handling with the status code,

    return response.text


def get_image_from_response(page_content):
    soup = BeautifulSoup(page_content, features="html.parser")
    image = soup.find('img', id="screenshot-image")
    image_url = image['src']
    # print(image_url)

    # If image was removed, it displays an image and the url always starts with //
    if image_url.startswith("//"):
        print(letters + numbers + " - Image deleted by user/server")
        return None

    if requests.get(image_url).status_code == "404":
        print(letters + numbers + " - Status 404")
        return None

    response_data = scraper.get(image_url)

    try:
        img = Image.open(BytesIO(response_data.content))
        img.save("images/" + letters + numbers + ".png")
        print("Image acquired")
    except Exception as excp:
        #print(excp)
        print(letters + numbers + " - Invalid image (was probably deleted from server")


atexit.register(save)
start()
