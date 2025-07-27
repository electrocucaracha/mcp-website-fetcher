# MCP Website Fetcher

<!-- markdown-link-check-disable-next-line -->

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub Super-Linter](https://github.com/electrocucaracha/mcp-website-fetcher/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

<!-- markdown-link-check-disable-next-line -->

![visitors](https://visitor-badge.laobi.icu/badge?page_id=electrocucaracha.mcp-website-fetcher)
[![Scc Code Badge](https://sloc.xyz/github/electrocucaracha/mcp-website-fetcher?category=code)](https://github.com/boyter/scc/)
[![Scc COCOMO Badge](https://sloc.xyz/github/electrocucaracha/mcp-website-fetcher?category=cocomo)](https://github.com/boyter/scc/)

Model Context Protocol (MCP) Website Fetcher is a lightweight MCP server implementation that provides a simple tool for fetching website content.
It serves as a demonstration project to show how tools can be exposed and interacted with using the MCP protocol.

## Overview

This project exposes an MCP-compatible API endpoint with a tool called `fetch` that allows clients to retrieve the raw content of a specified URL.
It's designed mainly for demo purposes and testing how clients can interact with tools over the MCP protocol.

## Running the Server Using Docker

The application is automatically built and pushed to GitHub Container Registry (GHCR) on every push to the main branch.

To run the latest version locally using Docker:

```bash
docker run -d -p 8000:8000 ghcr.io/electrocucaracha/mcp-website-fetcher:main
```

> This will start the MCP server and expose it on port 8000.

## Testing Locally

Once the container is running, you can interact with the server using `curl` to test its capabilities.

### Get the List of Tools

To retrieve the list of available tools exposed by the MCP server:

```bash
curl -H "Accept: application/json, text/event-stream" \
     -H "Content-Type: application/json" \
     -d '{ "jsonrpc": "2.0", "id": 1, "method": "tools/list"}' \
     http://127.0.0.1:8000/mcp
```

### Fetch the Content of a Website

To fetch the content of `https://electrocucaracha.com/`:

```bash
curl -H "Accept: application/json, text/event-stream" \
     -H "Content-Type: application/json" \
     -d '{ "jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": { "name": "fetch", "arguments": { "url": "https://electrocucaracha.com/" }}}' \
     http://127.0.0.1:8000/mcp
```

> The server will return the HTML content of the requested URL.
