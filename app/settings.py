#!/usr/bin/env python3

# Manage PPP daemon settings

import json
import os
import logging
from pathlib import Path

logger = logging.getLogger("pppd.settings")

# Settings file path - stored in the extension's persistent storage directory
SETTINGS_FILE = Path("/app/settings/pppd-settings.json")

# Default settings
# device:               /dev/ttyS0
# baudrate:             921600
# local_ip_address:     192.168.1.205
# remote_ip_address:    192.168.1.200

DEFAULT_SETTINGS = {
    "last_used": {
        "device": "/dev/ttyS0",
        "baudrate": "921600",
        "local_ip_address": "192.168.1.205",
        "remote_ip_address": "192.168.1.200",
    },
    "pppd": {
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


# get the last used PPP daemon settings
def get_last_used():
    """
    Get the last used PPP daemon settings

    Returns:
        dict: Dictionary with PPP daemon settings
    """
    settings = get_settings()
    return settings.get("last_used", DEFAULT_SETTINGS["last_used"])


# get the PPP daemon enabled state
def get_pppd_enabled():
    """
    Get the PPP daemon enabled state

    Returns:
        bool: True if the PPP daemon is enabled, False otherwise
    """
    try:
        settings = get_settings()

        # Check if PPP daemon section exists
        if "pppd" in settings and "enabled" in settings["pppd"]:
            return settings["pppd"]["enabled"]

        # Return default if not found
        return DEFAULT_SETTINGS["pppd"]["enabled"]
    except Exception as e:
        logger.error(f"Error getting PPP daemon enabled state: {e}")
        return False


# update the PPP daemon enabled state
def update_pppd_enabled(enabled):
    """
    Update the PPP daemon enabled state

    Args:
        enabled (bool): Whether the PPP daemon is enabled

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure PPP daemon section exists
        if "pppd" not in settings:
            settings["pppd"] = {}

        settings["pppd"]["enabled"] = enabled

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating PPP daemon enabled state: {e}")
        return False


# get PPP daemon device
def get_pppd_device():
    """
    Get the PPP daemon device

    Returns:
        str: The device (default: /dev/ttyS0)
    """
    settings = get_settings()
    return settings.get("pppd", {}).get("device", DEFAULT_SETTINGS["pppd"]["device"])


# update PPP daemon device
def update_pppd_device(device):
    """
    Update PPP daemon device

    Args:
        device (str): The device name

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure PPP daemon section exists
        if "pppd" not in settings:
            settings["pppd"] = {}

        settings["pppd"]["device"] = device

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating PPP daemon settings: {e}")
        return False


# get PPP daemon baudrate
def get_pppd_baudrate():
    """
    Get the PPP daemon baudrate

    Returns:
        int: The baudrate (default: 921600)
    """
    settings = get_settings()
    return settings.get("pppd", {}).get(
        "baudrate", DEFAULT_SETTINGS["pppd"]["baudrate"]
    )


# update PPP daemon baudrate
def update_pppd_baudrate(baudrate):
    """
    Update PPP daemon baudrate

    Args:
        baudrate (int): The baudrate

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure PPP daemon section exists
        if "pppd" not in settings:
            settings["pppd"] = {}

        settings["pppd"]["baudrate"] = baudrate

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating PPP daemon settings: {e}")
        return False


# get PPP daemon local ip address
def get_pppd_local_ip_address():
    """
    Get the PPP daemon local ip address

    Returns:
        str: The local ip address (default: 192.168.1.205)
    """
    settings = get_settings()
    return settings.get("pppd", {}).get(
        "local_ip_address", DEFAULT_SETTINGS["pppd"]["local_ip_address"]
    )


# update PPP daemon local ip address
def update_pppd_local_ip_address(ip_addr):
    """
    Update PPP daemon local ip address

    Args:
        ip_addr (str): The local ip address

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure PPP daemon section exists
        if "pppd" not in settings:
            settings["pppd"] = {}

        settings["pppd"]["local_ip_address"] = ip_addr

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating PPP daemon settings: {e}")
        return False


# get PPP daemon remote ip address
def get_pppd_remote_ip_address():
    """
    Get the PPP daemon remote ip address

    Returns:
        str: The remote ip address (default: 192.168.1.205)
    """
    settings = get_settings()
    return settings.get("pppd", {}).get(
        "remote_ip_address", DEFAULT_SETTINGS["pppd"]["remote_ip_address"]
    )


# update PPP daemon remote ip address
def update_pppd_remote_ip_address(ip_addr):
    """
    Update PPP daemon remote ip address

    Args:
        ip_addr (str): The remote ip address

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure PPP daemon section exists
        if "pppd" not in settings:
            settings["pppd"] = {}

        settings["pppd"]["remote_ip_address"] = ip_addr

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating PPP daemon settings: {e}")
        return False
