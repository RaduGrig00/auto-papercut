from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from utils import wait_random_time, torna_indietro
from certificato import Certificato

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
wait = WebDriverWait(driver, 10)


def smart_page_load(driver, domain, timeout=10):
    """
    Carica la pagina e determina se ha avuto successo o è andato in errore
    """
    
    https_url = f"https://{domain}"
    print(f"Tentativo HTTPS: {https_url}")
    
    try:
        driver.get(https_url)
        time.sleep(3)  # Attendi caricamento
        
        # Controlla se c'è una pagina di errore
        try:
            # Prova a trovare elementi di errore con timeout breve
            error_element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "main-frame-error"))
            )
            print("Trovata pagina di errore HTTPS")
            return "error", None
            
        except TimeoutException:
            # Nessun errore trovato = successo!
            print("HTTPS caricato con successo")
            return "https", driver.current_url
            
    except Exception as e:
        print(f"Errore generale: {e}")
        return "error", None

def load_page_with_protocol_detection(driver, domain):
    """
    Carica la pagina e gestisce automaticamente HTTPS/HTTP
    """
    
    # Prova prima HTTPS
    result, final_url = smart_page_load(driver, domain)
    
    if result == "https":
        print("Usando HTTPS - procedimento sicuro")
        return "https", final_url
        
    elif result == "error":
        print("HTTPS fallito, provo HTTP...")
        
        # Prova HTTP
        http_url = f"http://{domain}"
        try:
            driver.get(http_url)
            
            # Attendi caricamento
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            print("HTTP caricato con successo")
            return "http", driver.current_url
            
        except Exception as e:
            print(f"Anche HTTP fallito: {e}")
            return None, None
    
    return None, None

#Funzione che interagisce con gli elementi del DOM per eseguire il login da Amministratore
def login_amministratore():
    try:
        #Switcho al iframe SPA-contents-body
        driver.switch_to.frame("SPA-contents-body")

        #cerco e clicco sul bottone a dropdown per la selezione del tipo utente
        wait.until(EC.element_to_be_clickable((By.ID, "ID_LGI_TYPE_BT"))).click()
        wait_random_time()

        #cerco e clicco, selezionando, il tipo di utente: amministratore
        wait.until(EC.element_to_be_clickable((By.ID, "ID_LGI_TYPE_ADMIN"))).click()
        wait_random_time()

        #inserisco la password nel campo apposito
        driver.find_element(By.ID, "ID_LGI_PASS").send_keys("12345678")
        wait_random_time()

        #cerco e clicco sul bottone per confermare il login
        wait.until(EC.element_to_be_clickable((By.ID, "ID_LGI_LOGIN_BT"))).click()
        wait_random_time()
    except Exception as e:
        print(f"Errore login admin: {e}")

def disattiva_funzioni_usb():
    #Switcho al frame principale
    driver.switch_to.default_content()

    #Cerco e clicco navigando nel menù sicurezza
    wait.until(EC.element_to_be_clickable((By.ID, "ID_Menu_Security"))).click()
    wait_random_time()

    #Cerco e clicco navigando nel sottomenù "Impostazione di sicurezza rapida"
    wait.until(EC.element_to_be_clickable((By.ID, "ID_SubMenu_Security_SimpleSecuritySetting"))).click()
    wait_random_time()

    #Switcho al frame SPA-contents-body
    driver.switch_to.frame("SPA-contents-body")

    #Trovo l'elemento della pagina che si può scrollare per andare in fondo alla pagina e vedere tutti i checkbox
    scrollable_div = driver.find_element(By.ID, "SPA-contents-html")

    #Vado in fondo alla pagina
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)

    #creo una lista contenente tutti gli id delle checkbox
    checkbox_ids = ["AN_SSE_USD_checked", "AN_SSE_USP_checked", "AN_SSE_USN_checked", "AN_SSE_UPP_checked", "AN_SSE_APC_checked"]

    #trovo ogni checkbox corrispondente agli id e se selezionate, trovo e clicco sul fieldset per disattivarle
    for checkbox_id in checkbox_ids:
        checkbox = driver.find_element(By.ID, checkbox_id)

        if checkbox.is_selected():
            fieldset = checkbox.find_element(By.XPATH, "../..")
            fieldset.click()
            wait_random_time()
    
    #trovo e clicco sul bottone ok per confermare la configurazione
    wait.until(EC.element_to_be_clickable((By.ID, "ID_Ok"))).click()
    time.sleep(2)

