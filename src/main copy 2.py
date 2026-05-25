from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from utils.get_quiz import get_quiz


kahoot_link = "https://kahoot.it/solo/07533d80-c426-4d3d-80a8-3ae49e557d12_1779474250522"
email = "rubemernesto2@gmail.com"
name = "ernest"


parsed = urlparse(kahoot_link)

if "challenge-id" in parsed.query:
    kahoot_id = parse_qs(parsed.query).get("challenge-id", [None])[0]
else:
    kahoot_id = parsed.path.split('/')[-1]


asks = get_quiz(kahoot_id)['questions']

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(kahoot_link)
wait = WebDriverWait(driver, 120)


input_email = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-functional-selector="participant-id-input"]'))
)
input_email.click()
input_email.send_keys(email)

send_email = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="send-player-id"]'))
)
send_email.click()


input_nickname = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-functional-selector="username-input"]'))
)
input_nickname.click()
input_nickname.send_keys(name)

send_nickname = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="join-button-username"]'))
)
send_nickname.click()


for i, ask in enumerate(asks):
    print(f"Pergunta {i+1}: {ask['title']}")

    correct_text = next(
        (c["text"] for c in ask["choices"] if c["correct"]),
        None
    )

    if correct_text is None:
        print(f"  ⚠ Preenche manualmente e avança!")
        wait.until(lambda d: not d.find_elements(By.CSS_SELECTOR, "form button"))
        continue

    wait.until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "form button")) >= len(ask["choices"])
    )
    sleep(0.5)

    buttons = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "form button"))
    )

    for btn in buttons:
        btn_text = btn.get_attribute("innerText").strip()
        if correct_text.strip() in btn_text:
            wait.until(EC.element_to_be_clickable(btn))
            btn.click()
            print(f"  ✓ Respondido: {correct_text}")
            break

    # espera botão existir
    next_btn = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-functional-selector="nano-next-button"]')
        )
    )

    # espera ficar clicável
    next_btn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-functional-selector="nano-next-button"]')
        )
    )

    # garante que está visível na tela
    driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)

    # clique real (mais confiável no Kahoot)
    driver.execute_script("arguments[0].click();", next_btn)

    # espera UI mudar (evita clique “perdido”)
    wait.until(
        EC.staleness_of(next_btn)
    )
    sleep(1)


sleep(100)
driver.quit()