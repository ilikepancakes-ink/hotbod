"""Flask admin panel for hotspot management."""

from flask import Flask, render_template_string, request, redirect, url_for
from config.settings import DEFAULT_SSID, DEFAULT_PASSWORD, WEB_PORT
from network.hotspot import update_hotspot
from utils.logger import get_logger

logger = get_logger(__name__)

app = Flask(__name__)

# Global variables for current settings and process
current_ssid = DEFAULT_SSID
current_password = DEFAULT_PASSWORD
current_iface = None
hostapd_process = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PiBox Admin</title>
</head>
<body>
    <h1>PiBox Hotspot Admin</h1>
    <p>Current SSID: {{ ssid }}</p>
    <p>Current Password: {{ password }}</p>
    <form method="post">
        <label>SSID: <input type="text" name="ssid" value="{{ ssid }}" required></label><br>
        <label>Password: <input type="password" name="password" value="{{ password }}" required></label><br>
        <input type="submit" value="Update">
    </form>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main admin page to view and update hotspot settings.
    """
    global current_ssid, current_password, hostapd_process
    if request.method == 'POST':
        new_ssid = request.form['ssid']
        new_password = request.form['password']
        logger.info(f"Updating hotspot: SSID={new_ssid}, Password={new_password}")
        hostapd_process = update_hotspot(new_ssid, new_password, current_iface, hostapd_process)
        current_ssid = new_ssid
        current_password = new_password
        return redirect(url_for('index'))
    return render_template_string(HTML_TEMPLATE, ssid=current_ssid, password=current_password)


def set_current_settings(ssid: str, password: str, iface: str, process):
    """
    Set current settings for the web app.

    Args:
        ssid: Current SSID.
        password: Current password.
        iface: Hotspot interface.
        process: Hostapd process.
    """
    global current_ssid, current_password, current_iface, hostapd_process
    current_ssid = ssid
    current_password = password
    current_iface = iface
    hostapd_process = process


def run_app():
    """Run the Flask app."""
    app.run(host='0.0.0.0', port=WEB_PORT)
