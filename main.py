from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from gui import GuiApp
from web_interaction import smart_page_load, login_amministratore, disattiva_funzioni_usb, crea_certificato, compila_certificato, abilita_ssl, rimuovi_verifica_cert, imposta_stampa_no_aut, disattiva_dpws, imp_web_dav, imp_open_api, logout_finally

def click_until_selected():
    try:
        row = driver.find_element(By.XPATH, "//tr[@data-index='0']")
        print(row)
        row.click()

        WebDriverWait(driver, 3).until(lambda driver: "info" in driver.find_element(By.XPATH, "//tr[@data-index='0']").get_attribute("class"))
        print("Riga selezionata")
        return True
    except TimeoutException:
        return False


if __name__ == "__main__":
    root = tk.Tk()
    app = GuiApp(root)
    root.mainloop()

if hasattr(app, "certificato"):
    cert = app.certificato
    ip = app.indirizzo_ip
    print("Dati raccolti dalla GUI:")
    print(f"Reparto: {cert.reparto}")
    print(f"Nome: {cert.nome}")
    print(f"Email: {cert.email}")

    options = Options()
    options.add_argument("--incognito")
   # Opzioni per ignorare errori SSL/certificati
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors-type')
    options.add_argument('--accept-insecure-certs')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--test-type')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("prefs", {
        "directory_upgrade": True,
        "profile.default_content_settings.popups": 0,
        "plugins.always_open_pdf_externally": True,
        "profile.default_content_setting_values.automatic_downloads": 1,
        "safebrowsing.enabled": True
    })


    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    page_source = driver.page_source.lower()
    

    domain = f"{ip}/wcd/spa_login.html"

    protocol, final_url = smart_page_load(driver, domain)

    try:
        # Prova a trovare l'errore con timeout breve
        wait_short = WebDriverWait(driver, 2)
        wait_short.until(EC.presence_of_element_located((By.ID, "main-frame-error")))
        
        # Se arriviamo qui, c'è un errore
        print("Trovato errore, provo HTTP...")
        driver.get(f"http://{ip}/wcd/spa_login.html")
    
    except TimeoutException:
        # Nessun errore trovato = successo!
        print("Pagina caricata correttamente, procedo...")

    driver.maximize_window()
    
    driver.implicitly_wait(5)
    
    try:
        login_amministratore()

        disattiva_funzioni_usb()

        crea_certificato()
        
        compila_certificato(cert)

        abilita_ssl()
        
        rimuovi_verifica_cert()

        imposta_stampa_no_aut()

        disattiva_dpws()

        imp_web_dav()

        imp_open_api()

    except Exception as e:
        print(f"Errore: {e}")
    
    finally:
        logout_finally()


else:
    print("Nessun certificato inserito")


