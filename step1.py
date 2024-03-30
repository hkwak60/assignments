import socket

port = 53
ip = '172.16.88.192'

#AF_INET: ipv4, SOCK_DGRAM: udp
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip,port))

while 1: 
  data, addr = sock.recvfrom(512)
  print(data)