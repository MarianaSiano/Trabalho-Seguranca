import subprocess
import json
import os

NF_CONFIG = {
    "IMAGE_AMF": "free5gc/amf:v1.2.5",
    "K8S_NAMESPACE": "free5gc",
    "K8S_POD_AMF": "amf-0"
}

def test_infra_conf():
    print("=" * 50)
    print("A3: Testando Configuração Insegura da Infraestrutura (Kubernetes/Trivy)")
    print("=" * 50)

    try:
        print(f"\n[*] Verificando configurações inseguras do pod '{NF_CONFIG['K8S_POD_AMF']}'...")
        kubectl_command = f"kubectl get pod {NF_CONFIG['K8S_POD_AMF']} -n {NF_CONFIG['K8S_NAMESPACE']} -o yaml"
        result = subprocess.run(kubectl_command.split(), capture_output=True, text=True, check=True)
        
        if "privileged: true" in result.stdout:
            print("[!!!] VULNERABILIDADE DETECTADA: O pod tem privilégios de root no host (privileged: true).")
        if "hostNetwork: true" in result.stdout:
            print("[!!!] VULNERABILIDADE DETECTADA: O pod tem acesso total à rede do host (hostNetwork: true).")
        if "allowPrivilegeEscalation: true" in result.stdout:
            print("[!!!] VULNERABILIDADE DETECTADA: O pod permite escalação de privilégios.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[-] Erro ao executar kubectl. Verifique se o pod e o namespace existem: {e}")
    except Exception as e:
        print(f"[-] Erro inesperado no teste A3: {e}")

if __name__ == "__main__":
    test_infra_conf()