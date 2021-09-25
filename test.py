from selenium import webdriver
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

today_date = datetime.today().strftime('%Y-%m-%d')
driver = webdriver.Chrome()
#driver.implicitly_wait(30)
wait = WebDriverWait(driver, 30)
driver.get("https://forms.gle/VUwbshGuXxDb7NRbA")
time.sleep(1)
date= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.quantumWizTextinputPaperinputInput")))
driver.execute_script(f"arguments[0].setAttribute('value', '{today_date}')", date)
next = driver.find_element_by_css_selector("#mG61Hd > div.freebirdFormviewerViewFormCard.exportFormCard > div > div.freebirdFormviewerViewNavigationNavControls > div > div.freebirdFormviewerViewNavigationLeftButtons > div > span").click()
