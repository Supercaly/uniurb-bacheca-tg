ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION} as base

WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY broker.py .

# Install cron
RUN apt update && apt -y install cron

# Copy entrypoint.sh file
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Run entrypoint.sh
CMD ["./entrypoint.sh"]
