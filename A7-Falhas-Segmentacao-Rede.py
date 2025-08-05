import requests
import urllib3
import json
import socket
import time

#--- Configurações de Ambiente (Valores Padrão do Free5GC v3.4.3) ---
NF_CONFIG = {
    "NRF_IP": "127.0.0.1",
    "NRF_PORT": 29510,
    "UDM_IP": "127.0.0.1",
    "UDM_PORT": 29503,
    "SUPI_2": "208930000000002"
}

UDM_API_URL_BASE = f"https://{NF_CONFIG['UDM_IP']}:{NF_CONFIG['UDM_PORT']}/nudm-uecm/v1/ues"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_access_token():
    """Tenta obter um token de acesso de uma NF."""
    auth_url = f"https://{NF_CONFIG['NRF_IP']}:{NF_CONFIG['NRF_PORT']}/nnrf-nfm/v1/oauth2/token"
    auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    auth_data = "grant_type=client_credentials&client_id=NSSF"
    try:
        response = requests.post(auth_url, headers=auth_headers, data=auth_data, verify=False, timeout=5)
        response.raise_for_status()
        return response.json().get("access_token")
    except (requests.exceptions.RequestException, KeyError) as e:
        return None