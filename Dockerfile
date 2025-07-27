FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . /app/

RUN uv sync --no-editable && uvx pex -o website-fetcher -c website-fetcher --sh-boot --include-tools .

FROM python:3.12-slim

COPY --from=builder /app/website-fetcher /opt/website-fetcher

EXPOSE 8000

ENV TRANSPORT=streamable-http
ENV HOST=0.0.0.0
ENV PORT=8000

ENTRYPOINT ["/opt/website-fetcher"]
CMD ["--host", "0.0.0.0"]
