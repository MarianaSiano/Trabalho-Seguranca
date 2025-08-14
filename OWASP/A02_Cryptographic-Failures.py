import ssl
import socket
import requests
import urllib3

#--- Configurações de Ambiente (Valores dos arquivos .yaml) ---
NF_CONFIG = {
    "NRF_IP": "127.0.0.10",
    "NRF_PORT": 8000,
    "NRF_SCHEME": "http"
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_cryptographic_failures():
    print("=" * 50)
    print("A02 - Testando Cryptographic Failures")
    print("=" * 50)

    #Teste 1: Exposição de dados (HTTP não criptografado)
    #A configuração usa HTTP, que é uma falha de confidencialidade
    if NF_CONFIG["NRF_SCHEME"] == "http":
        print("[!!!] VULNERABILIDADE DETECTADA: O NRF usa HTTP (não criptografado)!")
        print("      O tráfego de comunicação entre as NFs pode ser interceptado (sniffing).")
        return
    else:
        print("[+] O NRF está configurado para usar HTTPS, o que é seguro.")

    #A lógica para testar TLSv1 e cifras fracas é a mesma do A04.
    print("[*] (O restante do teste de cifras fracas seria executado aqui, se o protocolo fosse HTTPS).")

if __name__ == "__main__":
    test_cryptographic_failures()