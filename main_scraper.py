from bs4 import BeautifulSoup as bs
import requests
import os
from langchain_community.document_loaders.url_selenium import SeleniumURLLoader

def list_of_civs():
    civ_retriever = requests.get("https://ageofempires.fandom.com/wiki/Civilization_(Age_of_Empires_II)")
    soup = bs(civ_retriever.text, "html.parser")
    # Find the civs
    civs = soup.findAll("span", attrs={"class": "mw-headline"})
    bad_words = ["Unique unit", "Unique building", "Unique technologies", "Civilization bonuses", "Team bonus"]
    civList = []
    # Converting civs to a list
    for civ in civs:
        civText = civ.text.strip()
        if civText == "Vikings":
            civList.append(civText)
            print(civText)
            break
        if civText != "Contents" and not any(bad_word in civText for bad_word in bad_words):
            civList.append(civText)
            print(civText)    

    return civList

def main_scraper():
    
    civList = list_of_civs()
    pages_to_scrape = []   
    
    for civ in civList:
        
        if civ == "Aztecs":
            civ_url = "https://ageofempires.fandom.com/wiki/" + civ
            pages_to_scrape.append(civ_url)
            sendRequest = requests.get(civ_url)
            
            # langchain document loader
            
            print(civ_url)
            print(sendRequest)

    
    
if __name__ == ("__main__"):
    main_scraper()