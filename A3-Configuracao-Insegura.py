import subprocess
import json

#Configurações do teste
IMAGE_NAME = "free5gc/amf:v3.2.0" #Exemplo de imagem de contêiner da NF
K8S_NAMESPACD = "free5gc-amf-nf" #Exemplo de namespace do Kubernetes
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