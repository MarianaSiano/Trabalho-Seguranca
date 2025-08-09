import requests
import socket
import ssl
import subprocess
import urllib3
import matplotlib.pyplot as plt
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NF_CONFIG = {
    "NRF_IP": "127.0.0.10",
    "NRF_PORT": 8000,
    "NRF_SCHEME": "http",
    "UDM_IP": "127.0.0.3",
    "UDM_PORT": 8000,
    "SUPI_2": "208930000000002"
}

# A02 - Criptografia
def test_cryptographic_failures():
    print("=" * 50)
    print("A2 - Testando Criptografia")
    print("=" * 50)

    http_insecure, tls_weak = 0, 0
    if NF_CONFIG["NRF_SCHEME"] == "http":
        print("[!!!] HTTP inseguro em uso.")
        http_insecure = 1
    return http_insecure, tls_weak

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
        print("[!!!] Conexão TCP entre slices permitida!")
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

#======== Ping ========
def test_ping_with_latency(target):
    print(f"==== PING para {target} ====")
    try:
        #Modo detalhado - mostra cada pacote
        result = subprocess.run(["ping", "-c", "4", "-v", target], capture_output=True, text=True)
        print(result.stdout)

        packet_loss_match = re.search(r"(\d+)% packet loss", result.stdout)
        packet_loss = int(packet_loss_match.group(1)) if packet_loss_match else 100

        latency_match = re.search(r"= [\d\.]+/[\d\.]+/([\d\.]+)/", result.stdout)
        avg_latency = float(latency_match.group(1)) if latency_match else None

        print(f"[INFO] Perda: {packet_loss}%  |  Latência média: {avg_latency} ms")
        return (1 if packet_loss > 0 else 0), avg_latency
    except Exception as e:
        print("Erro no ping:", e)
        return 1, None

#======== HPING3 ========
def test_hping3(target):
    print(f"==== HPING3 SYN scan em {target} ====")
    try:
        #Modo detalhado
        result = subprocess.run(["hping3", "-S", "-V", "-p", str(NF_CONFIG['NRF_PORT']), "-c", "5", target], capture_output=True, text=True)
        print(result.stdout)
        return 1
    except FileNotFoundError:
        print("hping3 não está instalado.")
    return 0

#======== IDS Simulação ========
def simulate_ids_traffic(target):
    print(f"==== Simulação IDS flood para {target} ====")
    try:
        subprocess.run(["hping3", "--flood", "-V", "-p", str(NF_CONFIG['NRF_PORT']), target], capture_output=True, text=True, timeout=5)
        print("[INFO] Flood enviado por 5 segundos.")
        return 1
    except Exception as e:
        print("Erro na simulação IDS:", e)
    return 0

#======== Gráfico ========
def gerar_grafico_linha(resultados):
    categorias = [
        "HTTP não seguro", "TLS fraco",
        "Login inválido", "Endpoint inválido",
        "Conexão inter-slice", "Bypass autorização",
    ]

    plt.plot(categorias, resultados, marker='o', linestyle='-', color='blue')
    plt.title("Exploração de Vulnerabilidades no free5GC")
    plt.ylabel("Ocorrências Detectadas")
    plt.xticks(rotation=30)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("grafico_vulnerabilidades.png")
    plt.show()

if __name__ == "__main__":
    r1, r2 = test_cryptographic_failures()
    r3, r4 = test_network_slicing()
    brute_force_result = 0  # Definido como 0 para manter a estrutura do gráfico
    lat_nrf = test_ping_with_latency(NF_CONFIG['NRF_IP'])
    lat_udm = test_ping_with_latency(NF_CONFIG['UDM_IP'])

    print(f"\n📊 Latência média NRF: {lat_nrf} ms")
    print(f"📊 Latência média UDM: {lat_udm} ms\n")

    resultados = [r1, r2, brute_force_result, 0, r3, r4]
    gerar_grafico_linha(resultados)