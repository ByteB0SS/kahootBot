from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from utils.get_quiz import get_quiz


kahoot_link = "https://kahoot.it/challenge/08763903?challenge-id=3d2fdc30-3133-4e33-ac25-b05d1b8af52b_1779443089898"
email = "rubemernesto2@gmail.com"
name = "ruba"


from urllib.parse import urlparse, parse_qs

parsed = urlparse(kahoot_link)
kahoot_id = parse_qs(parsed.query).get("challenge-id", [None])[0]

asks = get_quiz(kahoot_id)
print(asks)
asks = asks['questions']

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(kahoot_link)
wait = WebDriverWait(driver, 120)


read = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-functional-selector="namerator-continue-button"]'))
)
read.click()

print(len(asks))
for ask in asks:
    wait.until(lambda d: len(d.find_element(By.CSS_SELECTOR, "h1").text.strip()) > 5)
    current_h1 = driver.find_element(By.CSS_SELECTOR, "h1").text

    print(f"Pergunta: {ask['title']}")

    buttons = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "form button"))
    )

    sleep(0.5)

    correct_answer = next(
        (c["text"] for c in ask["choices"] if c["correct"]),
        None
    )

    clicked = False
    for btn in buttons:
        if correct_answer and correct_answer.strip() == btn.text.strip():
            wait.until(EC.element_to_be_clickable(btn))
            btn.click()
            clicked = True
            print(f"  ✓ Respondido: {correct_answer}")
            break

    if not clicked:
        print(f"  ⚠ Resposta não encontrada: {correct_answer!r}")
        print(f"  Botões disponíveis: {[b.text for b in buttons]}")

    next_btn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-functional-selector="nano-next-button"]')
        )
    )
    next_btn.click()
    sleep(0.5)
    next_btn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-functional-selector="nano-next-button"]')
        )
    )
    driver.execute_script("arguments[0].click();", next_btn)

    sleep(1)
    print(f"  H1 atual: {driver.find_element(By.CSS_SELECTOR, 'h1').text!r}")
    wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "h1").text != current_h1)
    print(f"  H1 depois do wait: {driver.find_element(By.CSS_SELECTOR, 'h1').text!r}")
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "form button")))
    print(f"  Botões encontrados, avançando loop")


sleep(100)
driver.quit()