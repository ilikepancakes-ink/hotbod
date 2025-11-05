"""Lightweight DHCP/DNS server logic using dnsmasq."""

import subprocess
from config.settings import (
    DNSMASQ_CONFIG_PATH,
    HOTSPOT_IP,
    DHCP_RANGE_START,
    DHCP_RANGE_END,
    DNS_DOMAIN
)
from utils.logger import get_logger

logger = get_logger(__name__)


def generate_dnsmasq_config(iface: str) -> None:
    """
    Generate dnsmasq configuration file.

    Args:
        iface: Interface to bind dnsmasq to.
    """
    config = f"""interface={iface}
dhcp-range={DHCP_RANGE_START},{DHCP_RANGE_END},12h
dhcp-option=3,{HOTSPOT_IP}
dhcp-option=6,{HOTSPOT_IP}
address=/{DNS_DOMAIN}/{HOTSPOT_IP}
"""
    with open(DNSMASQ_CONFIG_PATH, 'w') as f:
        f.write(config)
    logger.info(f"Generated dnsmasq config at {DNSMASQ_CONFIG_PATH}")


def start_dnsmasq() -> subprocess.Popen:
    """
    Start dnsmasq service.

    Returns:
        The subprocess.Popen object for the dnsmasq process.
    """
    logger.info("Starting dnsmasq")
    return subprocess.Popen(['sudo', 'dnsmasq', '-C', DNSMASQ_CONFIG_PATH])


def stop_dnsmasq(process: subprocess.Popen) -> None:
    """
    Stop dnsmasq service.

    Args:
        process: The dnsmasq subprocess to stop.
    """
    logger.info("Stopping dnsmasq")
    process.terminate()
    process.wait()
