import requests
import urllib3
import json
import base64
import os

#--- Configurações de Ambiente (Valores do nefcfg.yaml)
NF_CONFIG = {
    "NEF_IP": "127.0.0.1",
    "NEF_PORT": 29509
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)