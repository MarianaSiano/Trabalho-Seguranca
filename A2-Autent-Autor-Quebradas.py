import requests
import urllib3
import json

#--- Configurações de Ambiente (Valores do seu nrfcfg.yaml e udmcfg.yaml) ---
NF_CONFIG = {
    "NRF_IP": "127.0.0.10",
    "NRF_PORT": 8000,
    "UDM_IP": "127.0.0.3",
    "UDM_PORT": 8000,
    "SUPI_1": "208930000000001",
    "SUPI_2": "208930000000002"
}

UDM_API_URL_BASE = f"http://{NF_CONFIG['UDM_IP']}:{NF_CONFIG['UDM_PORT']}/nudm-uecm/v1/ues"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)