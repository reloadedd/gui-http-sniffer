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


def list_filters() -> None:
    """List all possible filters to be applied for sniffed packets."""
    table = Table(title='Filters')

    table.add_column("Name", justify='left', style='cyan')
    table.add_column("Meaning", justify='center', style='magenta')
    table.add_column("Allowed Values", justify='left', style='red')

    # ip.src
    table.add_row('ip.src = <ip>',
                  'Allow only packets with the specified source IP address',
                  'any IPv4 address')
    # ip.dst
    table.add_row('ip.dst = <ip>',
                  'Allow only packets with the specified destination IP '
                  'address',
                  'any IPv4 address')
    # http.method
    table.add_row('http.method = <method>',
                  'Allow only HTTP requests using the specified method',
                  'GET, POST etc.')
    # http.type
    table.add_row('http.type = <type>',
                  'Allow only HTTP packets of that type',
                  'request, response')

    console.print(table)
