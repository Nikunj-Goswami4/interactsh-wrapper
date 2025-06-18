FROM python:3.11-slim

# Install required tools
RUN apt update && apt install -y curl unzip

# Download and install interactsh-client binary
RUN curl -LO https://github.com/projectdiscovery/interactsh/releases/latest/download/interactsh-client_1.2.4_linux_amd64.zip \
    && unzip interactsh-client_1.2.4_linux_amd64.zip \
    && mv interactsh-client /usr/local/bin/ \
    && chmod +x /usr/local/bin/interactsh-client \
    && rm interactsh-client_1.2.4_linux_amd64.zip

# Set working directory
WORKDIR /app

# Copy source files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "run.py"]