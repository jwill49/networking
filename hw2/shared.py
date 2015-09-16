import sys
import connect

commands = {
  "WANT_GAME": '\x00',
  "GAME_START": '\x01',
  "PLAY_CARD": '\x02',
  "PLAY_RESULT": '\x03',
  0: "WANT_GAME",
  1: "GAME_START",
  2: "PLAY_CARD", 
  3: "PLAY_RESULT",
  '\x00': "WANT_GAME",
  '\x01': "GAME_START",
  '\x02': "PLAY_CARD",
  '\x03': "PLAY_RESULT"
}

results = {
  '\x00': 1,
  '\x01': -1,
  '\x02': 0,
  1: '\x00',
  -1: '\x01',
  0: '\x02'
}

def invalid_response(socks, source):
  print >> sys.stderr, "invalid response from: " + source
  connect.shutdown_sockets_and_exit(socks, 1)
  

def sign(val):
  if val == 0: return 0
  elif val < 0: return -1
  else: return 1
  

def compare_cards(p1, p2):
  p1, p2 = ord(p1)+13, ord(p2)+13
  diff = p1%13 - p2%13
  diff = sign(diff)
  return (diff, -1*diff)