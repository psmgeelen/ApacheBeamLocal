# Use an official Beam SDK image as a base
FROM apache/beam_python3.12_sdk:2.60.0

# Install UV package manager
RUN pip install uv

# Set up working directory
WORKDIR /app

# Copy only the dependency files first for better layer caching
COPY pyproject.toml uv.lock /app/

# Install dependencies using uv.lock for deterministic builds
RUN uv sync --no-default-groups

# Copy only the dependency files first for better layer caching
COPY main.py /app/

# Optional: Set entrypoint if your script is not the default
ENTRYPOINT ["uv", "run", "--no-default-groups",  "main.py"]