def crea_certificato():
    #Switcho al frame di default
    driver.switch_to.default_content()

    #Cerco e clicco sul bottone per navigare nel sottomenù "Impostazioni PKI"
    wait.until(EC.element_to_be_clickable((By.ID, "ID_SubMenu_Security_SSLSetting"))).click()
    wait_random_time()

    #Cerco e clicco sul bottone per navigare nel sottomenù "Impostazione certificato dispositivo" 
    wait.until(EC.element_to_be_clickable((By.ID, "ID_SpareSubMenu_Security_DeciceCertSetting"))).click()
    wait_random_time()

    #Switcho al frame SPA-contents-body
    driver.switch_to.frame("SPA-contents-body")

    #Se trovo nel codice sorgente 'No matching records found' significa che non ci sono certificati e posso procedere
    #con la registrazione di uno nuovo, altrimenti lo cancello e lo creo
    try:
        #Cerco questo elemento che mi indica l'assenza di certificati presenti, in caso non ci fosse scatta l'exception dove elimino il cert.
        driver.find_element(By.XPATH, "//td[text()='No matching records found']")
        
        #Se viene trovato si passa direttamente alla creazione del certificato, quindi cerco e clicco sul bottone per la nuova registrazione
        wait.until(EC.element_to_be_clickable((By.ID, "ID_REGIST_INFO_BTN"))).click()
        wait_random_time()
    #qui segue la logica in caso sia presente già un certificato e bisogna prima eliminarlo
    except NoSuchElementException:
        #cerco e clicco la riga che indica il certificato per selezionarlo
        wait.until(EC.element_to_be_clickable((By.XPATH, "//tr[@data-index='0']"))).click()
        wait_random_time()

        #cerco e clicco il bottone impostazione per accedere all'eliminazione del cert.
        wait.until(EC.element_to_be_clickable((By.ID, "ID_SETTING_BTN"))).click()
        wait_random_time()

        #cerco e clicco il bottone ok per selezionare l'eliminazione
        wait.until(EC.element_to_be_clickable((By.ID, "ID_OK"))).click()
        wait_random_time()

        #cerco e clicco il bottone ok per confermare l'eliminazione
        wait.until(EC.element_to_be_clickable((By.ID, "ID_BTN_OK"))).click()
        wait_random_time()

        # RICARICA LA PAGINA DOPO AVER ELIMINATO IL CERTIFICATO
        print("Ricarico la pagina dopo eliminazione certificato...")
        time.sleep(3)  # Aspetta che il certificato sia effettivamente eliminato
        driver.refresh()
        wait_random_time()

        #Switcho al frame default
        driver.switch_to.default_content()

        #Navigo di nuovo fino alla pagina di creazione certificato
        wait.until(EC.presence_of_element_located((By.ID, "ID_Menu_Security"))).click()
        wait_random_time()

        wait.until(EC.presence_of_element_located((By.ID, "ID_SubMenu_Security_SSLSetting"))).click()
        wait_random_time()

        wait.until(EC.presence_of_element_located((By.ID, "ID_SpareSubMenu_Security_DeciceCertSetting"))).click()
        wait_random_time()

        #switcho al frame SPA-contents-body
        driver.switch_to.frame("SPA-contents-body")

        #Cerco e clicco il bottone per creare un nuovo certificato
        wait.until(EC.presence_of_element_located((By.ID, "ID_REGIST_INFO_BTN"))).click()
        wait_random_time()

    #Cerco e clicco il bottone ok per confermare l'intenzione
    wait.until(EC.presence_of_element_located((By.ID, "ID_OK"))).click()
    wait_random_time()

