"""Entrypoint for the PiBox hotspot application."""

import threading
import signal
import sys
from config.settings import DEFAULT_SSID, DEFAULT_PASSWORD, HOTSPOT_IP, HOTSPOT_SUBNET
from network.interfaces import get_upstream_interface, get_hotspot_interface, configure_interface
from network.hotspot import generate_hostapd_config, start_hostapd
from network.dhcp_dns import generate_dnsmasq_config, start_dnsmasq
from network.firewall import enable_ip_forwarding, setup_nat
from web.app import set_current_settings, run_app
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Main function to start the hotspot."""
    logger.info("Starting PiBox hotspot")

    # Get interfaces
    upstream = get_upstream_interface()
    hotspot_iface = get_hotspot_interface(upstream)
    logger.info(f"Upstream: {upstream}, Hotspot: {hotspot_iface}")

    # Configure hotspot interface
    configure_interface(hotspot_iface, HOTSPOT_IP, HOTSPOT_SUBNET)

    # Enable IP forwarding and NAT
    enable_ip_forwarding()
    setup_nat(upstream, hotspot_iface)

    # Generate and start hostapd
    generate_hostapd_config(DEFAULT_SSID, DEFAULT_PASSWORD, hotspot_iface)
    hostapd_proc = start_hostapd()

    # Generate and start dnsmasq
    generate_dnsmasq_config(hotspot_iface)
    dnsmasq_proc = start_dnsmasq()

    # Set web app settings
    set_current_settings(DEFAULT_SSID, DEFAULT_PASSWORD, hotspot_iface, hostapd_proc)

    # Start web app in thread
    web_thread = threading.Thread(target=run_app)
    web_thread.daemon = True
    web_thread.start()

    logger.info("PiBox hotspot started. Admin panel at http://pibox.lmao")

    # Wait for interrupt
    def signal_handler(sig, frame):
        logger.info("Shutting down...")
        hostapd_proc.terminate()
        dnsmasq_proc.terminate()
        hostapd_proc.wait()
        dnsmasq_proc.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()


if __name__ == "__main__":
    main()
