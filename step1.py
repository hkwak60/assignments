import dns.query
import dns.resolver
from typing import Union,Optional,Dict,Any,List,Tuple

import contextlib,socket,time


def make_query(
    qname: Union[dns.name.Name, str],
    rdtype: Union[dns.rdatatype.RdataType, str],
    rdclass: Union[dns.rdataclass.RdataClass, str] = dns.rdataclass.IN,
    use_edns: Optional[Union[int, bool]] = None,
    want_dnssec: bool = False,
    ednsflags: Optional[int] = None,
    payload: Optional[int] = None,
    request_payload: Optional[int] = None,
    options: Optional[List[dns.edns.Option]] = None,
    idna_codec: Optional[dns.name.IDNACodec] = None,
    id: Optional[int] = None,
    flags: int = dns.flags.RD,
    pad: int = 0,
) -> dns.message.QueryMessage:
  if isinstance(qname, str):
      qname = dns.name.from_text(qname, idna_codec=idna_codec)
      rdtype = dns.rdatatype.RdataType.make(rdtype)
      rdclass = dns.rdataclass.RdataClass.make(rdclass)
      m = dns.message.QueryMessage(id=id)
      m.flags = dns.flags.Flag(flags)
      m.find_rrset(m.question, qname, rdclass, rdtype, create=True, force_unique=True)
      # only pass keywords on to use_edns if they have been set to a
      # non-None value.  Setting a field will turn EDNS on if it hasn't
      # been configured.
      kwargs: Dict[str, Any] = {}
      if ednsflags is not None:
          kwargs["ednsflags"] = ednsflags
      if payload is not None:
          kwargs["payload"] = payload
      if request_payload is not None:
          kwargs["request_payload"] = request_payload
      if options is not None:
          kwargs["options"] = options
      if kwargs and use_edns is None:
          use_edns = 0
      kwargs["edns"] = use_edns
      kwargs["pad"] = pad
      m.use_edns(**kwargs)
      m.want_dnssec(want_dnssec)
      return m
  #여기서부터 response!!!!
  #!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def _destination_and_source(
  where, port, source, source_port, where_must_be_address=True):
  # Apply defaults and compute destination and source tuples
  # suitable for use in connect(), sendto(), or bind().
  af = None
  destination = None
  try:
    af = dns.inet.af_for_address(where)
    destination = where
  except Exception:
    if where_must_be_address:
        raise
    # URLs are ok so eat the exception
  if source:
    saf = dns.inet.af_for_address(source)
    if af:
      # We know the destination af, so source had better agree!
      if saf != af:
        raise ValueError(
            "different address families for source and destination"
        )
    else:
      # We didn't know the destination af, but we know the source,
      # so that's our af.
      af = saf
  if source_port and not source:
    # Caller has specified a source_port but not an address, so we
    # need to return a source, and we need to use the appropriate
    # wildcard address as the address.
    try:
      source = dns.inet.any_for_af(af)
    except Exception:
      # we catch this and raise ValueError for backwards compatibility
      raise ValueError("source_port specified but address family is unknown")
  # Convert high-level (address, port) tuples into low-level address
  # tuples.
  if destination:
    destination = dns.inet.low_level_address_tuple((destination, port), af)
  if source:
    source = dns.inet.low_level_address_tuple((source, source_port), af)
  return (af, destination, source)

def _make_socket(af, type, source, ssl_context=None, server_hostname=None):
    s = socket.socket(af, type)
    try:
        s.setblocking(False)
        if source is not None:
            s.bind(source)
        if ssl_context:
            # LGTM gets a false positive here, as our default context is OK
            return ssl_context.wrap_socket(
                s,
                do_handshake_on_connect=False,  # lgtm[py/insecure-protocol]
                server_hostname=server_hostname,
            )
        else:
            return s
    except Exception:
        s.close()
        raise

def _compute_times(timeout):
    now = time.time()
    if timeout is None:
        return (now, None)
    else:
        return (now, now + timeout)
    

def udp(
  q: dns.message.Message,
  where: str,
  timeout: Optional[float] = None,
  port: int = 53,
  source: Optional[str] = None,
  source_port: int = 0,
  ignore_unexpected: bool = False,
  one_rr_per_rrset: bool = False,
  ignore_trailing: bool = False,
  raise_on_truncation: bool = False,
  sock: Optional[Any] = None,
  ignore_errors: bool = False,
) -> dns.message.Message:
  wire = q.to_wire()
  (af, destination, source) = _destination_and_source(
      where, port, source, source_port
  )
  (begin_time, expiration) = _compute_times(timeout)
  if sock:
      cm: contextlib.AbstractContextManager = contextlib.nullcontext(sock)
  else:
      cm = _make_socket(af, socket.SOCK_DGRAM, source)
  # with cm as s:
  #     send_udp(s, wire, destination, expiration)
  #     (r, received_time) = receive_udp(
  #         s,
  #         destination,
  #         expiration,
  #         ignore_unexpected,
  #         one_rr_per_rrset,
  #         q.keyring,
  #         q.mac,
  #         ignore_trailing,
  #         raise_on_truncation,
  #         ignore_errors,
  #         q,
  #     )
      # r.time = received_time - begin_time
      # We don't need to check q.is_response() if we are in ignore_errors mode
      # as receive_udp() will have checked it.
      return r

# 질의할 도메인 주소 입력
domain = 'google.com'

# 사용할 DNS Server 주소 입력
dns_server = '8.8.8.8'

# 도메인의 A record에 대한 DNS 쿼리 생성
query = make_query(domain, 'A')
#print(query)

# DNS 서버로 쿼리 전송 및 응답 받기
response = dns.query.udp(query, dns_server)

# 응답 출력
print(response)