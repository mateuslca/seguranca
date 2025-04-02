from flask import Flask, request
import logging
import requests

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename="honeypot.log", level=logging.INFO, 
                    format="%(asctime)s - %(message)s")

def get_geolocation(ip):
    """Fetch geolocation data from ipinfo.io API."""
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/json", timeout=5)
        data = response.json()
        return f"{data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}, {data.get('country', 'Unknown')} - ISP: {data.get('org', 'Unknown')}"
    except Exception:
        return "Geolocation lookup failed"

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def honeypot(path):
    """Logs incoming requests, fetches geolocation, and responds with a fake '403 Forbidden' message."""
    ip_address = request.remote_addr
    location = get_geolocation(ip_address)
    
    log_entry = f"Intruder Alert! IP: {ip_address}, Location: {location}, Method: {request.method}, Path: {request.path}, Headers: {dict(request.headers)}"
    
    # Write to log file
    logging.info(log_entry)
    print(log_entry)  # Print to console for real-time monitoring

    return "403 Forbidden - Access Denied", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
