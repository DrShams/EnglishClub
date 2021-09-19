from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import requests

options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
path = "chromedriver.exe"


#STEP 1 GRABBING
def firststep():
    driver = webdriver.Chrome(path,options=options)
    url = "https://www.palabrasaleatorias.com/random-words.php"
    driver.get(url)
    driver.implicitly_wait(3) # seconds
    rez = driver.find_element(By.XPATH, "//td/div")
    global word
    word = rez.text.lower()

    url = "https://www.google.ru/imghp?hl=ru"
    driver.get(url)
    driver.implicitly_wait(3) # seconds
    rez = driver.find_element(By.XPATH, "//input")
    rez.send_keys(word)
    rez.send_keys(Keys.ENTER)

    rez = driver.find_element(By.XPATH, "//*[@id='islrg']//img")
    rez.click()
    time.sleep(2)
    elems = driver.find_elements(By.XPATH, ".//div[@id='Sva75c']//a/img")
    for elem in elems:
        #print(elem)
        picture_url = elem.get_attribute("src")
        print("picture has url: \n",picture_url)
        if '.jpg' in picture_url:
            format = 'jpg'
        elif '.jpeg' in picture_url:
            format = 'jpeg'
        elif '.png' in picture_url:
            format = 'png'
        else:
            print("there is no valid picture for the word",word)
            driver.close()
            return False
        break
    r = requests.get(picture_url, allow_redirects=True)
    print(word,".",format)
    global name
    name = 'pictures/' + word + "." + format
    open(name, 'wb').write(r.content)
    driver.close()

#STEP 2 VK
import time
import vk_api

def secondstep():
    driver = webdriver.Chrome(path,options=options)
    url = "https://dictionary.cambridge.org/dictionary/english/" + word
    print(url)
    driver.get(url)
#    driver.close()


def main():
    """ Пример загрузки фото """

    login, password = '79656559552', 'Xa5xv9958!@'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    """ В VkUpload реализованы методы загрузки файлов в ВК
    """

    upload = vk_api.VkUpload(vk_session)
    print(name)
    photo = upload.photo(

        name,
        album_id=279409061,
        group_id=''
    )

    vk_photo_url = 'https://vk.com/photo{}_{}'.format(
        photo[0]['owner_id'], photo[0]['id']
    )

    print(photo, '\nLink: ', vk_photo_url)

    photourl = 'photo' + str(photo[0]['owner_id']) + '_' + str(photo[0]['id'])
    print(photourl)
    vk = vk_session.get_api()
    print(vk.wall.post(attachments = photourl,message=word))

if __name__ == '__main__':
    #firststep()
    if firststep() is False:
        #rint("no valid")
        firststep()
    else:
        #print("True valid")
        secondstep()
    #else:
        #main()
