import pickle
from unidecode import unidecode
import re
import os

def salvar_pkl(objeto, path_completo):

    os.makedirs(os.path.dirname(path_completo), exist_ok=True)
    
    with open(path_completo, "wb") as f:
        pickle.dump(objeto, f)
    print(f"Arquivo salvo em: {path_completo}")

def ler_pkl(path_completo):

    with open(path_completo, "rb") as f:
        return pickle.load(f)


def normalize_name(text):
    new_text = text.replace("’", "'")
    new_text = re.sub(r"'[sS]\s*", " ", new_text)
    new_text = new_text.replace('&', '').replace('`', '').replace("'", "").replace("’", "").replace('-', '').replace(',','')
    new_text = new_text.replace('?','').replace('-', '').replace("-", "")
    new_text = re.sub(r"[-–—]", "", new_text)
    new_text = unidecode(re.sub(r'\s+', ' ', new_text).strip().upper().replace(" ", "_").replace(":", "_").lower())
    new_text = new_text.replace(".", "")
    return new_text
