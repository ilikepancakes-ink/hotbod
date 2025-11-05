"""Detect and manage network interfaces."""

import subprocess
import netifaces
from utils.logger import get_logger

logger = get_logger(__name__)


def get_interfaces() -> list[str]:
    """
    Get list of available network interfaces, excluding loopback.

    Returns:
        List of interface names.
    """
    interfaces = netifaces.interfaces()
    return [iface for iface in interfaces if iface != 'lo']


def configure_interface(iface: str, ip: str, subnet: str) -> None:
    """
    Configure interface with static IP.

    Args:
        iface: Interface name.
        ip: IP address to assign.
        subnet: Subnet mask (not used in this implementation).
    """
    logger.info(f"Configuring {iface} with IP {ip}")
    subprocess.run(['sudo', 'ip', 'addr', 'flush', 'dev', iface], check=True)
    subprocess.run(['sudo', 'ip', 'addr', 'add', f"{ip}/24", 'dev', iface], check=True)
    subprocess.run(['sudo', 'ip', 'link', 'set', iface, 'up'], check=True)


def get_upstream_interface() -> str:
    """
    Ask user to select upstream interface.

    Returns:
        Selected upstream interface name.
    """
    interfaces = get_interfaces()
    print("Available interfaces:")
    for i, iface in enumerate(interfaces):
        print(f"{i+1}. {iface}")
    while True:
        try:
            choice = int(input("Select upstream interface (number): ")) - 1
            if 0 <= choice < len(interfaces):
                return interfaces[choice]
        except ValueError:
            pass
        print("Invalid choice. Try again.")


def get_hotspot_interface(upstream: str) -> str:
    """
    Ask user to select hotspot interface, different from upstream.

    Args:
        upstream: Upstream interface name to exclude.

    Returns:
        Selected hotspot interface name.
    """
    interfaces = get_interfaces()
    available = [iface for iface in interfaces if iface != upstream]
    print("Available interfaces for hotspot:")
    for i, iface in enumerate(available):
        print(f"{i+1}. {iface}")
    while True:
        try:
            choice = int(input("Select hotspot interface (number): ")) - 1
            if 0 <= choice < len(available):
                return available[choice]
        except ValueError:
            pass
        print("Invalid choice. Try again.")
