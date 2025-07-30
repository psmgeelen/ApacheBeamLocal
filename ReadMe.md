I'll analyze the repository and create a comprehensive README.md for the Apache Beam local development project.

# Apache Beam Local Development Example

This repository demonstrates how to work with Apache Beam locally, showcasing a simple data processing pipeline with sensor data statistics. It includes Docker containerization for easy deployment and demonstrates best practices for setting up a Beam development environment.

## Overview

This project illustrates:

1. Creating and running Apache Beam pipelines locally
2. Using SciPy for statistical calculations within a Beam pipeline
3. Implementing windowing and CombineFn in Apache Beam
4. Containerizing a Beam application with Docker
5. Managing dependencies with UV package manager

## Repository Structure

- `main.py` - The Apache Beam pipeline for processing sensor data and calculating statistics
- `pyproject.toml` - Project configuration and dependency management
- `uv.lock` - Locked dependencies for deterministic builds
- `Dockerfile` - Container definition for running the application

## The Pipeline

The pipeline in `main.py` demonstrates key Apache Beam concepts:

- Reading and processing sensor temperature data
- Fixed windowing (60-second windows) to group data points
- Custom `CombineFn` implementation for calculating statistics
- Integration with SciPy for advanced statistical calculations
- Formatting and displaying results

## Dependencies

The project uses the following main dependencies:

- `apache-beam[gcp]==2.60.0` - The Apache Beam SDK with Google Cloud Platform extensions
- `scipy>=1.16.1` - Scientific computing library used for statistical calculations

Additional dependency groups are defined for development and interactive use:

### Development Dependencies
- `black>=25.1.0` - Code formatter
- `ruff>=0.12.5` - Linter

### Interactive Dependencies
- `apache-beam[interactive]>=2.60.0` - Interactive Beam extensions
- `notebook>=7.4.4` - Jupyter notebook support

## Package Management

This project uses UV, a modern Python package manager:

- Fast dependency resolution
- Deterministic builds with lockfiles
- Dependency grouping for development vs. production

## Running Locally

### Prerequisites

- Python 3.12
- UV package manager

### Setup

1. Clone the repository
2. Install dependencies:

```shell script
uv sync
```


3. Run the pipeline:

```shell script
uv run main.py
```


## Docker Deployment

The project includes a Dockerfile for containerized deployment:

```shell script
# Build the Docker image
docker build -t apachebeamtest .

# Run the container
docker run apachebeamtest
```


The Docker image:
- Uses an official Apache Beam Python 3.12 SDK base image
- Installs only required production dependencies (not dev dependencies)
- Provides a consistent, reproducible environment for the pipeline

## Example Output

When running the pipeline, you'll see output similar to:

```
Running pipeline with SciPy Statistics:
Sensor: sensor_A, Window: 2023-03-15 13:20:00, Stats: Count=2, Mean=20.25, StdDev=0.3536, Variance=0.0002
Sensor: sensor_A, Window: 2023-03-15 13:21:00, Stats: Count=2, Mean=20.65, StdDev=0.4950, Variance=0.0003
Sensor: sensor_A, Window: 2023-03-15 13:22:00, Stats: Count=1, Mean=22.00, StdDev=nan, Variance=0.0000
Sensor: sensor_A, Window: 2023-03-15 13:23:00, Stats: Count=1, Mean=23.00, StdDev=nan, Variance=0.0000
Sensor: sensor_A, Window: 2023-03-15 13:24:00, Stats: Count=3, Mean=21.00, StdDev=1.0000, Variance=0.0015
Sensor: sensor_B, Window: 2023-03-15 13:20:00, Stats: Count=1, Mean=25.00, StdDev=nan, Variance=0.0000
Sensor: sensor_B, Window: 2023-03-15 13:21:00, Stats: Count=1, Mean=24.50, StdDev=nan, Variance=0.0000
Sensor: sensor_B, Window: 2023-03-15 13:22:00, Stats: Count=1, Mean=26.00, StdDev=nan, Variance=0.0000
```


## Key Features Demonstrated

### Apache Beam Concepts
- PCollection transformations
- Windowing (Fixed Windows)
- Custom CombineFn for aggregation
- Timestamps and event time processing

### Integration with SciPy
- Using SciPy's statistical functions within a Beam pipeline
- Efficient calculation of mean, standard deviation, and variance

### Dependency Management
- Using UV for modern package management
- Separating production and development dependencies

### Containerization
- Containerizing a Beam application for easy deployment
- Optimizing Docker images for production use

## Advanced Usage

### Interactive Mode

For interactive development with Jupyter notebooks:

```shell script
uv sync --group interactive
uv run --group interactive -m jupyter notebook
```


### Development Environment

For local development with code formatting and linting:

```shell script
uv sync --group dev
```


## License

UNLICENSE