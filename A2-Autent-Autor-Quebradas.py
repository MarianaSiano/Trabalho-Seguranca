import requests
import urllib3
import json

#--- Configurações de Ambiente
#Usando IPs de loopback específicos da sua configuração para testes internos
NF_CONFIG ={
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
    """Tenta obter um token de acesso de uma NF, conforme fluxo OAuth2 no 5G Core."""
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

def test_bola():
    print("=" * 50)
    print("A2 - Testando Auteticação e Autorização Quebradas (BOLA)")
    print("=" * 50)

    token = get_access_token()
    if not token:
        print("[-] Não foi possível obter o token, o teste não pode continuar")
        return

        headers = {"Authorization": f"Bearer {token}"}
        other_supi = NF_CONFIG['SUPI_2']

        try:
            response_other = requests.get(f"{UDM_API_URL_BASE}/imsi-{other_supi}/authentications", headers=headers, timeout=5)
        
            if response_other.status_code in [200, 201]:
                print("[!!!] VULNERABILIDADE DETECTADA: Broken Object Level Authorization!")
                print("      O token acessa dados de outro SUPI.")
            elif response_other.status_code in [401, 403]:
                print("[+] Acesso negado. A API está protegida corretamente")
            else:
                print(f"[-] Erro inesperado na requisição maliciosa. Status: {response_other.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[-] Erro ao se conectar à API para o teste: {e}")

if __name__ == "__main__":
    test_bola()