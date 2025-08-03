import subprocess
import json
import os

#--- Configurações de Ambiente (Valores Padrão do Free5GC) ---
#A3 testa a infraestrutura, não as APIs.
NF_CONFIG = {
    "IMAGE_AMF": "free5gc/amf:v3.2.0",
    "K8S_NAMESPACE": "free5gc",
    "K8S_POD_AMF": "amf-0"
}

def test_infra_config():
    print("=" * 50)
    print("A3: Testando Configuração Insegura da Infraestrutura (Kubernetes/Trivy)")
    print("=" * 50)

    #Teste de imagem de contêiner com Trivy
    try:
        print(f"[*] Escaneando a imagem '{NF_CONFIG['IMAGE_AMF']}' com Trivy...")
        result = subprocess.run(["trivy", "image", "-f", "json", NF_CONFIG['IMAGE_AMF']], capture_output=True, text=True, check=True, timeout=120)
        scan_results = json.loads(result.stdout)
        
        if any(res.get("Vulnerabilities") for res in scan_results.get("Results", [])):
            print("[!!!] VULNERABILIDADE DE IMAGEM DETECTADA! Veja o log do Trivy para detalhes.")
        else:
            print("[+] Nenhuma vulnerabilidade crítica encontrada na imagem do contêiner.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[-] Erro ao executar Trivy. Verifique se a ferramenta está instalada: {e}")
    except Exception as e:
        print(f"[-] Erro inesperado no teste A3: {e}")

    #Verificação de configurações de Pods no Kubernetes (se for o caso)
    try:
        print(f"\n[*] Verificando configurações inseguras do pod '{NF_CONFIG['K8S_POD_AMF']}'...")
        kubectl_command = f"kubectl get pod {NF_CONFIG['K8S_POD_AMF']} -n {NF_CONFIG['K8S_NAMESPACE']} -o yaml"
        result = subprocess.run(kubectl_command.split(), capture_output=True, text=True, check=True)
        
        if "privileged: true" in result.stdout:
            print("[!!!] VULNERABILIDADE DETECTADA: O pod tem privilégios de root no host.")
        if "hostNetwork: true" in result.stdout:
            print("[!!!] VULNERABILIDADE DETECTADA: O pod tem acesso total à rede do host.")
        if "allowPrivilegeEscalation: true" in result.stdout:
            print("[!!!] VULNERABILIDADE DETECTADA: O pod permite escalação de privilégios.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[-] Erro ao executar kubectl. Verifique se o pod e o namespace existem: {e}")
    except Exception as e:
        print(f"[-] Erro inesperado no teste A3: {e}")

if __name__ == "__main__":
    test_infra_config()