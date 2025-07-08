import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options

load_dotenv()

#Classe per gestire tutte le configurazioni dell'applicazione
class Config:
    
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

    #Timeout attese
    DEFAULT_TIMEOUT = 10
    SHORT_TIMEOUT = 2
    LONG_TIMEOUT = 30

    #Configurazioni certificato
    CERT_VALIDITY_DAYS = os.getenv('CERT_VALIDITY_DAYS')
    CERT_KEY_TYPE = os.getenv('CERT_KEY_TYPE')

    #Opzioni di Chrome
    CHROME_OPTIONS = [
        "--incognito",
        "--ignore-certificate-errors",
        "--ignore-ssl-errors",
        "--ignore-certificate-errors-spki-list",
        "--allow-running-insecure-content",
        "--disable-web-security",
        "--accept-insecure-certs",
        "--disable-features=VizDisplayCompositor",
        "--test-type",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]

    # Preferenze Chrome
    CHROME_PREFS = {
        "directory_upgrade": True,
        "profile.default_content_settings.popups": 0,
        "plugins.always_open_pdf_externally": True,
        "profile.default_content_setting_values.automatic_downloads": 1,
        "safebrowsing.enabled": True
    }
    
    # Opzioni sperimentali Chrome
    CHROME_EXPERIMENTAL_OPTIONS = {
        'useAutomationExtension': False,
        "excludeSwitches": ["enable-automation"],
        "prefs": CHROME_PREFS
    }

    #Metodo di utilità
    @classmethod
    def get_chrome_options(cls):
        #Restituisce le opzioni Chrome configurate
        
        options = Options()

        #Aggiunge tutte le opzioni
        for option in cls.CHROME_OPTIONS:
            options.add_argument(option)

        #Aggiunge opzioni sperimentali
        for key, value in cls.CHROME_EXPERIMENTAL_OPTIONS.items():
            options.add_experimental_option(key, value)

        return options