def compila_certificato(cert):
    try:
        #Cerca il campo reparto e lo compila con i dati ricevuti dall'input dell'utente
        driver.find_element(By.ID, "ASE_SSL_ORG").send_keys(cert.reparto)
        wait_random_time()

        #Cerca il campo nome e lo compila con i dati ricevuti dall'input dell'utente
        driver.find_element(By.ID, "ASE_SSL_UNI").send_keys(cert.nome)
        wait_random_time()

        #Cerca il campo località e lo compila con i dati ricevuti dall'input dell'utente
        driver.find_element(By.ID, "ASE_SSL_LOC").send_keys(cert.localita)
        wait_random_time()

        #Cerca il campo provincia e lo compila con i dati ricevuti dall'input dell'utente
        driver.find_element(By.ID, "ASE_SSL_STA").send_keys(cert.provincia)
        wait_random_time()

        #Cerca il campo paese e lo compila con i dati ricevuti dall'input dell'utente
        driver.find_element(By.ID, "ASE_SSL_COU").send_keys(cert.paese)
        wait_random_time()

        #Cerca il campo email e lo compila con i dati ricevuti dall'input dell'utente
        driver.find_element(By.ID, "ASE_SSL_AAD").send_keys(cert.email)
        wait_random_time()

        #Cerca il campo del periodo di validità, lo pulisce e inserisce il nuovo valore di 3600
        data_val = wait.until(EC.presence_of_element_located((By.ID, "ASE_SSL_VAL")))
        data_val.clear()
        data_val.send_keys("3600")
        wait_random_time()

        #Cerca e clicca il dropdown che contiene i tipi di chiavi crittografiche
        driver.find_element(By.XPATH, "//button[@data-toggle='dropdown']").click()
        wait_random_time()

        #Cerca e individua l'elemento scrollabile
        scrollable_ul = driver.find_element(By.XPATH, "//ul[@role='menu']")
        #Una volta individuato lo scrolla verso il basso
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_ul)
        wait_random_time()

        #Cerca e seleziona il valore RSA2048_SHA_256
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-value='Rsa2048_SHA_256']"))).click()
        wait_random_time()
    except Exception as e:
        print(f"Errore compilazione certificato:{e}")

    try:
        #Cerca e clicca (con js) il bottone di okay per confermare il certificato
        element = wait.until(EC.presence_of_element_located((By.ID, "ID_ASE_BTN_OK")))
        driver.execute_script("arguments[0].click();", element)
        wait_random_time()

        #Cerca e clicca il bottone di okay del popup
        wait.until(EC.presence_of_element_located((By.ID, "ID_CGI_OK"))).click()
        wait_random_time()
        
    except Exception as e:
        print(f"Eccezione catturata dopo conferma certificato: {e}")

def abilita_ssl():
    try:
        #Switcha frame default 
        driver.switch_to.default_content()

        #Cerca e clicca il sottomenù Abilita versione SSL per navigarci
        wait.until(EC.element_to_be_clickable((By.ID, "ID_SpareSubMenu_Security_UseSslSetting"))).click()
        wait_random_time()

        #Switcha frame SPA-contents-body
        driver.switch_to.frame("SPA-contents-body")

        #Cerca e clicca il bottone del dropdown contenente la modalità in cui abilitare SSL
        wait.until(EC.presence_of_element_located((By.ID, "c63633200654865962100988"))).click()
        wait_random_time()

        #Cerca e seleziona la modalità Utente e Amministratore
        wait.until(EC.presence_of_element_located((By.ID, "c63633200968803222601203"))).click()
        wait_random_time()

        #Cerca e clicca il bottone ok per confermare la configurazione
        wait.until(EC.presence_of_element_located((By.ID, "ID_BTN_OK"))).click()
        time.sleep(5)
    except Exception as e:
        print(f"Eccezione catturata dopo abilita ssl: {e}")

def rimuovi_verifica_cert():
    try:
        #Switch al frame default
        driver.switch_to.default_content()

        # Cerca il link per tornare alla schermata precedente e lo clicca
        torna_indietro(wait)

        # Cerca il link Impost. verifica certificato e lo clicca
        wait.until(EC.presence_of_element_located((By.ID, "ID_SubMenu_Security_CertVerifiSetting"))).click()
        wait_random_time()

        #Switcha al frame SPA-contents-body
        driver.switch_to.frame("SPA-contents-body")

        # Cerca e clicca (se attivo) disattivando il fieldset impost. verifica certificato 
        checkbox = driver.find_element(By.ID, "ID_ASE_CEV_SET_checked")
        if checkbox.is_selected():
            fieldset = checkbox.find_element(By.XPATH, "../..")
            fieldset.click()
            wait_random_time()

        # Cerca e clicca il tasto ok per confermare l'impostazione
        wait.until(EC.presence_of_element_located((By.ID, "ID_OK_ASE_CEV_CEV"))).click()
        wait_random_time()
    except Exception as e:
        print(f"Eccezione catturata dopo rimozione verifica certificato: {e}")

