# Build stage
FROM python:3.11-slim-bookworm AS builder

# Install build dependencies for OpenCV compilation
RUN apt-get update && \
    apt-get install -y \
        autoconf \
        build-essential \
        cmake \
        git \
        libatm1-dev \ 
        libpam-dev \
        libpcap-dev \
        libssl-dev \
        libtool \
        pkg-config \
        net-tools && \
    rm -rf /var/lib/apt/lists/*

# Build pppd
RUN mkdir /ppp_ws && cd /ppp_ws && \
    git clone https://github.com/ppp-project/ppp && \
    cd ppp && \
    git submodule update --init --recursive && \
    ./autogen.sh && \
    make install

# Install Python packages
COPY app /app
RUN python -m pip install /app --extra-index-url https://www.piwheels.org/simple && \
    python -m pip install fastapi uvicorn requests

# Final runtime stage
FROM python:3.11-slim-bookworm

# Install only runtime dependencies
RUN apt-get update && \
    apt-get install -y \
        libatm1-dev \ 
        libpam-dev \
        libpcap-dev \
        libssl-dev \
        libtool \
        net-tools && \
    rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

# TODO: do not need entire build folder...
COPY --from=builder /ppp_ws /ppp_ws

EXPOSE 8000/tcp

# Application version.  This should match the register_service file's version
LABEL version="0.0.1"

# Permissions for the container
# "Binds" section maps the host PC directories to the application directories
LABEL permissions='\
{\
  "ExposedPorts": {\
    "8000/tcp": {}\
  },\
  "HostConfig": {\
    "Privileged": true,\
    "Binds":[\
      "/usr/blueos/extensions/ppp/settings:/app/settings",\
      "/usr/blueos/extensions/ppp/logs:/app/logs",\
      "/dev:/dev:rw"\
    ],\
    "CpuQuota": 100000,\
    "CpuPeriod": 100000,\
    "ExtraHosts": [\
      "host.docker.internal:host-gateway"\
    ],\
    "NetworkMode": "host",\
    "PortBindings": {\
      "8000/tcp": [\
        {\
          "HostPort": ""\
        }\
      ]\
    }\
  }\
}'

LABEL authors='[\
    {\
        "name": "Rhys Mainwaring",\
        "email": "rhys.mainwaring@me.com"\
    }\
]'

LABEL company='{\
        "about": "ArduPilot",\
        "name": "ArduPilot",\
        "email": "rhys.mainwaring@me.com"\
    }'

LABEL type="device-integration"
LABEL readme='https://github.com/srmainwaring/blueos-ppp/blob/main/README.md'
LABEL links='{\
        "source": "https://github.com/srmainwaring/blueos-ppp"\
    }'
LABEL requirements="core >= 1.1"

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
