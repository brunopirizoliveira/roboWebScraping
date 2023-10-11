from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config
from datetime import datetime

import time
import re
import chromedriver_autoinstaller
import pandas as pd
import numpy as np
import os
import glob

def renameFile(filial):
    # data_formated = data.replace("/", "-").replace(":", "-").replace(" ", "_")
    downloads_dir = os.path.expanduser("~") + "/Downloads"
    # Lista todos os arquivos na pasta de Downloads por data de modificação
    files = glob.glob(os.path.join(downloads_dir, "*"))
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    if len(files) > 0:
        # Pega o caminho do último arquivo baixado
        last_downloaded_file = files[0]

        if last_downloaded_file.lower().endswith('.sswweb'):
                
            # Pode renomear o arquivo para o novo nome desejado
            novo_nome = f'{filial}.sswweb'

            # Renomeia o arquivo
            novo_caminho = os.path.join(downloads_dir, novo_nome)
            os.rename(last_downloaded_file, novo_caminho)

            print(f"O último arquivo baixado foi renomeado para: {novo_nome}")
    else:
        print("A pasta de Downloads está vazia.")

def waitToDownload(data_hora_inicial) :

    urlReports = config("URL_REPORTS")
    driver.get(urlReports)
    pageReports = driver.page_source
    soup = BeautifulSoup(pageReports, 'html.parser')


    # Encontre a tabela
    table = soup.find('table')
    time.sleep(2)

    rows = table.find_all('tr')

    # Itere a partir da segunda linha em diante (começando do índice 1)
    for row in rows[1:]:
    # Dentro de cada linha, itere sobre todas as células <td>
    # cell_count = 0

        usuario = row.find_all('td')[3]
        seq = row.find_all('td')[0]
        filialText = row.find_all('td')[4]
        status = row.find_all('td')[6]


        # Converta a string em um objeto datetime        
        dataReport = row.find_all('td')[2]
        # dataReport = "10/10/23 15:17:48"
        data_hora_formatada = datetime.strptime(dataReport.text, "%d/%m/%y %H:%M:%S")
        

        print(data_hora_formatada)
        print(data_hora_inicial)
        # Compare as datas/horas
        if data_hora_formatada > data_hora_inicial:

            if (usuario.text == "corelog") :

                if( status.text == "Concluído" and filialText.text == filial) :
                    print(usuario.text)
                    print(status.text)
                    print(seq.text)

                    # print("Tentativa download")
                    tdHref = row.find_all('td')[8]
                    # print(tdHref)
                    div = tdHref.find_all('div')[0]
                    # print(div)
                    a = div.find('a')   
                    onclick_value = a.get('onclick')
                    match = re.search(r"ajaxEnvia\('([^']*)'\)", onclick_value)     

                    value_inside_ajaxEnvia = match.group(1)  # Substitua pelo valor obtido a partir do match.group(1)

                    # Construa a expressão XPath usando aspas duplas para a string completa e aspas simples para o valor
                    # xpath_expression = f'//a[contains("{value_inside_ajaxEnvia}")]'
                    xpath_expression = f'//*[contains(@onclick, "{value_inside_ajaxEnvia}")]'


                    # Encontre o elemento usando a expressão XPath construída
                    element = driver.find_element(By.XPATH, xpath_expression)
                    element.click()
                    time.sleep(5)
                    renameFile(filial)
                    
                else :
                    print(seq.text)
                    print(usuario.text)
                    print(status.text)
                    print(filialText)
                    time.sleep(10)
                    driver.find_element(By.ID, "2").click()


                    waitToDownload(data_hora_inicial)
        else :
            exit()

data_hora_inicial = datetime.now()

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
unidadeInput = driver.find_element(By.ID, "2")
unidadeInput.send_keys(Keys.BACKSPACE)
unidadeInput.send_keys(Keys.BACKSPACE)
unidadeInput.send_keys(Keys.BACKSPACE)
time.sleep(2)
unidadeInput.send_keys(filial)
time.sleep(2)

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

# print(tableReports)

# Inicialize uma variável para contar as células
# Obtenha a data e hora atual

waitToDownload(data_hora_inicial)
#Configuracao Excel
# configExcel = driver.find_element(By.ID, "36")
# configExcel.click()
# time.sleep(50)
# print(driver.page_source.encode('utf-8'))



# # print(bs.prettify())
# print(cpfInput)
# print(userInput)
# print(passInput)
