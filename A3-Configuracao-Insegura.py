import subprocess
import json

#Configurações do teste
IMAGE_NAME = "free5gc/amf:v3.2.0" #Exemplo de imagem de contêiner da NF
K8S_NAMESPACE = "free5gc-amf-nf" #Exemplo de namespace do Kubernetes
NF_POD_NAME = "amf-pod-xyz" #Exemplo de nome de um pod

print("[+] Iniciando auditoria de infraestrutura...")

#--- Análise de Imagem de Contêiner com Trivy ---
print("\n[*] Escaneando a imagem do contêiner com Trivy...")
try:
    trivy_command = ["trivy", "image", "-f", "json", IMAGE_NAME]
    result = subprocess.run(trivy_command, capture_output=True, text=True, check=True)
    scan_results = json.loads(result.stdout)

    vulnerabilities = scan_results.get("Results", [])
    if vulnerabilities:
        print("[!!!] VULNERABILIDADE DE IMAGEM DETECTADA!")
        for res in vulnerabilities:
            for vuln in res["Vulnerabilities"]:
                print(f"  - ID: {vuln['VulnerabilityID']}, Severidade: {vuln['Severity']}, Pacote: {vuln['PkgName']}")
    else:
        print("[+] Nenhuma vulnerabilidade encontrada na imagem do contêiner.")

except Exception as e:
    print(f"[-] Erro ao executar Trivy: {e}")

#--- Verificação de configurações de Pods no Kubernetes ---
print("\n[*] Verificando configurações inseguras de Pods com kubectl...")
try:
    kubectl_command = f"kubectl get pod {NF_POD_NAME} -n {K8S_NAMESPACE} -o yaml"
    result = subprocess.run(kubectl_command.split(), capture_output=True, text=True, check=True)

    if "privileged: true" in result.stdout:
        print("[!!!] VULNERABILIDADE DETECTADA: O pod tem privilégios de root no host (privileged: true).")

    if "hostNetwork: true" in result.stdout:
        print("[!!!] VULNERABILIDADE DETECTADA: O pod tem acesso total à rede do host (hostNetwork: true).")

    if "allowPrivilegeEscalation: true" in result.stdout:
        print("[!!!] VULNERABILIDADE DETECTADA: O pod permite escalação de privilégios.")

except Exception as e:
    print(f"[-] Erro ao executar kubectl: {e}")

print("\n[+] Auditoria de infraestrutura concluída.")