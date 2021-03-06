from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import sqlite3
import requests
import time
import os

path = os.path.abspath("files/")
os.environ["PATH"] += os.pathsep + path

conn = sqlite3.connect('files/dict.sqlite',check_same_thread=False)
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS "Dictionary"(
    'id' INTEGER,
    'word' TEXT,
    'path' TEXT,
    'one' TEXT,
    'two' TEXT,
    'three' TEXT,
    PRIMARY KEY("id" AUTOINCREMENT));'''
)
#STEP 1 GRABBING
def firststep():
    url = "https://www.palabrasaleatorias.com/random-words.php"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    block = soup.find_all("div")[1] #get second div
    global word
    word = str(block.text.strip())

    url = "https://www.google.ru/imghp?hl=ru"
    driver.get(url)
    driver.implicitly_wait(3) #seconds
    elem = driver.find_element(By.XPATH, "//input")
    elem.send_keys(word)
    elem.send_keys(Keys.ENTER)

    elem = driver.find_element(By.XPATH, "//*[@id='islrg']//img")
    elem.click()
    time.sleep(2)
    pictures = driver.find_elements(By.XPATH, ".//div[@id='Sva75c']//a/img")
    if len(pictures) < 1:
        print("there is no pictures at all",word)
        firststep()
        return True
    for elem in pictures:
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
            firststep()
            return True
        break
    print(word,".",format)
    global path_pic
    path_pic = 'files/pictures/' + word + "." + format
    try:
        with open(path_pic, 'wb') as f:
            r = requests.get(picture_url, stream=True)
            for block in r.iter_content(1024):
                if not block:
                    break
                f.write(block)
    except:
        print("[x]problem with connection")

#STEP 2 VK
def secondstep():
    url = "https://dictionary.cambridge.org/dictionary/english/" + word
    print(url)
    driver.get(url)
    wdefs = driver.find_elements(By.CLASS_NAME,"def-block")
    count = 0
    if len(wdefs) > 1:
        print("definitions of the word:",word)
    else:
        print("definition of the word:",word)
    wordlist = list()
    deflist = list()
    for wdef in wdefs:
        if count == 3: break
        count += 1
        try:
            title = wdef.find_element(By.CSS_SELECTOR,".def.ddef_d")
        except:
            print("[x] The is no title element")
            continue
        try:
            titledef = wdef.find_element(By.CLASS_path_pic,"eg")
            titledeftext = titledef.text
        except:
            titledeftext = None
        symbol = str(title.text)[-1:]
        if symbol == ':':
            title_fmt = str(title.text)[:-1]
        else:
            title_fmt = str(title.text)

        if titledeftext is not None:
            deflist.append(title_fmt+titledeftext)
            print("["+str(count)+"]",title_fmt,titledeftext)
        else:
            deflist.append(title_fmt)
            print("["+str(count)+"]",title_fmt)

    one = two = three = None
    words = len(deflist)
    if words == 1:
        one = deflist[0]
    elif words == 2:
        one = deflist[0]
        two = deflist[1]
    elif words == 3:
        one = deflist[0]
        two = deflist[1]
        three = deflist[2]
    else:
        print("there is no words")

    cur.execute('SELECT id FROM Dictionary WHERE word = ?',(word,))
    row = cur.fetchone()#fix this func
    conn.commit()
    if row is None:
        cur.execute('INSERT INTO Dictionary (word, path, one, two, three) VALUES (?, ?, ?, ?, ?)',
        (word, path_pic, one, two, three))
        conn.commit()
    else:
        id = row[0]
        print(word, "is already in the database with id=",id)

def exfunction(num = 1000):
    global driver
    driver = Firefox()
    for wordcount in range(num):
        print("word #",wordcount+1)
        firststep()
        secondstep()
    driver.close()

if __name__ == '__main__':
    exfunction()
