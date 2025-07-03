import random
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def wait_random_time(min_sec=1, max_sec=1):
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)

def torna_indietro(wait):
    # Cerca il link per tornare alla schermata precedente e lo clicca
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='fixed-menu-nav']//a"))).click() 
    wait_random_time()