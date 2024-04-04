import dns.message
import dns.rdatatype
import dns.query
import dns.exception
import time
from datetime import datetime


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

def mydig(q:dns.message.QueryMessage, d, addr, res:dns.message.QueryMessage, root):
    while(len(res.answer)==0):
        if(len(res.additional)==0):
            if(res.authority[0][0].rdtype==dns.rdatatype.SOA):
                d=res.authority[0][0].mname
            else:
                d = res.authority[0][0].target
            q = dns.message.make_query(d,res.authority[0][0].rdtype)
            res = dns.query.udp(q, root, timeout=2)
        else:
            q = dns.message.make_query(d, dns.rdatatype.A)
            addr = get_ip_from_additional(res)
            res = dns.query.udp(q, addr, timeout=2)
    while(True):
        if(len(res.answer)!=0):
            if(res.answer[0][0].rdtype==dns.rdatatype.A):
                return res
            else:
                d = res.answer[0][0].target
                q = dns.message.make_query(d, res.answer[0][0].rdtype)
                res = dns.query.udp(q, root, timeout=2)
        if(len(res.additional)==0):
            if(res.authority[0][0].rdtype==dns.rdatatype.SOA):
                d=res.authority[0][0].mname
            else:
                d = res.authority[0][0].target
            q = dns.message.make_query(d,res.authority[0][0].rdtype)
            res = dns.query.udp(q, root, timeout=2)
        else:
            q = dns.message.make_query(d, dns.rdatatype.A)
            addr = get_ip_from_additional(res)
            res = dns.query.udp(q, addr, timeout=2)

def print_result(q, res:dns.message.QueryMessage, delay, current:datetime):
    print("Question Section: \n"+q+"\t\t\tIN\tA\n")
    index = 0
    print("Answer Section:")
    while(index<len(res.answer[0])):
        print(q+"\t\t"+str(res.answer[0].ttl)+"\tIN\tA\t"+str(res.answer[0][index].address))
        index+=1
    print("Query time: "+str(int(delay*1000))+"msec")
    print("WHEN: "+current.strftime("%a %b %d %H:%M:%S KST %Z %Y"))




def main():
    domain = input("Input domain: ")
    start = time.time()
    current = datetime.now()
    query = dns.message.make_query(domain, dns.rdatatype.A)
    root = '198.41.0.4'
    response = dns.query.udp(query, root, timeout = 2)
    if(response.rcode()!=0):
        print("Wrong Domain Name!")
    else:
        response = mydig(query, domain, root, response, root)
        end=time.time()
        delay = end-start
        print_result(domain,response, delay, current)

main()