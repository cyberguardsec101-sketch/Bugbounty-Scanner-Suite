# Bugbounty Scanner Suite

Herramienta todo-en-uno para automatizar pruebas de:

* CORS Misconfiguration
* XSS Reflejado
* SQL y NoSQL Injection

Integrando herramientas de la comunidad y validaciones personalizadas con patrones reales.

---

## 🚀 Requisitos

* Python 3.x
* Linux (Kali, Parrot, etc.)
* `Corsy` (clonado en la misma carpeta)
* `dalfox` (instalado globalmente)
* `sqlmap` (instalado o clonado globalmente)
* Archivo `subdomains.txt` con dominios o subdominios en el scope (uno por línea)

---

## 📦 Instalación rápida

```bash
sudo apt install python3-pip
pip3 install -r requirements.txt  # si usas requests

# Clonar herramientas necesarias
git clone https://github.com/s0md3v/Corsy.git
sudo go install github.com/hahwul/dalfox/v2@latest
```

---

## 🛠️ Ejecución

```bash
python3 scanner.py
```

Esto mostrará el banner ASCII:

```
  ____             _                      _                 
 |  _ \           | |                    | |                
 | |_) | __ _  ___| | _____ _ __ ___  ___| |_ ___  _ __ ___
 |  _ < / _` |/ __| |/ / _ \ '__/ __|/ _ \ __/ _ \| '__/ _ \
 | |_) | (_| | (__|   <  __/ |  \__ \  __/ || (_) | | |  __/
 |____/ \__,_|\___|_|\_\___|_|  |___/\___|\__\___/|_|  \___|
```

Y ejecutará tres fases:

1. **CORS Scan:** con Corsy y prueba personalizada con `Origin: evil.com`
2. **XSS Scan:** con Dalfox y validación reflejada de `<script>alert(1)</script>`
3. **SQL/NoSQL Scan:** con SQLMap y payload `$ne$test`

---

## 📁 Salidas generadas

* `cors_results.txt`: dominios con configuración CORS débil
* `xss_results.txt`: URLs vulnerables o que reflejan payloads
* `sql_results.txt`: hallazgos de SQLMap o respuestas sospechosas de NoSQL

---

## 🔍 ¿Cómo validar?

Cada sección agrega una POC o ejemplo:

* CORS: si `Access-Control-Allow-Origin` refleja `evil.com` y hay `Allow-Credentials: true` → se considera explotable.
* XSS: si la respuesta refleja `alert(1)` sin codificar → posible vector reflejado.
* SQLi: si SQLMap confirma inyección y obtiene datos → crítico.
* NoSQL: si al inyectar `$ne$test` cambia la lógica de respuesta → riesgo.

---

## 💡 Sugerencias

* Usa proxy como Burp para validar manualmente respuestas sospechosas.
* Puedes separar cada escáner en scripts individuales si lo deseas.
* Combínalo con `gf`, `waybackurls`, `httpx`, etc. para expansión de superficie.

---

## 📜 Licencia

Este script es de uso ético y educativo. Solo escanea dominios autorizados (en el scope de programas públicos o con consentimiento).

---

## ✉️ Contacto

Desarrollado en base a investigación personalizada por ChatGPT + comunidad bug bounty.

¿Tienes dudas o quieres mejorar este suite? ¡Forkéalo y contribuye!
