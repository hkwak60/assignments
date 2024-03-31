import dns.query
import dns.resolver

# 질의할 도메인 주소 입력
domain = 'google.com'

# 사용할 DNS Server 주소 입력
dns_server = '8.8.8.8'

# 도메인의 A record에 대한 DNS 쿼리 생성
query = dns.message.make_query(domain, 'A')
#print(query)

# DNS 서버로 쿼리 전송 및 응답 받기
response = dns.query.udp(query, dns_server)

# 응답 출력
print(response)