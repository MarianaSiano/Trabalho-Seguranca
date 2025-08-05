import requests
import urllib3
import json
import socket
import time

#--- Configurações de Ambiente (Valores Padrão do Free5GC v3.4.3) ---
NF_CONFIG = {
    "NRF_IP": "127.0.0.1",
    "NRF_PORT": 29510,
    "UDM_IP": "127.0.0.1",
    "UDM_PORT": 29503,
    "SUPI_2": "208930000000002"
}

UDM_API_URL_BASE = f"https://{NF_CONFIG['UDM_IP']}:{NF_CONFIG['UDM_PORT']}/nudm-uecm/v1/ues"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_access_token():
    """Tenta obter um token de acesso de uma NF."""
    auth_url = f"https://{NF_CONFIG['NRF_IP']}:{NF_CONFIG['NRF_PORT']}/nnrf-nfm/v1/oauth2/token"
    auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    auth_data = "grant_type=client_credentials&client_id=NSSF"
    try:
        response = requests.post(auth_url, headers=auth_headers, data=auth_data, verify=False, timeout=5)
        response.raise_for_status()
        return response.json().get("access_token")
    except (requests.exceptions.RequestException, KeyError) as e:
        return None

def test_network_slicing():
    print("=" * 50)
    print("A7 - Testando Falhas de Segmentação de Rede (Network Slicing)")
    print("=" * 50)

    #Exemplo com IPs diferentes, mas no mesmo host de loopback para simular slices.
    slice_a_ip = NF_CONFIG['NRF_IP']
    slice_b_ip = NF_CONFIG['UDM_IP']
    slice_b_port = NF_CONFIG['UDM_PORT']

    #Teste de conectividade a nível de rede (Socket)
    try:
        socket.create_connection((slice_b_ip, slice_b_port), timeout=3).close()
        print(f"[!!!] VULNERABILIDADE DETECTADA: Um host na Slice A pode se conectar à Slice B.")
    except (socket.timeout, socket.error):
        print("[+] Conexão TCP para a Slice B falhou. A segmentação de rede parece correta.")

    #Teste de bypass de autorização
    token = get_access_token()
    if not token:
        print("[-] Não foi possível obter o token para o teste de bypass")
        return
    headers = {"Authorization": f"Bearer {token}"}
    other_supi_url = f"{UDM_API_URL_BASE}/imsi-{NF_CONFIG['SUPI_2']}/authentications"
    
    try:
        response = requests.get(other_supi_url, headers=headers, verify=False, timeout=5)
        if response.status_code in [200, 201]:
            print("[!!!] VULNERABILIDADE DETECTADA: Bypass de autorização inter-slice!")
        elif response.status_code in [401, 403]:
            print("[+] Bypass de autorização falhou (acesso negado).")
        else:
            print(f"[-] Resposta inesperada. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Erro ao tentar acessar a API da Slice B: {e}")

if __name__ == "__main__":
    test_network_slicing()