import dns.message
import dns.rdatatype
import dns.query
import dns.exception

domain = input("Input domain: ")
query = dns.message.make_query(domain, dns.rdatatype.A)
root = '198.41.0.4'
response = dns.query.udp(query, root, timeout = 2)

def get_ip_from_additional(res: dns.message.QueryMessage):
    index = 0
    while(res.additional[index].rdtype!=1):
        index+=1
    return res.additional[index][0].address

while len(response.answer)==0:
    # if(response.additional[0].rdtype!=1):
    #     addr = response.additional[1][0].address
    # else:
    #     addr = response.additional[0][0].address
    addr = get_ip_from_additional(response)
    response = dns.query.udp(query, addr, timeout = 2)

if(response.answer[0][0].rdtype==dns.rdatatype.CNAME):
    domain = response.answer[0][0].__str__()
    query = dns.message.make_query(domain, dns.rdatatype.CNAME)
    response = dns.query.udp(query, root, timeout = 2)
    while len(response.answer)==0:
        query = dns.message.make_query(domain, dns.rdatatype.A)
        addr = response.additional[0][0].address
        response = dns.query.udp(query, addr, timeout = 2)


print(response)
