import ssl
import socket
import requests
import urllib3

#--- Configurações de Ambiente ---
#A configuração atual usa HTTP. O teste assumiria HTTPS
NF_CONFIG = {
    "NRF_IP": "127.0.0.10",
    "NRF_PORT": 8000,
    "NRF_SCHEME": "http" #Informação da configuração atual
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_tls_weakness():
    print("=" * 50)
    print("A4 - Testando Falhas na Criptografia e Proteção de Dados (TLS)")
    print("=" * 50)

    if NF_CONFIG["NRF_SCHEME"] == "http":
        print("[!] Sua configuração do NRF usa HTTP. O teste de TLS só é aplicável com HTTPS.")
        print("[!] Para testar, altere 'scheme: http' para 'scheme: https' no arquivo nrfcfg.yaml e reinicie o Free5GC.")
        return

if __name__ == "__main__":
    test_tls_weakness()