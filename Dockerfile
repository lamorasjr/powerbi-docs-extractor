FROM python:3.12.6-slim

# Set the working directory in the container
WORKDIR /app

# Install Wine and dependencies
RUN dpkg --add-architecture i386 \
    && apt update \
    && apt install -y wine64 wine32 \
    && rm -rf /var/lib/apt/lists/*

# Copy the required files into the container
COPY pyproject.toml poetry.lock requirements.txt .env-example ./
COPY src/ ./src/
COPY tools/ ./tools/

# Set execute permissions for Windows executables
RUN chmod +x /app/tools/dax_studio/dscmd.exe

# Install Poetry
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Ensure .env exists (to be replaced with actual secrets at runtime)
RUN cp .env-example .env

# Command to run the application
CMD ["python", "src/main.py"]