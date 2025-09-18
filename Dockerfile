# Final runtime stage
FROM python:3.11-slim-bookworm

# Copy installed packages from builder stage
COPY app /app
RUN python -m pip install /app --extra-index-url https://www.piwheels.org/simple

EXPOSE 8000/tcp

# application version.  This should match the register_service file's version
LABEL version="0.0.0"

ARG IMAGE_NAME

# Permissions for the container
# "Binds" section maps the host PC directories to the application directories
LABEL permissions='\
{\
  "ExposedPorts": {\
    "8000/tcp": {}\
  },\
  "HostConfig": {\
    "Binds":["/usr/blueos/extensions/$IMAGE_NAME:/app"],\
    "ExtraHosts": ["host.docker.internal:host-gateway"],\
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
LABEL readme='https://github.com/srmainwaring/blueos-pppd/blob/main/README.md'
LABEL links='{\
        "source": "https://github.com/srmainwaring/blueos-pppd"\
    }'
LABEL requirements="core >= 1.1"

ENTRYPOINT litestar run --host 0.0.0.0
