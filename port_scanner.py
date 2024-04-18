import socket
from common_ports import ports_and_services as common_ports

def resolve_service_name(port):
    """
    Resolve the service name for a given port.

    Args:
        port (int): The port number to resolve.

    Returns:
        string: The service name associated with the port.
    """
    service = common_ports.get(port)
    return service if service is not None else ""

def get_open_ports(target, port_range, verbose=False):
    """
    Scan a target for open ports within a specified port range.

    Args:
        target (str): The target IP address or hostname to scan.
        port_range (tuple): A tuple containing the start and end ports of the range to scan.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.

    Returns:
        list: A list of open ports found within the specified range.
        string: If verbose=true, A string containing descriptive information about the open ports found.
    """    
    open_ports = []
    try:
        ipv4 = socket.gethostbyname(target)
        hostname = socket.gethostbyaddr(ipv4)[0]
    except socket.gaierror:
        return "Error: Invalid IP address" if target.replace(".", "").isnumeric() else "Error: Invalid hostname"
    except socket.herror:
        hostname = ""

    for port in range(port_range[0], port_range[1] + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result =  s.connect_ex((ipv4, port))
        if result == 0:
            open_ports.append(port)
        s.close()

    if verbose:
        if hostname == "":
            output_str = f"Open ports for {ipv4}\nPORT     SERVICE\n"
        else:
            output_str = f"Open ports for {hostname} ({ipv4})\nPORT     SERVICE\n"
        if len(open_ports) == 0:
            return output_str + "No open ports found"
        for port in open_ports:
            service = resolve_service_name(port)
            output_str += f"{port:<9}{service}\n"
        return output_str.rstrip()

    return open_ports