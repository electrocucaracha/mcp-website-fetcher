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

"""Module the provides a starting point for the application."""

import click

from website_fetcher.mcp import Server


@click.command()
@click.option(
    "--transport",
    help="Transport type",
    type=click.Choice(["stdio", "sse", "streamable-http"]),
    envvar="TRANSPORT",
    default="streamable-http",
)
@click.option(
    "--host",
    help="Server bind host",
    envvar="HOST",
    default="127.0.0.1",
)
@click.option(
    "--port",
    help="Server port number",
    type=click.IntRange(1024, 49151),
    envvar="PORT",
    default=8000,
)
def cli(transport: str, host: str, port: int) -> None:
    """
    This method starts a MCP server used for fetching web content

    Parameters:
        transport (str): MCP Transport type.
        host (str): Server bind host.
        port (int): Server port number.

    Returns:
        None
    """
    Server(host=host, port=port).run(transport=transport)
