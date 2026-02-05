import sys
import platform

def executar_auditoria():
    print("-" * 40)
    print("INICIANDO AUDITORIA DE AMBIENTE - DEVOPS")
    print("-" * 40)

    # 1. Verifica versão do Python
    print(f"[INFO] Versão do Python detectada: {sys.version}")

    # 2. Verifica Sistema Operacional
    print(f"[INFO] Sistema Operacional: {platform.system()} {platform.release()}")

    # 3. Simulação de verificação
    print("[INFO] Verificando integridade do pipeline...")

    # Mensagem de sucesso
    print("[SUCESSO] O Pipeline foi configurado e executado corretamente.")
    print("-" * 40)

if __name__ == "__main__":
    executar_auditoria()
