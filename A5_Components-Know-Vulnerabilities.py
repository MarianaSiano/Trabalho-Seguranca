import subprocess
import json
import os

def test_supply_chain():
    print("=" * 50)
    print("A5 - Testando Components with Know Vulnerabilities")
    print("=" * 50)

    free5gc_dir = os.path.expanduser("~/go/pkg/mod/github.com/free5gc")
    if not os.path.isdir(free5gc_dir):
        print(f"[-] O diretório {free5gc_dir} não existe. Verifique o caminho")
        return

    try:
        print(f"[*] Analisando o diretório '{free5gc_dir}' com Trivy...")
        trivy_command = ["trivy", "fs", "-f", "json", "--scanners", "vuln", free5gc_dir]
        result = subprocess.run(trivy_command, capture_output=True, text=True, check=True, timeout=300)
        scan_results = json.loads(result.stdout)
        
        if any(res.get("Vulnerabilities") for res in scan_results.get("Results", [])):
            print("[!!!] VULNERABILIDADE DE DEPENDÊNCIA DETECTADA! Verifique o log do Trivy.")
        else:
            print("[+] Nenhuma vulnerabilidade de dependência encontrada.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[-] Erro ao executar Trivy. Verifique se a ferramenta está instalada: {e}")
    except Exception as e:
        print(f"[-] Erro inesperado no teste A5: {e}")

if __name__ == "__main__":
    test_supply_chain()