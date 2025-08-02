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