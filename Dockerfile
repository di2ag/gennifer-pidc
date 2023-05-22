FROM julia:1.9

WORKDIR /
COPY installPackages.jl /

# Julia libs we want
RUN julia installPackages.jl

RUN apt-get update && apt-get install -y time python3-pip

# Set the working directory to /app
WORKDIR /app

COPY ./requirements.txt /app

# Install the required packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5000 for the Flask app to listen on
EXPOSE 5000

# Start the Flask app
CMD ["flask", "--app", "pidc", "run", "--host", "0.0.0.0", "--debug"]
