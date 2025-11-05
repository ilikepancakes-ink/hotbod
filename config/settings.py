"""Default configuration settings for the PiBox hotspot."""

# Default hotspot settings
DEFAULT_SSID = "PiBox"
DEFAULT_PASSWORD = "password123"

# Network configuration
HOTSPOT_IP = "192.168.50.1"
HOTSPOT_SUBNET = "192.168.50.0/24"
DHCP_RANGE_START = "192.168.50.10"
DHCP_RANGE_END = "192.168.50.100"

# DNS settings
DNS_DOMAIN = "pibox.lmao"

# File paths (use /tmp for testing, change to /etc for production)
HOSTAPD_CONFIG_PATH = "/tmp/hostapd.conf"
DNSMASQ_CONFIG_PATH = "/tmp/dnsmasq.conf"

# Web server settings
WEB_PORT = 80

# Logging
LOG_LEVEL = "INFO"
