#!/usr/bin/env python3

# PPP Python backend
# Implements these features required by the index.html frontend:
# - Save PPP settings
# - Get PPP settings including last used settings
# - Save/get PPP enabled state (persistent across restarts)
# - "Run" button to enable PPP
# - Status endpoint to check if PPP is currently running

import logging.handlers
import sys
import asyncio

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import Query
from typing import Dict, Any

# Import the local modules
from app import ppp_process
from app import settings

# Configure console logging
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(console_formatter)

# Create logger
logger = logging.getLogger("ppp")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)

app = FastAPI()


# Global exception handler to ensure all errors return JSON
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception in {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": f"Internal server error: {str(exc)}",
            "error": "Internal server error",
        },
    )


# Global variables
ppp_running = False  # True if PPP is currently running
ppp_daemon = None

# log that the backend has started
logger.info("PPP backend started")


# Auto-start PPP if it was previously enabled
async def startup_auto_restart():
    """Check if PPP was previously enabled and auto-restart if needed"""

    # logging prefix for all messages from this function
    logging_prefix_str = "ppp:"

    try:
        enabled = settings.get_ppp_enabled()
        if enabled:
            logger.info(f"{logging_prefix_str} auto-restarting")

            # call startup function in a background thread
            asyncio.create_task(start_ppp_internal())

    except Exception as e:
        logger.error(f"{logging_prefix_str} error during auto-restart: {str(e)}")


# Internal function to start PPP
async def start_ppp_internal():
    """Internal function to start the PPP"""
    global ppp_running
    global ppp_daemon

    # logging prefix for all messages from this function
    logging_prefix_str = "ppp:"

    try:
        logger.info(f"{logging_prefix_str} started")
        ppp_running = True

        # Get settings
        device = settings.get_ppp_device()
        baudrate = settings.get_ppp_baudrate()
        local_ip_address = settings.get_ppp_local_ip_address()
        remote_ip_address = settings.get_ppp_remote_ip_address()

        if ppp_daemon is None:
            ppp_daemon = ppp_process.PPPDaemon()
        
        ppp_daemon.device = device
        ppp_daemon.baudrate = baudrate
        ppp_daemon.local = local_ip_address
        ppp_daemon.remote = remote_ip_address
        ppp_daemon.start()

        # log settings used
        logger.info(
            f"{logging_prefix_str} "
            f"device: {device}, "
            f"baudrate: {baudrate}, "
            f"local IP address:{local_ip_address}, "
            f"remote IP address:{remote_ip_address}"
        )

    except Exception as e:
        logger.error(f"{logging_prefix_str} error {str(e)}")
    finally:
        logger.info(f"{logging_prefix_str} stopped")


# PPP API Endpoints


