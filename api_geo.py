import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

USER_AGENT = "tp1algoritmos_ufmg"
INPUT_CSV_PATH = "data/dados.csv"

try:
    geolocator = Nominatim(user_agent=USER_AGENT)
except Exception as e:
    print(f"Erro ao inicializar o geolocator Nominatim: {e}")
    print("Verifique sua conexão com a internet ou se há restrições de firewall.")
    exit()

def geocode_single_address(address_str, city_context="Belo Horizonte", state_context="MG"):
    """
    Tenta geocodificar um único endereço.
    Adiciona contexto de cidade/estado se não parecer estar presente.
    """
    full_address = address_str
    if city_context.lower() not in address_str.lower():
        full_address += f", {city_context}"
    if state_context.lower() not in address_str.lower() and state_context not in full_address: # Evitar duplicar MG se já tiver BH, MG
        full_address += f", {state_context}"

    print(f"Tentando geocodificar: \"{full_address}\"")
    try:
        # Timeout de 10 segundos para a requisição
        location = geolocator.geocode(full_address, timeout=10)
        if location:
            return location.latitude, location.longitude, location.address
        else:
            print(f"Endereço não encontrado por Nominatim: {full_address}")
            return None, None, None
    except GeocoderTimedOut:
        print(f"Timeout ao tentar geocodificar: {full_address}. O serviço pode estar ocupado.")
        return None, None, None
    except GeocoderUnavailable:
        print(f"Serviço de geocodificação indisponível: {full_address}. Tente novamente mais tarde.")
        return None, None, None
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a geocodificação de '{full_address}': {e}")
        return None, None, None

try:
    df = pd.read_csv(INPUT_CSV_PATH)
    print(f"Arquivo '{INPUT_CSV_PATH}' carregado com sucesso. {len(df)} linhas encontradas.")
except FileNotFoundError:
    print(f"Erro: Arquivo '{INPUT_CSV_PATH}' não encontrado. Verifique o caminho.")
    exit()
except pd.errors.EmptyDataError:
    print(f"Erro: Arquivo '{INPUT_CSV_PATH}' está vazio.")
    exit()
except Exception as e:
    print(f"Erro ao ler o arquivo CSV '{INPUT_CSV_PATH}': {e}")
    exit()

# --- Pegar um endereço de exemplo para testar ---
if not df.empty and 'ENDERECO_FORMATADO' in df.columns:
    # Pega o primeiro endereço da lista como exemplo
    endereco_exemplo = df['ENDERECO_FORMATADO'].iloc[13]
    print(f"\n--- Testando geocodificação para o endereço de exemplo ---")
    print(f"Endereço original do CSV: \"{endereco_exemplo}\"")

    latitude, longitude, EnderecoNominatim = geocode_single_address(endereco_exemplo)

    if latitude is not None and longitude is not None:
        print("\n--- Resultado da Geocodificação ---")
        print(f"Endereço Original: {endereco_exemplo}")
        print(f"Endereço Retornado pelo Nominatim: {EnderecoNominatim}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
    else:
        print(f"\nNão foi possível geocodificar o endereço de exemplo: \"{endereco_exemplo}\"")
else:
    if df.empty:
        print("O DataFrame está vazio. Não há endereços para testar.")
    else:
        print("Erro: A coluna 'ENDERECO_FORMATADO' não foi encontrada no CSV.")

print("\n--- Fim do teste de geocodificação para um endereço ---")