import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

USER_AGENT = "tp1algoritmos_ufmg"

try:
    geolocator = Nominatim(user_agent=USER_AGENT)
except Exception as e:
    print(f"Erro ao inicializar o geolocator Nominatim: {e}")
    print("Verifique sua conexão com a internet ou se há restrições de firewall.")
    exit()

def geocode_single_address(address_str, city_context="BELO HORIZONTE", state_context="MG"):

    full_address = address_str
    if city_context.lower() not in address_str.lower():
        full_address += f", {city_context}"
    if state_context.lower() not in address_str.lower() and state_context not in full_address: 
        full_address += f", {state_context}"

    try:
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