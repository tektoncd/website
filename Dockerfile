# Build stage - includes build tools
FROM python:3.11.15 AS builder

ENV DEBIAN_FRONTEND=noninteractive

# Install build dependencies
RUN apt-get -y update && apt-get -y install \
    git \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 22.x
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/* && \
    npm cache clean --force

# Install Go 1.22 (required by Hugo for module downloads)
RUN curl -L https://go.dev/dl/go1.22.0.linux-amd64.tar.gz -o go.tar.gz && \
    tar -C /usr/local -xzf go.tar.gz && \
    rm go.tar.gz
ENV PATH="/usr/local/go/bin:$PATH"

# Install Hugo v0.120.0
RUN curl -L https://github.com/gohugoio/hugo/releases/download/v0.120.0/hugo_extended_0.120.0_linux-amd64.tar.gz -o hugo.tar.gz && \
    tar -xzf hugo.tar.gz && \
    mv hugo /usr/local/bin/ && \
    rm hugo.tar.gz LICENSE README.md

COPY requirements.txt /tmp/requirements.txt
COPY package*.json /tmp/

WORKDIR /tmp

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt


# Runtime stage - minimal dependencies
FROM python:3.11.15 AS website

ENV DEBIAN_FRONTEND=noninteractive

# Install only runtime dependencies (no build-essential)
RUN apt-get -y update && apt-get -y install \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 22.x (runtime only, no build tools)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/* && \
    npm cache clean --force

# Copy Go from builder
COPY --from=builder /usr/local/go /usr/local/go
ENV PATH="/usr/local/go/bin:$PATH"

# Copy Hugo from builder
COPY --from=builder /usr/local/bin/hugo /usr/local/bin/hugo

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY . /src
WORKDIR /src

# Install npm packages (local dependencies and netlify-cli globally)
RUN npm install && \
    npm install -g netlify-cli@19.1.7 && \
    npm cache clean --force

RUN git config --global --add safe.directory /src

# Remove system python3 symlink and replace with python from container
# This ensures python3 always points to /usr/local/bin/python3 (3.11) even when PATH is modified
# netlify prepends /usr/bin to PATH, so we need to ensure python3 is available there
RUN rm /usr/bin/python3 && ln -s /usr/local/bin/python3 /usr/bin/python3

# Configure Netlify to bind to 0.0.0.0 so it's accessible from outside the container
ENV NETLIFY_DEV_HOST=0.0.0.0

ENTRYPOINT ["/usr/bin/netlify"]
CMD ["dev"]
