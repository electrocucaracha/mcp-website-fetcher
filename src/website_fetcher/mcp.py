# Copyright (c) 2025
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module the provides the implementation of a MCP server that fetches web content."""

import httpx
from mcp.server.fastmcp import FastMCP


class Server:
    """
    This class generates MCP server that fetches web site content.
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8000,
    ):
        self._mcp = FastMCP(
            name="MCP WebSite Fetcher", host=host, port=port, stateless_http=True
        )

        @self._mcp.tool(name="fetch", description="Get website content")
        async def fetch_website(url: str) -> str:
            headers = {"User-Agent": "MCP Test Server"}
            async with httpx.AsyncClient(
                follow_redirects=True, headers=headers
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.text

    @property
    def mcp(self) -> FastMCP:
        """
        Get FastMCP server created.

        Returns:
            FastMCP
        """
        return self._mcp

    def run(self, transport: str = "streamable-http"):
        """
        Initiate the FastMCP server created.
        """
        self._mcp.run(transport=transport)


server = FastMCP(
    "MCP WebSite Fetcher",
)
