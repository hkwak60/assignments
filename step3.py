import dns.message
import dns.rdatatype
import dns.query
import dns.exception


def get_ip_from_additional(res: dns.message.QueryMessage):
    index = 0
    while(res.additional[index].rdtype!=1):
        index+=1
    return res.additional[index][0].address

def mydig(q : dns.message.QueryMessage, domain, root, r : dns.message.QueryMessage):
    while(True):
        while(len(r.answer)==0):
            addr = get_ip_from_additional(r)
            r = dns.query.udp(q, addr, timeout = 2)
        if(r.answer[0][0].rdtype==dns.rdatatype.A):
            break
        while(r.answer[0][0].rdtype!=dns.rdatatype.A):
            domain = r.answer[0][0].__str__()
            q = dns.message.make_query(domain, r.answer[0][0].rdtype)
            r = dns.query.udp(q, root, timeout = 2)
            while len(r.answer)==0:
                q = dns.message.make_query(domain, dns.rdatatype.A)
                addr = get_ip_from_additional(r)
                r = dns.query.udp(q, addr, timeout = 2)
    return r

def main():
  domain = input("Input domain: ")
  query = dns.message.make_query(domain, dns.rdatatype.A)
  root = '198.41.0.4'
  response = dns.query.udp(query, root, timeout = 2)
  print(mydig(query, domain, root, response))


main()