
from typing import Optional
from rich.console import Console

def eprint(*value: object):
    """
    pretty print of a strout error recived
    """
    console = Console()
    console.print(f"[bold red]ERROR: {value}", style="italic")


def println(
    *value: object,
    sep: str = " ",
    end: str = "\n",
    style: Optional[str] = None,
    no_wrap: Optional[bool] = None,
    emoji: Optional[bool] = None,
    markup: Optional[bool] = None,
    highlight: Optional[bool] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    crop: bool = True,
    soft_wrap: Optional[bool] = None,
    new_line_start: bool = False,
) -> None:
    """
    Pretty print to console using Rich.
    """
    console = Console()
    
    # Handle new_line_start before printing
        
    console.print(
        *value,  # Ensure value is properly formatted
        sep=sep,
        end=end,
        style=style,
        no_wrap=no_wrap,
        emoji=emoji,
        markup=markup,
        highlight=highlight,
        width=width,
        height=height,
        crop=crop,
        soft_wrap=soft_wrap,
        new_line_start=new_line_start
    )