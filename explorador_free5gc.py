import requests
import socket
import ssl
import subprocess
import urllib3
import matplotlib.pyplot as plt

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NF_CONFIG = {
    "NRF_IP": "127.0.0.10",
    "NRF_PORT": 8000,
    "NRF_SCHEME": "http",
    "UDM_IP": "127.0.0.3",
    "UDM_PORT": 8000,
    "SUPI_2": "208930000000002"
}

#A2 - Cryptographic Failures
def test_cryptographic_failures():
    print("=" * 50)
    print("A2 - Testando Cryptografic Failures")
    print("=" * 50)

    http_insecure, tls_weak = 0, 0
    if NF_CONFIG["NRF_SCHEME"] == "http":
        print("[!!!] HTTP inseguro em uso.")
        http_insecure = 1
    return http_insecure, tls_weak

#A9 - Logging
def test_logging():
    print("=" * 50)
    print("A9 - Testando Logs")
    print("=" * 50)

    login_fails, endpoint_invalid = 0, 0
    try:
        for _ in range(3):
            requests.post(f"http://{NF_CONFIG['NRF_IP']}:{NF_CONFIG['NRF_PORT']}/auth/login", json={"user": "admin", "pass": "bad"}, timeout=2)
            login_fails += 1
        for _ in range(10):
            requests.post(f"http://{NF_CONFIG['NRF_IP']}:{NF_CONFIG['NRF_PORT']}/api/invalid_endpoint", json={}, timeout=1)
            endpoint_invalid += 1
    except Exception as e:
        print("Erro: ", e)
    return login_fails, endpoint_invalid

#Segmentação
def get_access_token():
    try:
        r = requests.post(f"http://{NF_CONFIG['NRF_IP']}:{NF_CONFIG['NRF_PORT']}/nnrf-nfm/v1/oauth2/token", headers={"Content-Type": "application/x-www-form-urlencoded"}, data="grant_type=client_credentials&client_id=NSSF", timeout=5)
        return r.json().get("access_token")
    except:
        return None

def test_network_slicing():
    print("=" * 50)
    print("Segmentação de Rede")
    print("=" * 50)

    interslice_tcp, bypass_auth = 0, 0
    try:
        socket.create_connection((NF_CONFIG['UDM_IP'], NF_CONFIG['UDM_PORT']), timeout=3).close()
        interslice_tcp = 1
    except:
        pass

    token = get_access_token()
    if token:
        r = requests.get(
            f"http://{NF_CONFIG['UDM_IP']}:{NF_CONFIG['UDM_PORT']}/nudm-uecm/v1/ues/imsi-{NF_CONFIG['SUPI_2']}/authentications",
            headers={"Authorization": f"Bearer {token}"}, timeout=5)
        if r.status_code in [200, 201]:
            bypass_auth = 1
    return interslice_tcp, bypass_auth

# ========== PING ==========
def test_ping(target):
    print(f"==== PING para {target} ====")

    try:
        result = subprocess.run(["ping", "-c", "4", target], capture_output=True, text=True)
        print(result.stdout)
        if "0% packet loss" not in result.stdout:
            return 1  #Perda detectada
    except Exception as e:
        print("Erro no ping:", e)
    return 0

#========== HPING3 ==========
def test_hping3(target):
    print(f"==== HPING3 SYN scan em {target} ====")
    try:
        result = subprocess.run(["hping3", "-S", "-p", str(NF_CONFIG['NRF_PORT']), "-c", "5", target],
                                capture_output=True, text=True)
        print(result.stdout)
        return 1  #Se executou, consideramos evento detectável
    except FileNotFoundError:
        print("hping3 não está instalado.")
    return 0

#========== IDS SIMULAÇÃO ==========
def simulate_ids_traffic(target):
    print(f"==== Simulação de tráfego suspeito para IDS ({target}) ====")
    try:
        subprocess.run(["hping3", "--flood", "-p", str(NF_CONFIG['NRF_PORT']), target], capture_output=True, text=True, timeout=5)
        return 1
    except Exception as e:
        print("Erro na simulação IDS:", e)
    return 0