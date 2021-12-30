from ipaddress import IPv4Address

from ..utils import constants


class Filter:
    """Class that provides filtering for network packets.

    Attributes
    ----------
    analyzer : PacketAnalyzer
        A parsable format that wraps a packet.
    filter : str
        The filter to be applied.
    """
    def __init__(self, analyzer: "PacketAnalyzer", _filter: str):
        self.analyzer = analyzer
        self.filter = _filter

    def _apply_ip_filter(self, _filter: str) -> bool:
        """Apply filters at layer 3.

        Parameters
        ----------
        _filter : str
            The filter to be applied.

        Returns
        -------
        bool
            Whether or not the filter passed the filters.
        """
        components = tuple(comp.strip() for comp in _filter.split('='))

        match components[0]:
            case 'src':
                return self.analyzer.source_ip == IPv4Address(components[1])
            case 'dst':
                return self.analyzer.dest_ip == IPv4Address(components[1])
            case _:
                return False

    def _apply_http_filter(self, _filter: str) -> bool:
        """Apply filters at layer 7.

        Parameters
        ----------
        _filter : str
            The filter to be applied.

        Returns
        -------
        bool
            Whether or not the filter passed the filters.
        """
        components = tuple(comp.strip() for comp in _filter.split('='))

        match components[0]:
            case 'method':
                return self.analyzer.http_verb is not None and \
                       self.analyzer.http_verb == components[1].upper()
            case 'type':
                if components[1] == 'request':
                    return self.analyzer.http_verb is not None
                elif components[1] == 'response':
                    return self.analyzer.http_verb is None
            case _:
                return False

    def __bool__(self):
        if self.filter == constants.DEFAULT_FILTER:
            return True

        match self.filter[:self.filter.index('.')]:
            case 'ip':
                return self._apply_ip_filter(
                    self.filter[self.filter.index('.') + 1:]
                )
            case 'http':
                return self._apply_http_filter(
                    self.filter[self.filter.index('.') + 1:]
                )
