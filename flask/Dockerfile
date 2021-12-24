# Set base image (host OS)
FROM continuumio/miniconda3
LABEL maintainer="mdwaldman"

RUN conda config --add channels conda-forge && conda update -y conda \
&& conda install -y geopandas

RUN conda install pip

EXPOSE 8000/tcp

# Set the working directory in the container
WORKDIR /app


# Copy the dependencies file to the working directory
COPY requirements.txt .

RUN pip install --upgrade pip


# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

CMD ["python", "wsgi.py"]
