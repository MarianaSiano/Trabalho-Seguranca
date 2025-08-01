import subprocess
import json

#Configurações do teste
IMAGE_NAME = "free5gc/amf:v3.2.0" #Exemplo de imagem de contêiner da NF
K8S_NAMESPACD = "free5gc-amf-nf" #Exemplo de namespace do Kubernetes
NF_POD_NAME = "amf-pod-xyz" #Exemplo de nome de um pod

print("[+] Iniciando auditoria de infraestrutura...")