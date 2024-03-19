#pip install beautifulsoup4
#pip install requests
#ip install spotipy
#pip install lxml
#pip install openpyxl

import spotipy
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import glob
from spotipy.oauth2 import SpotifyClientCredentials
import json

# Cargamos los credenciales de la API
SPOTIPY_CLIENT_ID = "****"
SPOTIPY_CLIENT_SECRET = "*****"


# Generamos el autenticador
auth_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


rango = range(2000,2024, 1)
def extract_wiki(rango):
    for r in rango:
        try:
            resposta = requests.get(f'https://es.wikipedia.org/wiki/Festival_de_la_Canci%C3%B3n_de_Eurovisi%C3%B3n_{r}')
            codi_web = (resposta.text)

            soup = BeautifulSoup(codi_web, 'html.parser')
            final = soup.find('span', id="Final")
            tabla = final.find_next("table")
            df = pd.read_html(str(tabla))[0]

            print(df)
            df.to_excel(f"final-{r}.xlsx", index= False)
            print(f"TODO BIEN EN {r}")
            time.sleep(1)
        except AttributeError:
            print(f"Problema en {r}")

#extract_wiki(rango)
def juntar():
    files = glob.glob("*.xlsx")
    print(files)

    llista_dfs = []
    for f in files:
        print(f)
        df = pd.read_excel(f)
        any = f.split("-")[1].split(".")[0]
        df["año"] = any
        df.columns.values[2] = "cantante"
        df.columns.values[5] = "Puntos"
        df.columns.values[0] = "N."

        llista_dfs.append(df)

    final_df = pd.concat(llista_dfs)
    final_df.to_excel("final-final.xlsx", index =False)
    print(final_df)
# juntar()

df = pd.read_excel("final-final.xlsx")
print(df)


for index,row in df.iterrows():
    cantant = row["cantante"]
    song = row["Canción"]
    año = row["año"]
    q = f"{song}{cantant} Eurovisión"
    print(q)
    resposta = sp.search(q, limit=10, offset=0, type='track', market=None)
    resposta["query"] = q
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(resposta, f, ensure_ascii=False, indent=4)
    time.sleep(15)