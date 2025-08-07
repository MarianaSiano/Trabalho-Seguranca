import ssl
import socket
import requests
import urllib3

#--- Configurações de Ambiente (Valores dos arquivos .yaml)
NF_CONFIG = {
    "AMF_IP": "172.16.0.114", # IP da máquina do 5G Core
    "AMF_PORT_SSH": 22,       # Porta padrão do SSH
    "AMF_PORT_TELNET": 23     # Porta padrão do Telnet
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_cryptographic_failures():
    print("=" * 50)
    print("A2 - Testando Cryptographic Failures")
    print("=" * 50)

    print("[*] Referência: O PDF sobre Telnet/SSH destaca a falta de criptografia do Telnet.")
    
    ports_to_test = {
        "SSH (Seguro)": NF_CONFIG["AMF_PORT_SSH"],
        "Telnet (Inseguro)": NF_CONFIG["AMF_PORT_TELNET"]
    }

    for protocol, port in ports_to_test.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((NF_CONFIG["AMF_IP"], port))
            s.close()
            is_open = True
        except (socket.timeout, socket.error):
            is_open = False

        if is_open and protocol == "Telnet (Inseguro)":
            print(f"[!!!] VULNERABILIDADE DETECTADA: A porta Telnet ({port}) está aberta. Isso expõe o tráfego sem criptografia.")
        elif is_open:
            print(f"[+] A porta {protocol} ({port}) está aberta. Este é um protocolo seguro para acesso remoto.")
        else:
            print(f"[-] A porta {protocol} ({port}) está fechada.")

if __name__ == "__main__":
    test_cryptographic_failures()