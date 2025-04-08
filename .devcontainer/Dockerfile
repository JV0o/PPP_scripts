# Use Ubuntu as the base image
FROM ubuntu:20.04

# Set non-interactive mode for apt
ARG DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    bzip2 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda (version 23.1.0 as an example)
RUN curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-py39_23.1.0-0-Linux-x86_64.sh -o miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh \
    && /opt/conda/bin/conda init bash

# Set Conda environment path
ENV PATH="/opt/conda/bin:$PATH"

# Copy the environment.yml into the container
COPY environment.yml /workspace/

# Set the working directory
WORKDIR /workspace

# Expose port if necessary (for Jupyter or any web-based tool)
EXPOSE 8888

# Default command to activate the Conda environment and keep the container running
CMD ["bash", "-c", "conda activate da39 && tail -f /dev/null"]