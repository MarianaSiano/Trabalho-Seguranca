import requests
import urllib3
import time

#--- Configurações de Ambiente ---
NF_CONFIG = {
    "NRF_IP": "127.0.0.10",
    "NRF_PORT": 8000
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_logging():
    print("=" * 50)
    print("A9 - Testando Insufficient Monitoring and Logging")
    print("=" * 50)

    print("[*] Referência: O PDF sobre IDS/IPS explica que um IDS analisa logs para buscar falhas e indicar invasões.")
    
    nf_invalid_url = f"http://{NF_CONFIG['NRF_IP']}:{NF_CONFIG['NRF_PORT']}/api/invalid_endpoint"
    print("[*] Simulando eventos de segurança. Verifique os logs da NF agora!")
    
    try:
        #Simular tentativas de login falhas
        for _ in range(3):
            requests.post(f"http://{NF_CONFIG['NRF_IP']}:8000/auth/login", json={"user":"admin", "pass":"bad_pass"}, timeout=2)
        
        #Simular acesso a endpoint inválido
        requests.get(nf_invalid_url, timeout=2)

        #Simular Negação de Serviço leve
        for i in range(10):
            requests.post(nf_invalid_url, json={}, timeout=0.1)

        print("[+] Simulação concluída. O resultado depende da sua análise manual dos logs.")
        print("[*] Para um resultado positivo, os logs devem ter registrado todos os eventos simulados.")
    except requests.exceptions.RequestException as e:
        print(f"[-] Erro durante a simulação de eventos: {e}")

if __name__ == "__main__":
    test_logging()