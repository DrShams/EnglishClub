from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-webgl")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
path = r'chromedriver.exe'
driver = webdriver.Chrome(path,options=options)

for x in range(1000):
    url = "https://www.palabrasaleatorias.com/random-words.php"
    driver.get(url)
    url = "https://www.google.ru/imghp?hl=ru"
    print(x,"Test[1]")
    driver.get(url)
    print(x,"Test[2]")
driver.close()
