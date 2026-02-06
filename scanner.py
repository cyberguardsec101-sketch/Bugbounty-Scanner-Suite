#!/usr/bin/env python3

"""
Script principal que automatiza pruebas de:
- CORS Misconfiguration
- XSS Reflejado
- SQL/NoSQL Injection

Usa herramientas comunitarias (Corsy, Dalfox, SQLMap) y aplica lógica personalizada basada en patrones conocidos para validar hallazgos.

Requiere: `subdomains.txt` como input.
"""

import subprocess
import os
import re
import requests
from datetime import datetime

INPUT_FILE = "subdomains.txt"
CORS_OUTPUT = "cors_results.txt"
XSS_OUTPUT = "xss_results.txt"
SQL_OUTPUT = "sql_results.txt"

HACKER_ASCII = r"""
  ____             _                      _                 
 |  _ \           | |                    | |                
 | |_) | __ _  ___| | _____ _ __ ___  ___| |_ ___  _ __ ___ 
 |  _ < / _` |/ __| |/ / _ \ '__/ __|/ _ \ __/ _ \| '__/ _ \
 | |_) | (_| | (__|   <  __/ |  \__ \  __/ || (_) | | |  __/
 |____/ \__,_|\___|_|\_\___|_|  |___/\___|\__\___/|_|  \___|
                                                          
"""

def banner():
    print(HACKER_ASCII)
    print("""
[+] Bug Bounty Scanner Suite
    CORS + XSS + SQLi Scanner
    Integrando herramientas: Corsy, Dalfox, SQLMap
    Incluye validaciones personalizadas por patrones conocidos
    """)


def run_cors_scan():
    print("\n[+] Iniciando escaneo CORS con Corsy...")
    cmd = ["python3", "Corsy/corsy.py", "-i", INPUT_FILE]
    with open(CORS_OUTPUT, "w") as f:
        subprocess.run(cmd, stdout=f)

    # Validación personalizada: patrón de CORS permisivo
    print("[+] Validación personalizada CORS...")
    with open(CORS_OUTPUT, "a") as out:
        with open(INPUT_FILE) as f:
            for domain in f:
                domain = domain.strip()
                try:
                    headers = {"Origin": f"http://evil.com"}
                    r = requests.get(domain, headers=headers, timeout=5)
                    if ("Access-Control-Allow-Origin" in r.headers and
                        "evil.com" in r.headers.get("Access-Control-Allow-Origin") and
                        "Access-Control-Allow-Credentials" in r.headers):
                        out.write(f"[!] {domain} vulnerable a CORS (valido personalizado)\n")
                except:
                    continue
    print(f"[✓] Resultados guardados en {CORS_OUTPUT}")


def run_xss_scan():
    print("\n[+] Iniciando escaneo XSS con Dalfox...")
    urls_file = "xss_targets.txt"
    generate_urls_from_subdomains(urls_file)
    cmd = ["dalfox", "file", urls_file, "--output", XSS_OUTPUT]
    subprocess.run(cmd)

    # Validación personalizada de reflejo de payload simple
    print("[+] Validación personalizada XSS...")
    with open(XSS_OUTPUT, "a") as out:
        with open(urls_file) as f:
            for url in f:
                url = url.strip().replace("test", "<script>alert(1)</script>")
                try:
                    r = requests.get(url, timeout=5)
                    if "<script>alert(1)</script>" in r.text:
                        out.write(f"[!] {url} refleja <script>alert(1)</script> — posible XSS\n")
                except:
                    continue
    print(f"[✓] Resultados guardados en {XSS_OUTPUT}")


def run_sql_scan():
    print("\n[+] Iniciando escaneo SQL/NoSQLi con SQLMap...")
    with open(INPUT_FILE) as f:
        targets = [line.strip() for line in f if line.strip()]
    with open(SQL_OUTPUT, "w") as out:
        for url in targets:
            print(f"\n[>] Probando {url}...")
            cmd = ["sqlmap", "-u", url, "--batch", "--level=2", "--risk=2"]
            subprocess.run(cmd, stdout=out, stderr=subprocess.DEVNULL)

            # Prueba adicional NoSQL payload
            try:
                payload_url = url + ("?user=$ne$test" if "?" not in url else "&user=$ne$test")
                r = requests.get(payload_url, timeout=5)
                if "error" not in r.text.lower():
                    out.write(f"[+] Posible NoSQLi detectada: {payload_url}\n")
            except:
                continue
    print(f"[✓] Resultados guardados en {SQL_OUTPUT}")


def generate_urls_from_subdomains(output_file):
    with open(INPUT_FILE) as f:
        subs = [line.strip() for line in f if line.strip()]
    with open(output_file, "w") as out:
        for sub in subs:
            out.write(f"{sub}/?q=test\n")
            out.write(f"{sub}/search.php?search=test\n")
            out.write(f"{sub}/page.php?name=test\n")


def summary():
    print("\n[✓] Escaneos completados. Archivos generados:")
    print(f"    - CORS: {CORS_OUTPUT}")
    print(f"    - XSS:  {XSS_OUTPUT}")
    print(f"    - SQLi: {SQL_OUTPUT}")
    print("\n[!] Revisa manualmente los resultados y realiza POC según los payloads exitosos.")


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[x] Archivo requerido '{INPUT_FILE}' no encontrado.")
        return
    banner()
    run_cors_scan()
    run_xss_scan()
    run_sql_scan()
    summary()


if __name__ == "__main__":
    main()
