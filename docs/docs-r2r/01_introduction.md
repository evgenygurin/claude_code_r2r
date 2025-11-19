# Understanding Internals of R2R Library

## Introduction

**R2R** (Retrieval to Riches) is an engine for building user-facing **Retrieval-Augmented Generation (RAG)** applications. It provides core services through an architecture of providers, services, and an integrated RESTful API. This documentation offers a detailed walkthrough of interacting with R2R, including installation, configuration, and leveraging its advanced features such as data ingestion, search, RAG, and knowledge graphs.

For a deeper dive into the R2R system architecture, refer to the [R2R System Architecture](https://r2r-docs.sciphi.ai/introduction/system).

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

## Table of Contents

- [Understanding Internals of R2R Library](#understanding-internals-of-r2r-library)
  - [Introduction](#introduction)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Docker Installation](#docker-installation)
      - [Install the R2R CLI \& Python SDK](#install-the-r2r-cli--python-sdk)
      - [Start R2R with Docker](#start-r2r-with-docker)
    - [Google Cloud Platform Deployment](#google-cloud-platform-deployment)
      - [Overview](#overview)
      - [Creating a Google Compute Engine Instance](#creating-a-google-compute-engine-instance)
  - [Table of Contents](#table-of-contents)

// ... existing code ...
