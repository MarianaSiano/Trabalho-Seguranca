import requests
import urllib3
import json
import socket

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Endereços das NFs em diferentes "slices"
MY_NF_IP = "10.0.1.1" #Exemplo: IP da NF na Slice A
TARGET_NF_IP = "10.0.2.1" #Exemplo: IP da NF que deveria estar isolada na Slice B
TARGET_NF_PORT = 29510 #Exemplo: porta do NRF na Slice B

print("[+] Testando isolamento de Network Slicing...")

#Teste 1: Teste de conectividade a nível de rede (socket)
def test_tcp_port_conection(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=3):
            return True
    except (socket.timeout, socket.error):
        return False

if test_tcp_port_conection(TARGET_NF_IP, TARGET_NF_PORT):
    print(f"[!!!] VULNERABILIDADE DETECTADA: Falha na segmentação de rede.")
    print(f"      Um host na Slice A pode se conectar via TCP a {TARGET_NF_IP}:{TARGET_NF_PORT} na Slice B.")
else:
    print(f"[+] Conexão TCP para {TARGET_NF_IP}:{TARGET_NF_PORT} falhou. A segmentação parece estar correta.")
