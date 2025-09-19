# BlueOS PPP

BlueOS Extension to run a PPP daemon (`pppd`) on the host computer to connect
to an autopilot via a serial port.

## Usage

Information for users

- Open the PPP tab
- Complete these fields
  - Device:
  - Baudrate:
  - Local IP Address:
  - Remote IP Address:
- Click the "Save" button to save settings
- Click the "Run" button to start PPP
 
## Developer Information

To manually install the extension in BlueOS

- Open the BlueOS Extensions tab, select "Installed"
- Push the "+" button on the bottom right
- Under "Create Extension" complete these fields
  - Extension Identifier: {your_dockerhub_user}.blueos-ppp
  - Extension Name: PPP
  - Docker image: {your_dockerhub_user}/blueos-ppp
  - Dockertag: 0.0.1
  - Settings: add the settings below in the editor

```json
{
  "ExposedPorts": {
    "8000/tcp": {}
  },
  "HostConfig": {
    "Privileged": true,
    "Binds": [
      "/usr/blueos/extensions/ppp/settings:/app/settings",
      "/usr/blueos/extensions/ppp/logs:/app/logs",
      "/dev:/dev:rw"
    ],
    "CpuQuota": 100000,
    "CpuPeriod": 100000,
    "ExtraHosts": [
      "host.docker.internal:host-gateway"
    ],
    "NetworkMode": "host",
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
