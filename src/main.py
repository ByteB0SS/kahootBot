from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


#kahoot_link = input("Link do jogo da semana: ")
kahoot_link = "https://kahoot.it/solo/07533d80-c426-4d3d-80a8-3ae49e557d12_1778268179845"
email = "albertojoao32@gmail.com"
name = "bananagato"
asks = []


driver = webdriver.Chrome()
driver.maximize_window()
driver.get(kahoot_link)
wait = WebDriverWait(driver, 120)


input_email = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-functional-selector="username-input"]'))
)
input_email.click()
input_email.send_keys(email)

send_nickname = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="join-button-username"]'))
)
send_nickname.click()


input_nickname = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-functional-selector="username-input"]'))
)
input_nickname.click()
input_nickname.send_keys(name)

send_nickname = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="join-button-username"]'))
)
send_nickname.click()

ask  = wait.until(
    EC.element_to_be_clickable
)

buttons = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, 'form button')
    )
)

wait.until(
    EC.element_to_be_clickable(buttons[0])
)

buttons[0].click()

sleep(100)

driver.quit()