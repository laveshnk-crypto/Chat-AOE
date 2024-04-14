# This code isnt really useful. Just something I was testing.

from bs4 import BeautifulSoup as bs
import requests
import os

def clean_main_civ_page():
    print("Processing...")
    page_to_scrape = requests.get("https://ageofempires.fandom.com/wiki/Civilization_(Age_of_Empires_II)")

    soup = bs(page_to_scrape.text, "html.parser")

    # Find the civs
    civs = soup.findAll("span", attrs={"class": "mw-headline"})
    # Civ information
    text_stuff = soup.findAll("li")

    bad_words = ["Unique unit", "Unique building", "Unique technologies", "Civilization bonuses", "Team bonus"]
    civList = []

    # Converting civs to a list
    for civ in civs:
        civText = civ.text.strip()
        if civText == "Vikings":
            civList.append(civText)
            break
        if civText != "Contents" and not any(bad_word in civText for bad_word in bad_words):
            civList.append(civText)

    directory = "textFiles"
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    # Write the info to a file
    with open(os.path.join(directory, "CivInfo.txt"), "w", encoding="utf-8") as file:
        # Initialize variables
        stop_word = "Focus"
        end_word = "↑ This means that:"
        civ_index = 0
        in_civ_section = False
        civCount = 1

        # Writing Civ Info to the file
        for texts in text_stuff:
            text = texts.text.strip()

            # Check if the current text contains the stop word
            if stop_word in text:
                in_civ_section = True
                file.write("\n" + civList[civCount-1] + ":\n")
                civCount += 1
                file.write(text + "\n")
                continue
            
            # Check if the current text contains the end word
            if end_word in text:
                in_civ_section = False
                civ_index += 1
                file.write("\n")
                continue

            # If in civ section, write the text to the file
            if in_civ_section:
                file.write(text + "\n")
    print("Complete!")

if __name__ == "__main__":
    clean_main_civ_page()
