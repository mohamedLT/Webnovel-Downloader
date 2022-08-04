import os
import PySimpleGUI as sg
import cloudscraper
from bs4 import BeautifulSoup
from os import getcwd
from werkzeug.utils import secure_filename
from chapters2book import *



PATH_CONST = "https://www.lightnovelworld.com"



def get_one_chapter(path):
    scraper = cloudscraper.create_scraper(delay=10, browser='chrome') 
    response = scraper.get(path)
    page = BeautifulSoup(response.text , "html.parser")
    text = page.find_all(name="p")
    title = page.find(name="span",class_="chapter-title")
    title = secure_filename(title.get_text())
    with open(title+".text", "w", encoding="utf-8") as f:
        for p in text:
            f.write(" \n ")
            txt = p.get_text()
            if "lightnov" in txt:
                continue
            f.write(txt )
    return title



def get_novel(path:str,title_parm:str,folder:str):


    scraper = cloudscraper.create_scraper(delay=10, browser='chrome') 
    response = scraper.get(path)
    page = BeautifulSoup(response.text , "html.parser")
    
    title = page.find(name="h1",class_="novel-title text2row").get_text() \
        if title_parm.isspace() or len(title_parm)==0  \
        else title_parm
    title = secure_filename(title)
    
    
    dir = f"{getcwd()}\\{title}" if folder.isspace() or len(folder)==0 else folder
    if not os.path.exists(dir):
        os.mkdir(dir)
    os.chdir(dir)
    first = page.find(id="readchapterbtn")
    path= PATH_CONST+first["href"] if first else path 
    while True:    
        name = get_one_chapter(path)
        nxt_path = get_next_path(path)
        if nxt_path :
            yield name
            path=nxt_path
        else :
            yield False
            break
    create_book(title)
    

def get_next_path(path):
    scraper = cloudscraper.create_scraper(delay=10, browser='chrome') 
    response = scraper.get(path)
    page = BeautifulSoup(response.text , "html.parser")
    a = page.find(name="a",class_="button nextchap")
    if a :
        return PATH_CONST+a["href"]
    return None

