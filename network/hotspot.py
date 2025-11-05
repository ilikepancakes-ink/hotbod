"""Configure and control hostapd."""

import subprocess
from config.settings import HOSTAPD_CONFIG_PATH, DEFAULT_SSID, DEFAULT_PASSWORD
from utils.logger import get_logger

logger = get_logger(__name__)


def generate_hostapd_config(ssid: str, password: str, iface: str) -> None:
    """
    Generate hostapd configuration file.

    Args:
        ssid: Wi-Fi network name.
        password: Wi-Fi password.
        iface: Interface to use for hotspot.
    """
    config = f"""interface={iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ap_isolate=1
"""
    with open(HOSTAPD_CONFIG_PATH, 'w') as f:
        f.write(config)
    logger.info(f"Generated hostapd config at {HOSTAPD_CONFIG_PATH}")


def start_hostapd() -> subprocess.Popen:
    """
    Start hostapd service.

    Returns:
        The subprocess.Popen object for the hostapd process.
    """
    logger.info("Starting hostapd")
    return subprocess.Popen(['sudo', 'hostapd', HOSTAPD_CONFIG_PATH])


def stop_hostapd(process: subprocess.Popen) -> None:
    """
    Stop hostapd service.

    Args:
        process: The hostapd subprocess to stop.
    """
    logger.info("Stopping hostapd")
    process.terminate()
    process.wait()


def update_hotspot(ssid: str, password: str, iface: str, current_process: subprocess.Popen = None) -> subprocess.Popen:
    """
    Update hotspot configuration and restart.

    Args:
        ssid: New SSID.
        password: New password.
        iface: Hotspot interface.
        current_process: Current hostapd process to stop.

    Returns:
        New hostapd subprocess.
    """
    if current_process:
        stop_hostapd(current_process)
    generate_hostapd_config(ssid, password, iface)
    return start_hostapd()
