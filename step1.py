import dns.message
import dns.rdatatype
import dns.query
import dns.exception

domain = "www.google.co"
root = '198.41.0.4'
try:
    query = dns.message.make_query(domain, dns.rdatatype.A)
    ip = root
    response = dns.query.udp(query, ip, timeout = 2)
    print(response)
except dns.exception.Timeout:
    print(f"Connection to {ip} timed out.")
except dns.exception.DNSException as e:
    print(f"Error querying {ip}: {e}")