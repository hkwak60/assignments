import dns.message
import dns.rdatatype
import dns.query
import dns.exception


def get_ip_from_additional(res: dns.message.QueryMessage):
    index = 0
    while(res.additional[index].rdtype!=1):
        index+=1
    return res.additional[index][0].address

def get_domain_from_auth(res : dns.message.QueryMessage):
    index = 0
    while(res.aut[index].rdtype!=1):
        index+=1
    return res.additional[index][0].address


def main():
  domain = input("Input domain: ")
  query = dns.message.make_query(domain, dns.rdatatype.A)
  root = '198.41.0.4'
  response = dns.query.udp(query, root, timeout = 2)
  print(mydig(query, domain, root, response))


main()