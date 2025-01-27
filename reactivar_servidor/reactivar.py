
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from dotenv import load_dotenv
import os
import shutil


load_dotenv()

USER = os.getenv('USER_PYTHON')
PASS = os.getenv('PASS_PYTHON')



def reactivar():
    # Configurar el navegador Brave
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

    options = webdriver.ChromeOptions()
    options.binary_location = brave_path
    driver = webdriver.Chrome(options=options)

    url = "https://www.pythonanywhere.com/user/MasDas333/consoles/37718233/"

    # Navegar a la página de inicio de sesión de Airbnb
    driver.get(url)


    time.sleep(5)

    username_input = driver.find_element(By.ID, 'id_auth-username')

    username_input.send_keys(USER)

    password_input = driver.find_element(By.ID, 'id_auth-password')

    password_input.send_keys(PASS)

    time.sleep(3)

    #click login
    login_button = driver.find_element(By.ID, 'id_next')

    login_button.click()

    time.sleep(5)


if __name__ == "__main__":
    print("Iniciando Automatizacion")
    reactivar()