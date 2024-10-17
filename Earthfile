VERSION 0.8

pip-lockfile:
    FROM --platform=linux/amd64 ghcr.io/astral-sh/uv:python3.12-bookworm
    WORKDIR /skyline

    RUN apt-get update && apt-get install git

    COPY pyproject.toml uv.lock ./
    RUN uv pip compile pyproject.toml -o requirements.txt

    SAVE ARTIFACT requirements.txt

python-deps:
    FROM --platform=linux/amd64 python:3.12-bookworm
    WORKDIR /skyline

    ENV LANG=C.UTF-8
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    ENV PATH="/skyline/venv/bin:$PATH"

    RUN apt-get update && apt-get install git

    RUN python -m venv /skyline/venv
    COPY +pip-lockfile/requirements.txt .

    RUN pip install --no-cache-dir -r requirements.txt

    SAVE ARTIFACT venv

node-deps:
    FROM cgr.dev/chainguard/node:latest
    WORKDIR /skyline

    COPY --chown=node:node package.json package-lock.json ./
    RUN npm install

    SAVE ARTIFACT node_modules

frontend:
    FROM cgr.dev/chainguard/node:latest
    WORKDIR /skyline

    COPY +node-deps/node_modules ./node_modules

    COPY --chown=node:node package.json package-lock.json postcss.config.js tailwind.config.js vite.config.ts tsconfig.json tsconfig.app.json tsconfig.node.json ./
    COPY --chown=node:node frontend frontend
    RUN npm run build

    SAVE ARTIFACT --keep-ts frontend/dist

app:
    FROM --platform=linux/amd64 python:3.12-slim-bookworm
    WORKDIR /skyline

    ENV PYTHONUNBUFFERED=1
    ENV PATH="/skyline/venv/bin:$PATH"

    COPY +python-deps/venv /skyline/venv
    COPY --keep-ts +frontend/dist /skyline/frontend/dist
    COPY . .

    RUN apt-get update && \
        apt-get install -y libgl1 && \
        apt-get clean && \
	    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

    ENTRYPOINT ["python", "-m", "skyline"]
    CMD ["start"]

    SAVE IMAGE --push ghcr.io/nint8835/skyline:latest