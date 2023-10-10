from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config

import time
import re
import chromedriver_autoinstaller
import pandas as pd
import numpy as np


def waitToDownload(table) :
    time.sleep(2)

    rows = table.find_all('tr')

    # Itere a partir da segunda linha em diante (começando do índice 1)
    for row in rows[1:]:
    # Dentro de cada linha, itere sobre todas as células <td>
    # cell_count = 0
        usuario = row.find_all('td')[3]
        seq = row.find_all('td')[0]
        filial = row.find_all('td')[4]
        status = row.find_all('td')[6]
        if( status == "Concluído" and usuario == "corelog" and filial == filial) :
            print(usuario.text)
            print(status.text)
            print(seq.text)

            print("Tentativa download")
            tdHref = row.find_all('td')[8]
            link = tdHref.find("a")
            link.click()
            
        # for cell in row.find_all('td')[3]:
            # print(cell.text)
            # Acesse o conteúdo de cada célula
            # if cell_count == 3:  # Lembrando que a indexação começa em 0
                # Acesse o conteúdo do quarto <td>
                # print(cell.text)
            # cell_count += 1
        else :
            print(seq.text)
            print(usuario.text)
            print(status.text)
            print(filial)
            time.sleep(30)
            driver.find_element(By.ID, "2").click()
            waitToDownload(table)

domain = config('DOMAIN')
cpf = config('CPF')
user = config('USER')
passw = config('PASSW')
url = config('URL')


chrome_options = Options()
chrome_options.add_argument("--headless") 
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(0.5)

domainInput = driver.find_element(By.ID, "1")
cpfInput = driver.find_element(By.ID, "2")
userInput = driver.find_element(By.ID, "3")
passInput = driver.find_element(By.ID, "4")


domainInput.send_keys(domain)
cpfInput.send_keys(cpf)
userInput.send_keys(user)
passInput.send_keys(passw)

submit_button = driver.find_element(By.ID, "5")
submit_button.click()

# html = urlopen(url)
# bs = BeautifulSoup(html, 'html.parser')

# domainInput = bs.find('input', {'id':'1'})
# cpfInput    = bs.find('input', {'id':'2'})
# userInput   = bs.find('input', {'id':'3'})
# passInput   = bs.find('input', {'id':'4'})
time.sleep(2)

# Aqui estou selecionando a filial
filial='LAJ'
filialInput = driver.find_element(By.NAME, "f2")
filialInput.send_keys(Keys.BACKSPACE)
filialInput.send_keys(Keys.BACKSPACE)
filialInput.send_keys(Keys.BACKSPACE)
filialInput.send_keys(Keys.BACKSPACE)
time.sleep(2)
filialInput.send_keys(filial)
time.sleep(2)

# Aqui estou selecionando o menu na opcao
opcao=455
opcaoInput = driver.find_element(By.NAME, "f3")
opcaoInput.send_keys(455)
opcaoInput.send_keys(Keys.ENTER)


# Aqui ja estou na pagina de menus
urlMenu = config('URL_MENU')
driver.get(urlMenu)

time.sleep(5)
# print(driver.page_source.encode('utf-8'))

#id 35 = E
#id 37 = H
#ID 11 = 011023
dtIniInput = driver.find_element(By.ID, "11")
dtIniInput.clear()
time.sleep(2)
dtIniInput.send_keys("011023")

arquivoInput = driver.find_element(By.ID, "35")
arquivoInput.clear()
time.sleep(2)
arquivoInput.send_keys("E")

complInput = driver.find_element(By.ID, "37")
complInput.clear()
time.sleep(2)
complInput.send_keys(Keys.BACKSPACE)
time.sleep(2)
complInput.send_keys("H")

submit_menu_button = driver.find_element(By.ID, "40")
time.sleep(2)
submit_menu_button.click()

time.sleep(5)

# Aqui ja estou na pagina de relatorios
urlReports = config("URL_REPORTS")
driver.get(urlReports)
pageReports = driver.page_source
soup = BeautifulSoup(pageReports, 'html.parser')


# Encontre a tabela
table = soup.find('table')
# print(tableReports)

# Inicialize uma variável para contar as células

waitToDownload(table)
#Configuracao Excel
# configExcel = driver.find_element(By.ID, "36")
# configExcel.click()
# time.sleep(50)
# print(driver.page_source.encode('utf-8'))



# # print(bs.prettify())
# print(cpfInput)
# print(userInput)
# print(passInput)
