import typer
from typing import Annotated, Optional

from spaces import __version__
from .common import println
from .serve import Server

from logging import getLogger, DEBUG, INFO

logger = getLogger(__name__)

app = typer.Typer(rich_markup_mode="rich")

def _version_callback(value: bool):
    if value:
        println(f"spaces CLI version [grean]{__version__}[/green]")
        raise typer.Exit()


app.add_typer(Server, name="serve")

@app.callback()
def callback(
    _version: Annotated[
        Optional[bool], typer.Option("--version", callback=_version_callback)
    ] = None,
    verbose: bool = typer.Option(False, help="Enable verbose output"),
) -> None:
    """
    Spaces CLI - The [bold]Spaces[/bold] command line app. 🌌

    Manage your [bold]Spaces[/bold] projects, run your experements, and more.
    """
    log_level = DEBUG if verbose else INFO

