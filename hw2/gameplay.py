import sys
import struct
import random
import string

from WarServer import WarServer
from WarClient import WarClient
from connect import *


def play_war(entity):
  entity.play_init()
  entity.play_ready()
  entity.play_in_progress()
  entity.play_complete()


def print_usage(errno):
  print >> sys.stderr, "usage: ./play.sh (client|server) [hostname] [portnumber]"
  exit(errno)


def main():
  if (len(sys.argv) != 4):
    print_usage(1)
  
  mode, host, port = sys.argv[1], sys.argv[2], int(sys.argv[3])
  
  if(mode == "server"):
    entity = WarServer(create_server(host, port))
  elif(mode == "client"):
    entity = WarClient(join_server(host, port))
  else:
    print_usage(1)
    
  play_war(entity)


if __name__ == '__main__':
  main()