import os
import time
import zipfile
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração dinâmica do geckodriver (dentro da pasta 'config')
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
geckodriver = os.path.join(diretorio_atual, "config", "geckodriver.exe")

# Cria a pasta 'data/csv' se não existir
if not os.path.exists("data/csv"):
    os.makedirs("data/csv")

def is_download_complete(download_dir):
    files_in_directory = os.listdir(download_dir)
    files_in_directory = [f for f in files_in_directory if f.endswith(".csv") or f.endswith(".zip")]
    return len(files_in_directory) > 0 and all(os.path.getsize(os.path.join(download_dir, f)) > 0 for f in files_in_directory)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_path) 

def wait_for_download(download_dir, prev_files_count):
    while True:
        time.sleep(1)
        files_in_directory = os.listdir(download_dir)
        files_in_directory = [f for f in files_in_directory if f.endswith(".csv") or f.endswith(".zip")]
        if len(files_in_directory) > prev_files_count: 
            return files_in_directory  
        if all(os.path.getsize(os.path.join(download_dir, f)) > 0 for f in files_in_directory):
            return files_in_directory 

options = Options()
options.headless = False
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", os.path.abspath("data/csv"))
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv,application/zip")

# Usa o caminho relativo ao invés do absoluto
service = Service(geckodriver)
driver = webdriver.Firefox(service=service, options=options)

URL = "https://dados.gov.br/dados/conjuntos-dados/serie-historica-de-precos-de-combustiveis-e-de-glp"
driver.get(URL)

wait = WebDriverWait(driver, 30)

try:
    btn_collapse = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'botao-collapse-Recursos')))
    btn_collapse.click()
except Exception as e:
    pass

tipoCombustivel = ["Álcool", "Diesel", "Combustíveis Automotivos"]

try:
    titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//h4')))
    anos_desejados = [str(ano) for ano in range(2020, 2026)]

    for title in titles:
        titulo_texto = title.text

        if any(palavra in titulo_texto for palavra in tipoCombustivel) and any(ano in titulo_texto for ano in anos_desejados):
            try:
                btn_download_xpath = f"//h4[text()='{titulo_texto.strip()}']/following-sibling::div//button[@id='btnDownloadUrl']"
                btn_download = wait.until(EC.element_to_be_clickable((By.XPATH, btn_download_xpath)))
                btn_download.click()

                prev_files_count = len(os.listdir("data/csv"))

                files = wait_for_download("data/csv", prev_files_count)

                for file_name in files:
                    file_path = os.path.join("data/csv", file_name)
                    if file_name.endswith(".zip"):
                        extract_zip(file_path, "data/csv")

            except Exception as e:
                continue

except Exception as e:
    pass

driver.quit()