import ssl
import socket
import requests
import urllib3

#--- Configurações de Ambiente (Valores do nrfcfg.yaml)
NF_CONFIG = {
    "NRF_IP": "127.0.0.10",
    "NEF_PORT": 8000,
    "NRF_SCHEME": "https"
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_insecure_design():
    print("=" * 50)
    print("A4 - Testando Insecure Design")
    print("=" * 50)

    if NF_CONFIG["NRF_SCHEME"] == "http":
        print("[!] Sua configuração do NRF usa HTTP. O teste de TLS só é aplicável com HTTPS.")
        print("[!] Altere 'scheme: http' para 'scheme: https' no arquivo nrfcfg.yaml e reinicie o Free5GC para rodar este teste.")
        return

    vulnerable_protocols = [ssl.PROTOCOL_TLSv1, ssl.PROTOCOL_TLSv1_1]
    vulnerable_ciphers = ["RC4-SHA", "DES-CBC3-SHA"]

    def check_tls_vulnerability(protocol, cipher):
        try:
            context = ssl.create_default_context()
            context.minimum_version = protocol
            context.maximum_version = protocol
            if cipher: context.set_ciphers(cipher)
            with socket.create_connection((NF_CONFIG['NRF_IP'], NF_CONFIG['NRF_PORT']), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=NF_CONFIG['NRF_IP']) as ssock:
                    print(f"  [+] Conexão bem-sucedida usando {ssock.version()} com {ssock.cipher()[0]}")
                    return True
        except Exception as e:
            return False

    vulnerable_found = False
    for proto in vulnerable_protocols:
        if check_tls_vulnerability(proto, None):
            print(f"[!!!] VULNERABILIDADE DETECTADA: O servidor suporta o protocolo fraco {proto.name}.")
            vulnerable_found = True

    for proto in [ssl.PROTOCOL_TLSv1_2, ssl.PROTOCOL_TLSv1_3]:
        for cipher in vulnerable_ciphers:
            if check_tls_vulnerability(proto, cipher):
                print(f"[!!!] VULNERABILIDADE DETECTADA: O servidor suporta a cifra fraca {cipher} em {proto.name}.")
                vulnerable_found = True

    if not vulnerable_found:
        print("[+] Análise de TLS concluída. Nenhuma vulnerabilidade de design inseguro na criptografia detectada.")

if __name__ == "__main__":
    test_insecure_design()