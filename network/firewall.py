"""NAT and IP forwarding setup."""

import subprocess
from utils.logger import get_logger

logger = get_logger(__name__)


def enable_ip_forwarding() -> None:
    """Enable IP forwarding in the kernel."""
    logger.info("Enabling IP forwarding")
    subprocess.run(['sudo', 'sysctl', '-w', 'net.ipv4.ip_forward=1'], check=True)


def setup_nat(upstream_iface: str, hotspot_iface: str) -> None:
    """
    Set up NAT using iptables.

    Args:
        upstream_iface: Upstream internet interface.
        hotspot_iface: Hotspot interface.
    """
    logger.info("Setting up NAT")
    # Clear existing rules
    subprocess.run(['sudo', 'iptables', '-t', 'nat', '-F'], check=True)
    subprocess.run(['sudo', 'iptables', '-F'], check=True)
    # Add NAT rule
    subprocess.run(['sudo', 'iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', upstream_iface, '-j', 'MASQUERADE'], check=True)
    # Allow forwarding
    subprocess.run(['sudo', 'iptables', '-A', 'FORWARD', '-i', hotspot_iface, '-o', upstream_iface, '-j', 'ACCEPT'], check=True)
    subprocess.run(['sudo', 'iptables', '-A', 'FORWARD', '-i', upstream_iface, '-o', hotspot_iface, '-m', 'state', '--state', 'RELATED,ESTABLISHED', '-j', 'ACCEPT'], check=True)
    # Client isolation: prevent hotspot clients from seeing each other
    subprocess.run(['sudo', 'iptables', '-I', 'FORWARD', '-i', hotspot_iface, '-o', hotspot_iface, '-j', 'DROP'], check=True)