def imposta_stampa_no_aut():
    try:
        #Switch al frame default
        driver.switch_to.default_content()

        #Cerca e clicca il link per tornare indietro di un menù
        torna_indietro(wait)

        #Cerca e clicca il link per andare autent.utente/perc. voce cost
        wait.until(EC.presence_of_element_located((By.ID, "ID_Menu_Authentication"))).click()
        wait_random_time()

        #Cerca e clicca il link per il menù stampa senza aut.
        wait.until(EC.presence_of_element_located((By.ID, "ID_SubMenu_Authentication_NoAuthPrintOn"))).click()
        wait_random_time()
            
        #Switch al frame SPA-contents-body
        driver.switch_to.frame("SPA-contents-body")

        #Cerca e clicca il menu a tendina per la stampa senza aut
        wait.until(EC.presence_of_element_located((By.ID, "ID_AA_AUT_APE"))).click()
        wait_random_time()

        #Cerca e clicca l'opzione colore pieno/nero
        wait.until(EC.presence_of_element_located((By.ID, "ID_AA_AUT_APE_Color"))).click()
        wait_random_time()

        #Cerca e clicca il bottone ok per confermare
        wait.until(EC.presence_of_element_located((By.ID, "ID_OK_AA_LLF_LL"))).click()
        wait_random_time()
    except Exception as e:
        print(f"Eccezione catturata dopo impostazione stampa no autenticazione: {e}")

def disattiva_dpws():
    try:
        #Switch frame default
        driver.switch_to.default_content()

        #Cerco e clicco il link per tornare indietro di un menù
        torna_indietro(wait)

        #Cerco e clicco il link per andare nel menù rete
        wait.until(EC.presence_of_element_located((By.ID, "ID_Menu_Network"))).click()
        wait_random_time()

        #Cerco e clicco il link per andare nel sottomenù DPWS
        wait.until(EC.presence_of_element_located((By.ID, "ID_SubMenu_Network_WebServiceSetting"))).click()
        wait_random_time()

        #Cerco e clicco il link per andare nel sottomenù Imp. comuni DPWS
        wait.until(EC.presence_of_element_located((By.ID, "ID_SpareSubMenu_Network_WebServiceCommonSetting"))).click()
        wait_random_time()

        driver.switch_to.frame("SPA-contents-body")

        # Cerco e clicco disattivando i fieldset per disattivare il DPWS, se attivi
        checkbox_ids = ["ID_AN_WEB_PSV_checked", "ID_AN_WEB_EXD_checked", "ID_AN_WEB_KYD_checked", "ID_AN_WEB_CHD_checked", "ID_AN_WEB_LCD_checked"]
        for checkbox_id in checkbox_ids:
            checkbox = driver.find_element(By.ID, checkbox_id)

            if checkbox.is_selected():
                fieldset = checkbox.find_element(By.XPATH, "../..")
                fieldset.click()
                wait_random_time()

        #Cerco e clicco il bottone ok per confermare
        wait.until(EC.presence_of_element_located((By.ID, "ID_OK_AN_WEB_SR"))).click()
        wait_random_time()
    except Exception as e:
        print(f"Eccezione catturata durante disattivazione dpws: {e}")

def imp_web_dav():
    try:
        #Switch a frame default
        driver.switch_to.default_content()

        #Cerco e clicco il link per tornare indietro di un menù
        torna_indietro(wait)

        #Cerco e clicco il link per andare nel sottomenù WebDAV
        wait.until(EC.presence_of_element_located((By.ID, "ID_SubMenu_Network_WebDAVSetting"))).click()
        wait_random_time()

        #Cerco e clicco il link per andare nel sottomenù Imp. client WebDAV
        wait.until(EC.presence_of_element_located((By.ID, "ID_SpareSubMenu_Network_WebDAVClientSetting"))).click()
        wait_random_time()

        #Switch frame SPA-contents-body
        driver.switch_to.frame("SPA-contents-body")

        #Cerco e controllo che il checkbox "Imp. TX WebDAV sia attivo, altrimenti lo attivo e confermo l'impostazione"
        try:
            checkbox = driver.find_element(By.ID, "ID_AN_DAV_CLI_checked")
            if not checkbox.is_selected():
                fieldset = checkbox.find_element(By.XPATH, "../..")
                fieldset.click()
                wait_random_time()
                #Eventuale conferma configurazione con click su tasto ok
                wait.until(EC.element_to_be_clickable((By.ID, "ID_OK_AN_DAV_CLI"))).click()
                wait_random_time()
        except Exception as e:
            print(f"Errore durante gestione checkbox: {e}")
        
        #Switch frame default
        driver.switch_to.default_content()

        #Cerco e clicco il link per andare nel sottomenù Imp. server WebDAV
        wait.until(EC.element_to_be_clickable((By.ID, "ID_SpareSubMenu_Network_WebDAVServerSetting"))).click()
        wait_random_time()

        #Switch frame SPA-contents-body
        driver.switch_to.frame("SPA-contents-body")

        #Controllo che imp. WebDAV sia attivo e che impostazioni SSL sia "Solo SSL", altrimenti le modifico e confermo
        try:
            checkbox = driver.find_element(By.ID, "ID_AN_DSV_SVR_checked")
            if not checkbox.is_selected():
                fieldset = checkbox.find_element(By.XPATH, "../..")
                fieldset.click()
                wait_random_time()
                #Eventuale conferma configurazione con click su tasto ok
                wait.until(EC.element_to_be_clickable((By.ID, "ID_AN_DSV_SVR_checked"))).click()
                wait_random_time()
        except Exception as e:
            print(f"Errore durante gestione bottone server webdav: {e}")

        try:
            bottone_ssl = driver.find_element(By.ID, "c63631454411411684900998")
        #se il bottone non ha testo default Solo SSL glielo imposto
            if bottone_ssl.text != "Solo SSL":
                #Cerca e clicca bottone dropdown per scelta ssl
                wait.until(EC.element_to_be_clickable((By.ID, "c63631454411411684900998"))).click()
                wait_random_time()
                #Cerca e clicca scelta "Solo ssl"
                wait.until(EC.element_to_be_clickable((By.ID, "c63631454411411684901001"))).click()
                wait_random_time()
        except Exception as e:
            print(f"Errore durante gestione botto solo SSL: {e}")

        #Cerca e clicca il bottone ok per confermare
        wait.until(EC.element_to_be_clickable((By.ID, "ID_OK_AN_DSV_SVR"))).click()
        wait_random_time()
    except Exception as e:
        print(f"Eccezione catturata durante impostazione WebDAV: {e}")

