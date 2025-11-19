## Installation

Before diving into R2R's features, ensure that you have completed the [installation instructions](https://r2r-docs.sciphi.ai/documentation/installation/overview).

### Prerequisites

- **Python 3.8+**: Ensure Python is installed on your system.
- **Docker**: Required for Docker-based installations. Install Docker from the [official Docker installation guide](https://docs.docker.com/engine/install/).
- **pip**: Python package installer.

### Docker Installation

This installation guide is for the **Full R2R**. For solo developers or teams prototyping, start with [R2R Light](https://r2r-docs.sciphi.ai/documentation/installation/light/local-system).

#### Install the R2R CLI & Python SDK

```bash
pip install r2r
```

> **Note**: A distinct CLI binary for R2R is under active development. For specific needs or feature requests, reach out to the R2R team.

#### Start R2R with Docker

The Full R2R installation uses a custom configuration (`full.toml`). Launch R2R with Docker:

```bash
r2r serve --docker --config-path=full.toml
```

> This command pulls necessary Docker images and starts required containers, including R2R, Hatchet, and Postgres+pgvector. Access the live server at [http://localhost:7272](http://localhost:7272/).

### Google Cloud Platform Deployment

Deploying R2R on Google Cloud Platform (GCP) involves setting up a Compute Engine instance, installing dependencies, and configuring port forwarding.

#### Overview

1. **Creating a Google Compute Engine Instance**
2. **Installing Dependencies**
3. **Setting up R2R**
4. **Configuring Port Forwarding for Local Access**
5. **Exposing Ports for Public Access (Optional)**
6. **Security Considerations**

#### Creating a Google Compute Engine Instance

1. **Log in** to the Google Cloud Console.
2. Navigate to **Compute Engine** > **VM instances**.
3. Click **Create Instance**.
4. Configure the instance:
   - **Name**: Choose a name.
   - **Region and Zone**: Select based on preference.
   - **Machine Configuration**:
     - **Series**: N1
     - **Machine type**: `n1-standard-4` (4 vCPU, 15 GB memory) or higher.
   - **Boot Disk**:
     - **OS**: Ubuntu 22.04 LTS
     - **Size**: 500 GB
   - **Firewall**: Allow HTTP and HTTPS traffic.
5. Click **Create** to launch the instance.

#### Installing Dependencies

SSH into your instance and run the following commands:

```bash
# Update package list and install Python and pip
sudo apt update
sudo apt install python3-pip -y

# Install R2R
pip install r2r

# Add R2R to PATH
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
source ~/.bashrc

# Install Docker
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg -y
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Add your user to the Docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify Docker installation
docker run hello-world
```

#### Setting up R2R

```bash
# Set required remote providers
export OPENAI_API_KEY=sk-...

# Optional - pass in a custom configuration
r2r serve --docker --full
```

#### Configuring Port Forwarding for Local Access

Use SSH port forwarding to access R2R locally:

```bash
gcloud compute ssh --zone "your-zone" "your-instance-name" -- -L 7273:localhost:7273 -L 7274:localhost:7274
```

#### Exposing Ports for Public Access (Optional)

To make R2R publicly accessible:

1. **Create a Firewall Rule**:
   - Navigate to **VPC network** > **Firewall**.
   - Click **Create Firewall Rule**.
   - **Name**: Allow-R2R
   - **Target tags**: `r2r-server`
   - **Source IP ranges**: `0.0.0.0/0`
   - **Protocols and ports**: `tcp:7272`
2. **Add Network Tag to Instance**:
   - Go to **Compute Engine** > **VM instances**.
   - Click on your instance.
   - Click **Edit**.
   - Under **Network tags**, add `r2r-server`.
   - Click **Save**.
3. **Ensure R2R Listens on All Interfaces**.

After starting R2R, access it at:

```
http://<your-instance-external-ip>:7272
```

> **Security Considerations**:
> - Use HTTPS with a valid SSL certificate.
> - Restrict source IP addresses in firewall rules.
> - Regularly update and patch your system.

#### Conclusion

You have successfully deployed R2R on Google Cloud Platform. The application is accessible locally via SSH tunneling and optionally publicly. Ensure proper security measures are in place before exposing R2R to the internet.

For more details, refer to the [R2R Configuration Documentation](https://r2r-docs.sciphi.ai/documentation/configuration/overview).

---