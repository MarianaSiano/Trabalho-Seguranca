import ssl
import socket
import requests
import urllib3

#--- Configurações de Ambiente (Valores do nrfcfg.yaml)
NF_CONFIG = {
    "NRF_IP": "127.0.0.10",
    "NRF_PORT": 8000
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)