def imp_open_api():
    try:
        #Switch frame default
        driver.switch_to.default_content()

        #Cerco e clicco il link per tornare indietro di un menù
        torna_indietro(wait)

        #Cerco e clicco il link per andare nel sottomenù Imp. OpenAPI
        wait.until(EC.element_to_be_clickable((By.ID, "ID_SubMenu_Network_OpenApiSetting"))).click()
        wait_random_time()
        wait.until(EC.element_to_be_clickable((By.ID, "ID_SpareSubMenu_Network_OpenApiSetting"))).click()
        wait_random_time()

        #Switch frame SPA-contents-body
        driver.switch_to.frame("SPA-contents-body")

        #Controllo che imp. SSL/Porta sia "Solo SSL", altrimenti le modifico
        bottone_ssl = driver.find_element(By.XPATH, "//fieldset[@id='ID_NETWORK_OVERSSL']//button")
        #se il bottone non ha testo default Solo SSL glielo imposto
        if bottone_ssl.text != "Solo SSL":
            wait.until(EC.element_to_be_clickable((bottone_ssl))).click()
            wait_random_time()
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-value='SslOnly']"))).click()
            wait_random_time()
        # Cerco e clicco disattivando i fieldset di impostazione livello verifica certificato
        # Cerca l'elemento della pagina scrollabile e lo fa scendere in basso per visualizzare tutte le checkbox
        scrollable_div = driver.find_element(By.ID, "SPA-contents-html")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        wait_random_time()

        # Cerco e clicco disattivando i fieldset di impostazione livello verifica certificato, se attivi
        checkbox_ids = ["ID_AN_IOP_CLD_checked", "ID_AN_IOP_EXD_checked", "ID_AN_IOP_CND_checked", "ID_AN_IOP_KYD_checked", "ID_AN_IOP_CHD_checked", "ID_AN_IOP_LCD_checked"]
        for checkbox_id in checkbox_ids:
            checkbox = driver.find_element(By.ID, checkbox_id)

            if checkbox.is_selected():
                fieldset = checkbox.find_element(By.XPATH, "../..")
                fieldset.click()
                wait_random_time()
        
        #Cerco e clicco il bottone ok per confermare
        wait.until(EC.element_to_be_clickable((By.ID, "ID_BTN_REGIST_NEXT"))).click()
        wait_random_time()
    except Exception as e:
        print(f"Eccezione catturata durante impostazione OpenAPI: {e}")

def logout_finally():
    time.sleep(5)
    print("vado al finally")
    #Switch frame default
    driver.switch_to.default_content()
    #Cerca e trova bottone Disconetti e clicca con js per essere sicuro di cliccarlo essendo che potrebbe essere mascherato
    disc = driver.find_element(By.XPATH, "//button[text()='Disconnetti']")
    driver.execute_script("arguments[0].click();", disc)
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Disconnetti']"))).click()
    time.sleep(5)
    #Conferma logout
    wait.until(EC.presence_of_element_located((By.ID, "ID_LOGOUT_BUTTON"))).click()
    time.sleep(5)
    driver.quit()

