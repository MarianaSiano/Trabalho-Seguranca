import requests
import urllib3
import json
import time
import subprocess

#--- Configurações de Ambiente (Valores Padrão do Free5GC v3.4.3) ---
#Os IPs de rede (172.16.0.x), mas para um único host, 127.0.0.1 é o padrão
NF_CONFIG = {
    "UDM_IP": "127.0.0.1",
    "UDM_PORT": 29503,
    "NEF_IP": "127.0.0.1",
    "NEF_PORT": 29509,
    "SUPI_1": "imsi-208930000000001"
}

#Desabilitar avisos de certificados autoassinados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#--- Teste de SQL Injection (Boolean-based blind) ---
