FROM continuumio/miniconda3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create the conda environment from environment.yml
#RUN conda env create -f environment.yml
RUN conda env export --no-builds | grep -v "prefix:" > environment.yml

# Ensure the conda environment is used
ENV PATH=/opt/conda/envs/myenv/bin:$PATH

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME=World

# Run app.py when the container launches
CMD ["python", "app.py"]