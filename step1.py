import dns.message
import dns.rdatatype
import dns.query
import dns.exception
import dns.resolver

domain = "aws.amazon.com"
root = '198.41.0.4'
try:
    query = dns.message.make_query(domain, dns.rdatatype.A)
    ip = "168.126.63.1"
    response = dns.query.udp(query, ip, timeout = 2)
    print(response)
except dns.exception.Timeout:
    print(f"Connection to {ip} timed out.")
except dns.exception.DNSException as e:
    print(f"Error querying {ip}: {e}")