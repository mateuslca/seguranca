from flask import Flask, request
import logging
import requests
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename="honeypot.log",
    level=logging.INFO,
    format="%(message)s"
)

def get_geolocation(ip):
    """Fetch geolocation data from ipinfo.io API."""
    try:
        if ip == "127.0.0.1":
            # Fallback to your own IP for local testing
            response = requests.get("http://ipinfo.io/json", timeout=5)
        else:
            response = requests.get(f"http://ipinfo.io/{ip}/json", timeout=5)

        data = response.json()
        city = data.get('city', 'Unknown')
        region = data.get('region', 'Unknown')
        country = data.get('country', 'Unknown')
        org = data.get('org', 'Unknown')
        return f"{city}, {region}, {country} - ISP: {org}"
    except Exception as e:
        return "Geolocation lookup failed"

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def honeypot(path):
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    method = request.method
    user_agent = request.headers.get("User-Agent", "Unknown")
    location = get_geolocation(ip_address)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    log_entry = (
        f"\n🕓 [{timestamp}]\n"
        f"🌐 IP: {ip_address}\n"
        f"🗺️ Location: {location}\n"
        f"🔍 Method: {method}\n"
        f"📂 Path: /{path}\n"
        f"🧭 User-Agent: {user_agent}\n"
        f"{'-'*60}"
    )

    # Log to file and print to console
    logging.info(log_entry)
    print(log_entry)

    return "404 - Page Not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
