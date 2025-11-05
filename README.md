# PiBox Hotspot

A configurable Wi-Fi hotspot for Raspberry Pi0

## Features

- Entirely Python-based (no Bash scripts, no external web servers)
- Automatically detects available network interfaces
- Configures hotspot interface with static IP (192.168.50.1/24)
- Provides DHCP and DNS services using dnsmasq
- Manages Wi-Fi hotspot using hostapd
- Built-in Flask web admin panel at http://pibox.lmao
- Handles IP forwarding and NAT for internet sharing

## Requirements

- Raspberry Pi (tested on Raspberry Pi OS)
- Wi-Fi adapter capable of AP mode
- Python 3.7+
- sudo privileges

## Installation

1. Update your system:
   ```
   sudo apt update
   sudo apt upgrade
   ```

2. Install required system packages:
   ```
   sudo apt install hostapd dnsmasq python3 python3-pip
   ```

3. Install Python dependencies:
   ```
   pip3 install flask netifaces
   ```

4. Clone or copy the project files to your Raspberry Pi.

## Usage

1. Run the application with sudo:
   ```
   sudo python3 main.py
   ```

2. Follow the interactive prompts to select:
   - Upstream interface (for internet connection)
   - Hotspot interface (for Wi-Fi clients)

3. The hotspot will start automatically, and you'll see log messages.

4. The admin panel will be available at http://pibox.lmao (accessible from connected devices).

5. To change SSID or password, visit the admin panel and submit the form.

6. Press Ctrl+C to stop the hotspot and clean up.

## Project Structure

```
pibox/
├── main.py                 # Entrypoint script
├── config/
│   ├── __init__.py
│   └── settings.py         # Default configuration
├── network/
│   ├── __init__.py
│   ├── interfaces.py       # Interface detection and configuration
│   ├── hotspot.py          # Hostapd management
│   ├── dhcp_dns.py         # DHCP/DNS server (dnsmasq)
│   └── firewall.py         # NAT and IP forwarding
├── web/
│   ├── __init__.py
│   └── app.py              # Flask admin panel
├── utils/
│   ├── __init__.py
│   └── logger.py           # Logging utilities
└── README.md
```

## Configuration

Edit `config/settings.py` to change default values:

- DEFAULT_SSID: Default Wi-Fi network name
- DEFAULT_PASSWORD: Default Wi-Fi password
- HOTSPOT_IP: Hotspot gateway IP
- DNS_DOMAIN: Domain for admin panel (pibox.lmao)
- WEB_PORT: Port for admin panel (80)

## Notes

- The application generates temporary config files in /tmp. For production use, change paths in settings.py to /etc/hostapd/ and /etc/dnsmasq.d/
- Ensure your Wi-Fi adapter supports AP mode
- The admin panel is served on port 80, accessible via the hotspot IP
- DNS resolves pibox.lmao to 192.168.50.1
- All network configuration is done via Python subprocess calls

## Troubleshooting

- If hostapd fails to start, check that your Wi-Fi adapter supports AP mode
- Ensure no other services are using the selected interfaces
- Check system logs with `journalctl -f` for detailed error messages
- For testing without actual hardware, you may need to adjust interface detection

## License

This project is provided as-is for educational purposes.
