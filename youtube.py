from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

link = "https://www.youtube.com/watch?v=88iypMO9H7g"

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(link)
driver.switch_to.frame(driver.find_element_by_xpath('//iframe[starts-with(@src, "https://www.youtube.com/embed")]'))
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Play"]'))).click()

driver.quit()
