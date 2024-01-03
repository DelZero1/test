import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Otvorite stranicu za logiranje
driver.get('https://partner.xometry.eu/profile/sign_in?locale=en')

# Logiranje koristeći Selenium
driver.find_element(By.ID, 'basic_email').send_keys('zia.printing.3d@gmail.com')
driver.find_element(By.ID, 'basic_password').send_keys('zia.printing.3d')
submit_button = driver.find_element(By.CLASS_NAME, 'SignUp_applyBtn__MmpA6')
submit_button.click()

# Čekanje na pojavu Shadow DOM host elementa
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='uc-app-container']"))
)

# Izvršavanje JavaScripta za simuliranje događaja miša nad gumbom "Accept All"
try:
    driver.execute_script("""
    let shadowHost = document.querySelector('[data-testid="uc-app-container"]');
    let shadowRoot = shadowHost.shadowRoot;
    let button = shadowRoot.querySelector("[data-testid='uc-accept-all-button']");
    if (button) {
        // Simulacija događaja miša
        let clickEvent = new MouseEvent('click', {
            bubbles: true,
            cancelable: true,
            view: window
        });
        button.dispatchEvent(clickEvent);
    } else {
        throw new Error('Gumb nije pronađen');
    }
    """)
except Exception as e:
    print("Došlo je do greške prilikom simuliranja klika na gumb za prihvaćanje kolačića:", e)



# Pređite na stranicu s podacima
driver.get('https://partner.xometry.eu/offers?locale=en')

# Čekanje na učitavanje stranice
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#css_selector_for_elements_containing_word"))
)

# Dohvatite HTML sadržaj i pretražite riječ "ABS"
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
search_word = 'ABS'
elements = soup.select('#css_selector_for_elements_containing_word')  # Ažurirajte CSS selektor
word_count = sum(element.text.lower().count(search_word.lower()) for element in elements)
print(f"Riječ '{search_word}' se pojavljuje {word_count} puta u odabranim elementima na stranici.")

# Zatvorite preglednik

