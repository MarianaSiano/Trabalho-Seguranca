import requests
import socket
import ssl
import urllib3
import matplotlib.pyplot as plt

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NF_CONFIG = {
    "NRF_IP": "127.0.0.10",
    "NRF_PORT": 8000,
    "NRF_SCHEME": "http",
    "UDM_IP": "127.0.0.3",
    "UDM_PORT": 8000,
    "SUPI_2": "208930000000002"
}

def test_cryptographic_failures():
    print("=" * 50)
    print("A2 - Testando Criptografia")
    print("=" * 50)

    http_insecure, tls_weak = 0, 0
    if NF_CONFIG["NRF_SCHEME"] == "http":
        print("[!!!] HTTP inseguro em uso")
        http_insecure = 1
    return http_insecure, tls_weak