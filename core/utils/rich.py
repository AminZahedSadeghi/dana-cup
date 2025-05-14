from rich.console import Console
from rich.theme import Theme

theme = Theme(styles={
    'info': 'cyan',
    'success': 'green b',
    'warning': 'yellow i',
    'danger': 'red b',
})

console = Console(theme=theme)
