import requests
import urllib3
import time

#--- Configurações de Ambiente (Valores Padrão do Free5GC) ---
NF_CONFIG = {
    "NRF_IP": "127.0.0.1",
    "NRF_PORT": 29510
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_logging():
    print("=" * 50)
    print("A8: Testando Monitoramento e Logging Insuficientes")
    print("=" * 50)
    
    nf_invalid_url = f"https://{NF_CONFIG['NRF_IP']}:{NF_CONFIG['NRF_PORT']}/api/invalid_endpoint"
    print("[*] Simulando eventos de segurança. Verifique os logs da NF agora!")
    
    try:
        #Simular tentativas de login falhas (exemplo conceitual)
        for _ in range(3):
            requests.post(f"https://{NF_CONFIG['NRF_IP']}:8000/auth/login", json={"user":"admin", "pass":"bad_pass"}, verify=False, timeout=2)
        
        #Simular acesso a endpoint inválido
        requests.get(nf_invalid_url, verify=False, timeout=2)
        
        #Simular negação de serviço leve
        for i in range(10):
            requests.post(nf_invalid_url, json={}, verify=False, timeout=0.1)
        
        print("[+] Simulação concluída. O resultado depende da sua análise manual dos logs.")
    except requests.exceptions.RequestException as e:
        print(f"[-] Erro durante a simulação de eventos: {e}")

if __name__ == "__main__":
    test_logging()