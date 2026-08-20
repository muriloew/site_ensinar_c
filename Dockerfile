FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    util-linux \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --system compiler-runner \
    && useradd --system --gid compiler-runner --no-create-home --shell /usr/sbin/nologin compiler-runner

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# O Flask permanece como supervisor; programas dos alunos perdem privilegios
# e nao conseguem ler o codigo da aplicacao nem o banco SQLite.
RUN mkdir -p /app/instance \
    && chown -R root:root /app \
    && chmod -R go-rwx /app \
    && chmod 700 /app /app/instance

ENV PORT=10000
ENV PYTHONUNBUFFERED=1
ENV COMPILER_BACKEND=local
ENV COMPILER_RUNNER_USER=compiler-runner
ENV MAX_COMPILER_JOBS=4
ENV COMPILER_COMPILE_TIMEOUT=30
ENV COMPILER_COMPILE_CPU=12
ENV COMPILER_RUN_TIMEOUT=8
ENV COMPILER_INTERACTIVE_TIMEOUT=120

CMD gunicorn -w 1 --threads 8 --timeout 75 app:app --bind 0.0.0.0:$PORT
