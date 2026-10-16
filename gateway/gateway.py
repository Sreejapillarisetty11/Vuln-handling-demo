"""RC-100 cloud gateway (demo): reads local config, renders a
status page, sends telemetry to the manufacturer cloud over HTTPS."""
import yaml
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape

CLOUD_URL = "https://cloud.example.com/api/telemetry"

def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)  # safe loader only

def render_status(config, notes):
    env = Environment(loader=FileSystemLoader("templates"),
                      autoescape=select_autoescape())
    tpl = env.get_template("status.html")
    return tpl.render(device=config["device_name"], notes=notes)

def send_telemetry(data):
    # TLS verification on (default), no proxy, fixed cloud URL
    r = requests.post(CLOUD_URL, json=data, timeout=10)
    r.raise_for_status()
