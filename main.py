from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from gui import GuiApp
from config import Config
from web_interaction import *

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

def main():
    """Funzione principale che orchestrare tutto il processo"""
    root = tk.Tk()
    app = GuiApp(root)
    root.mainloop()

    if not hasattr(app, "certificato") or not hasattr(app, "indirizzo_ip"):
        print("Dati non completi, uscita dal programma")
        return
    
    cert = app.certificato
    ip = app.indirizzo_ip

    print("Dati raccolti dalla GUI:")
    print(f"Reparto: {cert.reparto}")
    print(f"Nome: {cert.nome}")
    print(f"Email: {cert.email}")

    options = Config.get_chrome_options()

    service = Service(ChromeDriverManager().install())
    driver = None
    

    try:
        driver = webdriver.Chrome(service=service, options=options)

        domain = f"{ip}/wcd/spa_login.html"

        protocol, final_url = smart_page_load(driver, domain)
        # Prova a trovare l'errore con timeout breve
        try:
            
            WebDriverWait(driver, Config.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, "main-frame-error")))
                
            # Se arriviamo qui, c'è un errore
            print("Trovato errore, provo HTTP...")
            driver.get(f"http://{ip}/wcd/spa_login.html")
        except TimeoutException:
            print("Pagina caricata correttamente")

        driver.maximize_window()
        
        driver.implicitly_wait(5)

        esegui_automazione(driver, cert)
        
    except Exception as e:
        print(f"Errore automazione: {e}")
        
    finally:
        if driver:
            try:
                logout_finally()
            except: 
                driver.quit()

def esegui_automazione(driver, cert):
    init_web_interaction(driver)

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
        print(f"Errore durante sequenza automazione: {e}")
        raise

if __name__ == "__main__":
    main()