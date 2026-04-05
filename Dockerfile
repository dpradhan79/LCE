FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy

WORKDIR /app
ENV PYTHONPATH=/app

# Install tzdata for timezone support
# tzdata is used by our code to convert time in Indian Time Zone
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y tzdata
RUN rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir --upgrade uv
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files first
COPY pyproject.toml uv.lock .env ./

# Install runtime + azure
RUN uv sync --all-extras --link-mode=copy


# Copy rest of app folders
COPY ./docs ./docs
COPY ./src ./src
COPY ./tests ./tests
COPY ./tools ./tools

EXPOSE 8000
ENTRYPOINT ["uv", "run", "pytest"]
CMD [""]