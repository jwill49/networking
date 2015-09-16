import sys
import socket
import time
import struct
import array
import string
import select
import collections

from sys import stdin


def deck_to_bytearray(deck):
  return [struct.pack('B', card) for card in deck]


def str_bytestring(bstring):
  try:
    return str([hex(ord(b)) for b in bstring])
  except TypeError:
    return ""


def write_to_socket(sock, command, payload):
  """
  Writes to a socket using WAR Protocol.
  """
  message = str(command) + str(payload)
  print >> sys.stderr, str(sock.getsockname()) + " to " + \
                       str(sock.getpeername()) + ": " + \
                       str_bytestring(message)
                       
  sock.sendall(message)


def read_from_socket(sock, size):
  """
  Read size bytes from a socket.
  Return format is in WAR Protocol.
  """
  total_read = 0
  message = []
  
  while total_read < size:
    byte = sock.recv(1)
    message.append(byte)
    total_read += 1
  
  print message
  
  return (message[0], message[1:])


def join_server(host, port):
  """
  Connects to a IPv6 server on the given port.
  """
  client = None
  
  for res in socket.getaddrinfo(host, port, socket.AF_INET6, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
      print "Attempting to connect to WAR server at: " + str(sa)
      client = socket.socket(af, socktype, proto)
    except socket.error:
      client = None
      continue
    try:
      client.connect(sa)
      
    except socket.error, msg:
      client.close()
      client = None
  if client is not None:
    return client
  else:
    print >> sys.stderr, "could not open socket."
    shutdown_sockets_and_exit([], 1)


def create_server(host, port):
  """
  Creates a IPv6 server on the given port.
  """
  clients = []
  servers = []
  
  print >> sys.stderr, "WAR server starting up"
  
  for res in socket.getaddrinfo(None, port, socket.AF_INET6, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
      server = socket.socket(af, socktype, proto)
      server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error:
      server = None
      continue
    try:
      server.bind(sa)
      server.listen(2)
    except socket.error:
      server.close()
      server = None
  if server is not None:
    servers.append(server)
    while len(clients) < 2:
      print >> sys.stderr, "waiting for player " + str(len(clients) + 1)
      client, client_address = server.accept()
      clients.append(client)
      print >> sys.stderr, str(client_address) + " connected"
    return (servers, clients)
  else:
    print >> sys.stderr, "Failure launching WAR server.\n"
    shutdown_sockets_and_exit(servers + clients, 1)
  
  # try:
  #   server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
  #   server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  #   server.bind(('',port))
  #   server.listen(2)
  #   servers.append(server)
  #   input = [server, sys.stdin]
  #
  #   while len(clients) < 2:
  #     print >> sys.stderr, "waiting for player " + str(len(clients) + 1)
  #     inputready, outputready, exceptready = select.select(input,[],[])
  #
  #     for s in inputready:
  #       if s == server:
  #         client, client_address = server.accept()
  #         clients.append(client)
  #         print >> sys.stderr, str(client_address) + " connected"
  #       elif s != sys.stdin:
  #         s.close()
  #   return (servers, clients)
  # except Exception, e:
  #   print >> sys.stderr, "Failure launching WAR server.\n" + str(e)
  #   shutdown_sockets_and_exit(servers + clients, 1)


def shutdown_sockets_and_exit(socks, errno):
  print >> sys.stderr, "shutting down sockets"
  
  try:
    for sock in socks:
      sock.close()
  except TypeError:
    socks.close()
      
  exit(errno)
  