# Load PPP settings
@app.post("/ppp/get-settings")
async def get_ppp_settings() -> Dict[str, Any]:
    """Get saved PPP settings"""
    logger.debug("Getting PPP settings")

    try:
        # Get settings
        device = settings.get_ppp_device()
        baudrate = settings.get_ppp_baudrate()
        local_ip_address = settings.get_ppp_local_ip_address()
        remote_ip_address = settings.get_ppp_remote_ip_address()

        return {
            "success": True,
            "ppp": {
                "device": device,
                "baudrate": baudrate,
                "local_ip_address": local_ip_address,
                "remote_ip_address": remote_ip_address,
            },
        }
    except Exception as e:
        logger.exception(f"Error getting PPP settings: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


# Save PPP settings
@app.post("/ppp/save-settings")
async def save_ppp_settings(
    device: str = Query(...),
    baudrate: int = Query(...),
    local_ip_address: str = Query(...),
    remote_ip_address: str = Query(...),
) -> Dict[str, Any]:
    """Save PPP settings to persistent storage (using query parameters)"""
    logger.info(
        f"Saving PPP settings: "
        f"device={device}, "
        f"baudrate={baudrate}, "
        f"local_ip_address={local_ip_address}, "
        f"remote_ip_address={remote_ip_address}"
    )

    # Save settings
    device_success = settings.update_ppp_device(device)
    baudrate_success = settings.update_ppp_baudrate(baudrate)
    local_ip_address_success = settings.update_ppp_local_ip_address(local_ip_address)
    remote_ip_address_success = settings.update_ppp_remote_ip_address(
        remote_ip_address
    )

    if (
        device_success
        and baudrate_success
        and local_ip_address_success
        and remote_ip_address_success
    ):
        return {"success": True, "message": f"Settings saved"}
    else:
        return {"success": False, "message": "Failed to save some settings"}


# Get PPP enabled state
@app.get("/ppp/get-enabled-state")
async def get_ppp_enabled_state() -> Dict[str, Any]:
    """Get saved PPP enabled state (supports both GET and POST)"""
    logger.debug("Getting PPP enabled state")

    try:
        enabled = settings.get_ppp_enabled()
        return {"success": True, "enabled": enabled}
    except Exception as e:
        logger.exception(f"Error getting PPP enabled state: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}", "enabled": False}


# Save PPP enabled state
@app.post("/ppp/save-enabled-state")
async def save_ppp_enabled_state(enabled: bool = Query(...)) -> Dict[str, Any]:
    """Save PPP enabled state to persistent storage (using query parameter)"""
    logger.info(f"PPP enabled state: {enabled}")
    success = settings.update_ppp_enabled(enabled)

    if success:
        return {"success": True, "message": f"Enabled state saved: {enabled}"}
    else:
        return {"success": False, "message": "Failed to save enabled state"}


# Get PPP status
@app.get("/ppp/status")
async def get_ppp_status() -> Dict[str, Any]:
    """Get PPP status"""
    logger.debug("Getting PPP status")

    try:
        return {
            "success": True,
            "running": ppp_running,
            "message": "Running" if ppp_running else "Stopped",
        }
    except Exception as e:
        logger.exception(f"Error getting PPP status: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}", "running": False}


# Start PPP (this is called by the frontend's "Run" button)
@app.post("/ppp/start")
async def start_ppp() -> Dict[str, Any]:
    """Start PPP"""
    logger.info(f"Start PPP request received")

    try:
        if ppp_running:
            return {"success": False, "message": "PPP is already running"}

        # Start PPP
        asyncio.create_task(start_ppp_internal())

        # Wait a few seconds to catch immediate failures
        await asyncio.sleep(2)

        # Check if it's actually running now
        if ppp_running:
            return {
                "success": True,
                "message": f"PPP started successfully",
            }
        else:
            return {
                "success": False,
                "message": "PPP failed to start (check logs for details)",
            }

    except Exception as e:
        logger.exception(f"Error starting PPP: {str(e)}")
        return {"success": False, "message": f"Failed to start: {str(e)}"}


# Stop PPP (this is called by the frontend's "Stop" button)
@app.post("/ppp/stop")
async def stop_ppp() -> Dict[str, Any]:
    """Stop PPP"""
    global ppp_running

    logger.info("Stop PPP request received")

    try:
        # Stop PPP
        ppp_running = False

        return {"success": True, "message": "PPP stopped successfully"}
    except Exception as e:
        logger.exception(f"Error stopping PPP: {str(e)}")
        return {"success": False, "message": f"Failed to stop: {str(e)}"}


# Initialize auto-restart task
@app.on_event("startup")
async def on_startup():
    """Application startup event handler"""
    await startup_auto_restart()


# Mount static files AFTER defining API routes
# Use absolute path to handle Docker container environment
static_dir = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

# Set up logging for the app
log_dir = Path("./logs")  # Use local logs directory instead of /app/logs
log_dir.mkdir(parents=True, exist_ok=True)
fh = logging.handlers.RotatingFileHandler(
    log_dir / "lumber.log", maxBytes=2**16, backupCount=1
)
logger.addHandler(fh)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
