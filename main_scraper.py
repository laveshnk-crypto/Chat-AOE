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
        
        # Quite annoying that fandom has two different formats for some of the civs. This should solve that problem though
        url1 = "https://ageofempires.fandom.com/wiki/" + civ + "_(Age_of_Empires_II)"
        url2 = "https://ageofempires.fandom.com/wiki/" + civ

        try:
            sendRequest = requests.get(url1)
            sendRequest.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
            civ_url = url1
        except requests.HTTPError:
            try:
                sendRequest = requests.get(url2)
                sendRequest.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
                civ_url = url2
            except requests.HTTPError:
                print(f"Both URLs for {civ} returned a 404 error. Skipping...")
                continue  # Skip to the next civilization
            
        pages_to_scrape.append(civ_url)
        
        
        urls = [
            civ_url
        ]
        # langchain document loader
        loader = SeleniumURLLoader(urls=urls)
        data = loader.load()
        
        print(data)
        directory = "./textFiles"
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        filename = civ + ".txt"
        with open(os.path.join(directory, filename ), "w", encoding="utf-8") as file:
            for doc in data:
                file.write(doc.page_content + "\n")
        
        print(civ_url)
        print(sendRequest)
        
        
def cleaning_data():
    # Add premise to each file
    directory = "./textFiles"
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r+", encoding="utf-8") as file:
                content = file.read()
                file.seek(0, 0)
                file.write(f"This page is all about the {filename[:-4]}\n\n{content}")

if __name__ == "__main__":
    # main_scraper()
    cleaning_data()
    
