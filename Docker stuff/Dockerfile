# Use the miniconda3 base image
FROM mambaorg/micromamba
#FROM continuumio/miniconda3

# Set the working directory to /AMBR_sampling_scheme
WORKDIR /AMBR_sampling_scheme

# Copy the current directory contents into the container at /AMBR_sampling_scheme
COPY . /AMBR_sampling_scheme

# Create the conda environment from environment.yml
RUN conda env create -f environment.yml

# Ensure the conda environment is used (replace 'da39' with your environment name)
ENV PATH=/opt/conda/envs/da39/bin:$PATH

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME=World

# Run the app.py (or AMBR_sampling_scheme.py) when the container launches
CMD ["python", "AMBR_sampling_scheme.py"]