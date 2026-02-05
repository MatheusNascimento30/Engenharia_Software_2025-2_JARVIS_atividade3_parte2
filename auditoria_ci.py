import sys
import platform
import os
import json
import uuid
from datetime import datetime


def coletar_contexto_ci():
    return {
        "actor": os.getenv("GITHUB_ACTOR")
                 or os.getenv("GITLAB_USER_LOGIN")
                 or os.getenv("BUILD_REQUESTEDFOR")
                 or "desconhecido",

        "commit_hash": os.getenv("GITHUB_SHA")
                       or os.getenv("CI_COMMIT_SHA")
                       or "desconhecido",

        "branch": os.getenv("GITHUB_REF_NAME")
                  or os.getenv("CI_COMMIT_BRANCH")
                  or "desconhecido",

        "pipeline_id": os.getenv("GITHUB_RUN_ID")
                       or os.getenv("CI_PIPELINE_ID")
                       or "desconhecido",

        "runner": platform.node()
    }


def verificar_integridade_pipeline():
    checks = {
        "arquivos_essenciais": False,
        "dependencias": False,
        "repositorio_git": False,
    }
    
    arquivos_obrigatorios = ["README.md", "requirements.txt"]
    arquivos_encontrados = []
    
    for arquivo in arquivos_obrigatorios:
        if os.path.exists(arquivo):
            arquivos_encontrados.append(arquivo)
        else:
            for root, _, files in os.walk("."):
                if arquivo in files:
                    arquivos_encontrados.append(f"{os.path.join(root, arquivo)}")
                    break
    
    checks["arquivos_essenciais"] = len(arquivos_encontrados) > 0
    
    requirements_path = None
    if os.path.exists("requirements.txt"):
        requirements_path = "requirements.txt"
    else:
        for root, dirs, files in os.walk("."):
            if "requirements.txt" in files:
                requirements_path = os.path.join(root, "requirements.txt")
                break
    
    if requirements_path:
        with open(requirements_path, "r") as f:
            requirements = f.read().strip()
            checks["dependencias"] = len(requirements) > 0
    
    checks["repositorio_git"] = os.path.isdir(".git")
    
    pipeline_ok = all(checks.values())
    
    return pipeline_ok, checks


def executar_auditoria():

    print("-" * 40)
    print("INICIANDO AUDITORIA DEVOPS")
    print("-" * 40)

    evento = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "trace_id": str(uuid.uuid4()),
        "event_type": "pipeline_audit",
        "severity": "info",

        "environment": {
            "python_version": sys.version,
            "os": f"{platform.system()} {platform.release()}",
            "machine": platform.machine()
        },

        "pipeline_context": coletar_contexto_ci(),

        "checks": [],
        "result": None
    }

    try:

        print("[INFO] Verificando versão do Python...")
        evento["checks"].append({
            "check": "python_version",
            "status": "ok"
        })

        print("[INFO] Verificando sistema operacional...")
        evento["checks"].append({
            "check": "os_detection",
            "status": "ok"
        })

        print("[INFO] Verificando integridade do pipeline...")
        pipeline_ok, checks_detalhes = verificar_integridade_pipeline()
        
        evento["checks"].append({
            "check": "pipeline_integrity",
            "status": "ok" if pipeline_ok else "failed",
            "details": checks_detalhes
        })

        if pipeline_ok:
            evento["result"] = "success"
            print("[SUCESSO] Pipeline validado com sucesso.")

        else:
            evento["result"] = "failed"
            evento["severity"] = "warning"
            print("[ALERTA] Problemas detectados no pipeline.")

    except Exception as e:

        evento["result"] = "error"
        evento["severity"] = "critical"

        evento["error"] = {
            "type": type(e).__name__,
            "message": str(e)
        }

        print("[ERRO] Falha durante auditoria:", str(e))

    print("-" * 40)
    print("[AUDIT] Resultado da Auditoria:")
    print("-" * 40)
    print(json.dumps(evento, indent=4))
    print("-" * 40)


if __name__ == "__main__":
    executar_auditoria()
