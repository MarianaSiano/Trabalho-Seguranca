import requests
import urllib3
import time

#--- Configurações de Ambiente (Valores do nrfcfg.yaml)
NF_CONFIG = {
    "NEF_IP": "127.0.0.10",
    "NEF_PORT": 8000
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_logging():
    print("=" * 50)
    print("A8 - Testando o Monitoramento e Logging Insuficientes")
    print("=" * 50)

    nf_invalid_url = f"http://{NF_CONFIG['NRF_IP']}:{NF_CONFIG['NRF_PORT']}/api/invalid_endpoint"
    print("[*] Simulando eventos de segurança. Verifique os logs da NF agora!")
    
    try:
        for _ in range(3):
            requests.post(f"http://{NF_CONFIG['NRF_IP']}:8000/auth/login", json={"user":"admin", "pass":"bad_pass"}, timeout=2)
        
        requests.get(nf_invalid_url, timeout=2)
        
        for i in range(10):
            requests.post(nf_invalid_url, json={}, timeout=0.1)
        
        print("[+] Simulação concluída. O resultado depende da sua análise manual dos logs.")
    except requests.exceptions.RequestException as e:
        print(f"[-] Erro durante a simulação de eventos: {e}")

if __name__ == "__main__":
    test_logging()