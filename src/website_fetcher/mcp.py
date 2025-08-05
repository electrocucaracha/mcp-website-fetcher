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

import git
import httpx
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


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
        self._metadata = None

        @self._mcp.tool(name="fetch", description="Get website content")
        async def fetch_website(url: str) -> str:
            headers = {"User-Agent": "MCP Test Server"}
            async with httpx.AsyncClient(
                follow_redirects=True, headers=headers
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.text

        @self._mcp.custom_route("/health", methods=["GET"])
        def health_check(_: Request) -> Response:
            """
            Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
            to ensure a robust container orchestration and management is in place. Other
            services which rely on proper functioning of the API service will not deploy if this
            endpoint returns any other HTTP status code except 200 (OK).

            Returns:
                Returns a JSON response with the health status
            """
            return JSONResponse({"status": "ok"})

        @self._mcp.custom_route("/.well-known/mcp.json", methods=["GET"])
        async def well_known_mcp(_: Request) -> Response:
            """
            Endpoint to return MCP metadata information. This endpoint is used by MCP to
            determine what tools, prompts and resources are available and how to be used.

            Returns:
                Returns a JSON response with the metadata information
            """

            if self._metadata is None:
                features = []
                for items, item_type in [
                    (await self._mcp.list_tools(), "tool"),
                    (await self._mcp.list_prompts(), "prompt"),
                    (await self._mcp.list_resources(), "resource"),
                ]:
                    for item in items:
                        t = vars(item)
                        t["type"] = item_type
                        features.append(t)

                repo = git.Repo(search_parent_directories=True)

                self._metadata = JSONResponse(
                    {
                        "name": self._mcp.name,
                        "description": "MCP Server that fetches websites content of a given URL.",
                        "schemaVersion": "2025-06-18",
                        "transport": ["streamable-http"],
                        "language": "python",
                        "authentication": [],
                        "git": {
                            "repository": repo.remote().url,
                            "commitSHA": repo.head.object.hexsha,
                        },
                        "features": features,
                    }
                )

            return self._metadata

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
