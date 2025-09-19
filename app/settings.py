#!/usr/bin/env python3

# Manage PPP settings

import json
import os
import logging
from pathlib import Path

logger = logging.getLogger("ppp.settings")

# Settings file path - stored in the extension's persistent storage directory
SETTINGS_FILE = Path("/app/settings/ppp-settings.json")

# Default PPP settings
# enabled:              false
# device:               /dev/ttyS0
# baudrate:             921600
# local_ip_address:     192.168.1.205
# remote_ip_address:    192.168.1.200

DEFAULT_SETTINGS = {
    "ppp": {
        "enabled": False,
        "device": "/dev/ttyS0",
        "baudrate": "921600",
        "local_ip_address": "192.168.1.205",
        "remote_ip_address": "192.168.1.200",
    },
}


# get the dictionary of settings from the settings file
def get_settings():
    """
    Load settings from the settings file.
    Creates default settings file if it doesn't exist.

    Returns:
        dict: The settings dictionary
    """
    try:
        if not SETTINGS_FILE.exists():
            logger.info(f"Settings file not found, creating default at {SETTINGS_FILE}")
            save_settings(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS

        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)

            return settings
    except Exception as e:
        logger.error(f"Error loading settings, using defaults: {e}")
        # Try to save default settings for next time
        try:
            save_settings(DEFAULT_SETTINGS)
        except Exception:
            logger.exception("Failed to save default settings")

        return DEFAULT_SETTINGS


# save settings to the settings file
def save_settings(settings):
    """
    Save settings to the settings file

    Args:
        settings (dict): Settings dictionary to save
    """
    try:
        # Ensure parent directory exists
        os.makedirs(SETTINGS_FILE.parent, exist_ok=True)

        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving settings: {e}")


# get the PPP enabled state
def get_ppp_enabled():
    """
    Get the PPP enabled state

    Returns:
        bool: True if PPP is enabled, False otherwise
    """
    try:
        settings = get_settings()

        # Check if PPP section exists
        if "ppp" in settings and "enabled" in settings["ppp"]:
            return settings["ppp"]["enabled"]

        # Return default if not found
        return DEFAULT_SETTINGS["ppp"]["enabled"]
    except Exception as e:
        logger.error(f"Error getting PPP enabled state: {e}")
        return False


# update the PPP enabled state
def update_ppp_enabled(enabled):
    """
    Update the PPP enabled state

    Args:
        enabled (bool): Whether PPP is enabled

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure PPP section exists
        if "ppp" not in settings:
            settings["ppp"] = {}

        settings["ppp"]["enabled"] = enabled

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating PPP enabled state: {e}")
        return False


# get PPP device
def get_ppp_device():
    """
    Get the PPP device

    Returns:
        str: The device (default: /dev/ttyS0)
    """
    settings = get_settings()
    return settings.get("ppp", {}).get("device", DEFAULT_SETTINGS["ppp"]["device"])


# update PPP device
def update_ppp_device(device):
    """
    Update PPP device

    Args:
        device (str): The device name

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure PPP section exists
        if "ppp" not in settings:
            settings["ppp"] = {}

        settings["ppp"]["device"] = device

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating PPP settings: {e}")
        return False


# get PPP baudrate
def get_ppp_baudrate():
    """
    Get the PPP baudrate

    Returns:
        int: The baudrate (default: 921600)
    """
    settings = get_settings()
    return settings.get("ppp", {}).get(
        "baudrate", DEFAULT_SETTINGS["ppp"]["baudrate"]
    )


# update PPP baudrate
def update_ppp_baudrate(baudrate):
    """
    Update PPP baudrate

    Args:
        baudrate (int): The baudrate

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure PPP section exists
        if "ppp" not in settings:
            settings["ppp"] = {}

        settings["ppp"]["baudrate"] = baudrate

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating PPP settings: {e}")
        return False


# get PPP local ip address
def get_ppp_local_ip_address():
    """
    Get the PPP local ip address

    Returns:
        str: The local ip address (default: 192.168.1.205)
    """
    settings = get_settings()
    return settings.get("ppp", {}).get(
        "local_ip_address", DEFAULT_SETTINGS["ppp"]["local_ip_address"]
    )


# update PPP local ip address
def update_ppp_local_ip_address(ip_addr):
    """
    Update PPP local ip address

    Args:
        ip_addr (str): The local ip address

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure PPP section exists
        if "ppp" not in settings:
            settings["ppp"] = {}

        settings["ppp"]["local_ip_address"] = ip_addr

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating PPP settings: {e}")
        return False


# get PPP remote ip address
def get_ppp_remote_ip_address():
    """
    Get the PPP remote ip address

    Returns:
        str: The remote ip address (default: 192.168.1.205)
    """
    settings = get_settings()
    return settings.get("ppp", {}).get(
        "remote_ip_address", DEFAULT_SETTINGS["ppp"]["remote_ip_address"]
    )


# update PPP remote ip address
def update_ppp_remote_ip_address(ip_addr):
    """
    Update PPP remote ip address

    Args:
        ip_addr (str): The remote ip address

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure PPP section exists
        if "ppp" not in settings:
            settings["ppp"] = {}

        settings["ppp"]["remote_ip_address"] = ip_addr

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating PPP settings: {e}")
        return False
