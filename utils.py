import os
import re
from pyrogram import Client
from colorama import Fore
import pyfiglet
import random

""" Global """
session_name = "user"

def limpar_nome_arquivo(nome_arquivo):
    nome_limpo = re.sub(r'[^a-zA-Z0-9]', '_', nome_arquivo)
    chars_invalidos = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in chars_invalidos:
        nome_limpo = nome_limpo.replace(char, '_')
    return nome_limpo

class Banner:
    def __init__(self, banner):
        self.banner = banner
        self.lg = Fore.LIGHTGREEN_EX
        self.w = Fore.WHITE
        self.cy = Fore.CYAN
        self.ye = Fore.YELLOW
        self.r = Fore.RED
        self.n = Fore.RESET

    def print_banner(self):
        colors = [self.lg, self.r, self.w, self.cy, self.ye]
        f = pyfiglet.Figlet(font='slant')
        banner = f.renderText(self.banner)
        print(f'{random.choice(colors)}{banner}{self.n}')
        print(f'{self.r}  Version: v0.0.2 https://github.com/viniped \n{self.n}')

def show_banner():
    banner = Banner('TG - Mirror')
    banner.print_banner()

def cache_path():
    directories = ['downloads', 'download_tasks','forward_task','chat_download_task']

    for dir_name in directories:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

def authenticate():
    # Get credentialas from user
    def get_credentials():
        api_id = input("Digite seu API ID: ")
        api_hash = input("Digite seu API Hash: ")
        return api_id, api_hash

    # if session file does not exists, obtain the credentials 
    if not os.path.exists(f"{session_name}.session"):
        api_id, api_hash = get_credentials()
        with Client(session_name, api_id, api_hash) as app:
            print("Você está autenticado!")
    else:
        print("Usando sessão existente.")

def rename_files(directory, chat_title):
    
    chat_directory = os.path.join(directory, limpar_nome_arquivo(chat_title))
    files = [f for f in os.listdir(chat_directory) if os.path.isfile(os.path.join(chat_directory, f))]      
    files.sort(key=lambda x: os.path.getctime(os.path.join(chat_directory, x)))    
    for idx, filename in enumerate(files, start=1):
        # Substituir underscores por espaços
        cleaned_name = filename.replace("_", " ")
        new_name = f"{idx:03}_{cleaned_name}"
        os.rename(os.path.join(chat_directory, filename), os.path.join(chat_directory, new_name))
