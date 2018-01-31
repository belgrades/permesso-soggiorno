import requests
import json
from bs4 import BeautifulSoup


def get_permesso_data(password, lang='italian'):
    url = "http://questure.poliziadistato.it/servizio/stranieri?lang={language}&pratica={password}&invia=Invia&mime=4".format(password=password,
                                                                                                                              language=lang)
    r = requests.get(url)

    # Creating the soup object from Beautiful Soup
    soup = BeautifulSoup(r.content, 'html.parser')
    
    
    for titles in soup.find_all('title'):
        if "Permesso" not in titles:
            title = titles.text
            
    date = soup.find('pubdate').text
    
    for description in soup.find_all('description'):
        if "Polizia" not in description:
            status = description.text.strip()
    
    return title, date, status


def get_credentials():
    try:
        with open('credentials.json') as json_data:
            d = json.load(json_data)
            title, date, status = get_permesso_data(d["password"], d["language"])
            print(title)
            print(date)
            print("Status: ", status)
    except FileNotFoundError:
        print("First time!")
        print("Select Language | Escoge idioma | Selezione Lingua")
        
        print("[1] Italian")
        print("[2] Español")
        print("[3] English")
        
        lang = input()
        
        if all(map(lambda x: lang is not x, ["1", "2", "3"])):
            print("Invalid option! Bye!")
            raise SystemExit(0)
        
        if lang == "1":
            print("Inserisce il password dal scontrino della Poste Italiane")
        elif lang == "2":
            print("Ingrese el password que está en el recibo del Poste Italiane")
        else:
            print("Enter your password that's in the Poste Italiane receipt")

        password = input()
        title, date, status = get_permesso_data(password=password)
        
        if status == "Il documento di soggiorno non &egrave; presente in archivio.":
	        if lang == "1":
	            print("Password non valido! Ciao!")
	        elif lang == "2":
	            print("Password no valido! Adios!")
	        else:
	        	print("Password not valid! Bye!")	
        else:
            print(title)
            print(date)
            print("Status: ", status)

            if lang == "1":
                language = "italiano"
            elif lang == "2":
                language = "espanol"
            else:
	            language = "english"

            data = {'password': password,
                    'language': language}
            with open('credentials.json', 'w') as json_data:
                json.dump(data, json_data, indent=4)


if __name__ == "__main__":
	get_credentials()