import netifaces
from rich.table import Table

from .textutils import console


def list_interfaces() -> None:
    """List all network interfaces present in the system."""
    table = Table(title="Network Interfaces")

    table.add_column("Name", justify='center', style="cyan")
    table.add_column("MAC Address", justify='center', style="magenta")
    table.add_column("IPv4 Address", justify='center', style="green")
    table.add_column("IPv6 Address", justify='center', style="red")

    for interface in netifaces.interfaces():
        address = netifaces.ifaddresses(interface)
        table.add_row(
            interface,
            address[netifaces.AF_LINK][0]['addr'] if address.get(
                netifaces.AF_LINK, None) is not None else 'Unavailable',
            address[netifaces.AF_INET][0]['addr'] if address.get(
                netifaces.AF_INET, None) is not None else 'Unavailable',
            address[netifaces.AF_INET6][0]['addr'] if address.get(
                netifaces.AF_INET6, None) is not None else 'Unavailable',
        )

    console.print(table)
