import typer
import uvicorn
import ipaddress
from typing import Annotated

from .common import eprint



# Define the Server command group
Server = typer.Typer(rich_markup_mode="rich")

def host_callback( host : str) -> str:
    """
    
    """
    try:
        return str(ipaddress.IPv4Address(host))
    except ipaddress.AddressValueError as e:
        eprint(e)
        raise typer.Exit()
    
@Server.callback(invoke_without_command=True)
def serve(
    host: Annotated[
        str,
        typer.Option(
            help="The host to serve on. For local development in localhost use [blue]127.0.0.1[/blue]. To enable public access, e.g. in a container, use all the IP addresses available with [blue]0.0.0.0[/blue].",
            show_default="127.0.0.1",
            callback=host_callback
        )
    ] = "127.0.0.1",
    port: Annotated[
        int,
        typer.Option(
            help="The port to serve on. You would normally have a termination proxy on top (another program) handling HTTPS on port [blue]443[/blue] and HTTP on port [blue]80[/blue], transferring the communication to your app.",
            min=1,
            max=65_535,
            show_default="3000"
        )
    ] = 3000,
    reload: Annotated[
        bool,
        typer.Option(
            help="Enable auto-reload of the server when (code) files change. This is [bold]resource intensive[/bold], use it only during development.",
            show_default=True
        )
    ] = True,
    workers: Annotated[
        int,
        typer.Option(
            help="Enable auto-reload on code changes",
            show_default=1,
            min=1
        )
    ] = True,
):
    """
    Run a [bold]Spaces[/bold] server in [bold green]production[/bold green]. 🚀

    This command launches the Spaces server with the specified configuration.
    The server will be accessible at http://{host}:{port}.

    Examples:
        Launch server with default settings:
            $ spaces serve

        Launch on a specific port:
            $ spaces serve --port 8000

        Launch on a specific host:
            $ spaces serve --host 0.0.0.0

        Disable auto-reload:
            $ spaces serve --no-reload
    
    Args:
        host: The network interface to bind to. Use "0.0.0.0" to listen on all interfaces.
        port: The network port to listen on. Must be between 1 and 65535.
        reload: Whether to reload the server when code changes are detected.
    """
    try:
        uvicorn.run(
            "spaces.app:app",
            host=host,
            port=port,
            reload=reload,
            workers=workers,
        )
    except Exception as e:
        print(f"Failed to start server: {e}")
        raise typer.Exit(1)
    