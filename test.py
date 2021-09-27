def firststep():
    url = "https://www.palabrasaleatorias.com/random-words.php"
    driver.get(url)
    driver.implicitly_wait(3)
    rez = driver.find_element(By.XPATH, "//td/div")
    global word
    word = rez.text.lower()

    url = "https://www.google.ru/imghp?hl=ru"
    driver.get(url)
    driver.implicitly_wait(3)
    rez = driver.find_element(By.XPATH, "//input")
    rez.send_keys(word)
    rez.send_keys(Keys.ENTER)

    rez = driver.find_element(By.XPATH, "//*[@id='islrg']//img")
    rez.click()
    time.sleep(2)
    elems = driver.find_elements(By.XPATH, ".//div[@id='Sva75c']//a/img")
    if len(elems) > 0:
        for elem in elems:
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
    else:
    print(word,".",format)
