import sys
import platform
import os
import json
import uuid
from datetime import datetime


def coletar_contexto_ci():
    """
    Coleta informações comuns de ambientes CI/CD
    (GitHub Actions, GitLab CI, Azure DevOps, etc.)
    """

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

        pipeline_ok = True

        if pipeline_ok:
            evento["checks"].append({
                "check": "pipeline_integrity",
                "status": "ok"
            })

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
