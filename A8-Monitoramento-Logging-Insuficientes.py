import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Configurações do teste
NF_LOGIN_URL = "https://127.0.0.1:8000/auth/login"
NF_PROTECTED_URL = "https://127.0.0.1:29510/api/secure_resource"
NF_INVALID_URL = "https://127.0.0.1:29510/api/invalid_endpoit"

print("[+] Simulando eventos de segurança para teste de logging...")

#Teste 1: Simular tentativas de login falhas
for i in range(3):
    payload = {"username": "admin", "password": f"wrong_password_{i}"}
    print(f"[*] Tentativa de login falha #{i+1}...")
    try:
        requests.post(NF_LOGIN_URL, json=payload, verify=False, timeout=2)
    except requests.exceptions.RequestException:
        pass

#Teste 2: Simular acesso com token inválido
print("[*] Simular acesso a recurso protegido com token inválido...")
invalid_token_headers = {"Authorization": "Bearer INVALID_TOKEN"}
try:
    requests.get(NF_PROTECTED_URL, headers=invalid_token_headers, verify=False, timeout=2)
except requests.exceptions.RequestException:
    pass

#Teste 3: Simular requisições malformadas ou para endpoints inválidos
print("[*] Simular requisições para endpoit inválido...")
try:
    requests.post(NF_INVALID_URL, json={}, verify=False, timeout=2)
except requests.exceptions.RequestException:
    pass

print("=" * 50)
print("[+] Simulação de ataques concluída. Verifica os logs da NF agora!")