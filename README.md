# PPP Daemon

BlueOS Extension to run a PPP daemon (`pppd`) on the host computer to connect
to an autopilot via a serial port.

## Usage

Information for users

- Open the PPP Daemon tab
- Complete these fields
  - Device:
  - Baudrate:
  - Local IP Address:
  - Remote IP Address:
- Click the "Save" button to save settings
- Click the "Run" button to start the PPP daemon
 
## Developer Information

To manually install the extension in BlueOS

- Open the BlueOS Extensions tab, select "Installed"
- Push the "+" button on the bottom right
- Under "Create Extension" complete these fields
  - Extension Identifier: {your_dockerhub_user}.blueos-pppd
  - Extension Name: PPP Daemon
  - Docker image: {your_dockerhub_user}/blueos-pppd
  - Dockertag: 0.0.1
  - Settings: add the settings below in the editor

```json
{
  "ExposedPorts": {
    "8000/tcp": {}
  },
  "HostConfig": {
    "Binds": [
      "/usr/blueos/extensions/pppd/settings:/app/settings",
      "/usr/blueos/extensions/pppd/logs:/app/logs"
    ],
    "CpuQuota": 100000,
    "CpuPeriod": 100000,
    "ExtraHosts": [
      "host.docker.internal:host-gateway"
    ],
    "PortBindings": {
      "8000/tcp": [
        {
          "HostPort": ""
        }
      ]
    }
  }
}
```
