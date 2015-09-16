import random
import string
import sys

from connect import *
from shared import *

class WarServer:
  def __init__(self, sockets):
    self.servers, self.clients = sockets
    self.sockets = self.servers + self.clients
  
    
  def play_init(self):
    """
    Initial state of game. 
    Waits for clients to send want game messages.
    """
    for i, client in enumerate(self.clients):
      command, payload = read_from_socket(client, 2)
      
      try:
        assert commands[command] == "WANT_GAME" and payload == ['\x00']
      except (KeyError, AssertionError):
        invalid_response(self.sockets, str(client.getpeername()))
  
  
  def play_ready(self):
    """
    Game is ready to play. 
    Both clients have sent want game.
    Server will send out cards to both players.
    """
    deck = range(0, 52)
    random.shuffle(deck)
    self.decks = [deck_to_bytearray(d) for d in (deck[:26], deck[26:])]
  
    for i, client in enumerate(self.clients):
      write_to_socket(client, commands["GAME_START"], 
                      string.join(self.decks[i], ''))
  
  
  def play_in_progress(self):
    """
    Game is in session.
    """
    for _ in xrange(0, 26):
      cards = [None, None]

      for i, client in enumerate(self.clients):
        command, card = read_from_socket(client, 2)
        
        try:
          assert commands[command] == "PLAY_CARD"
          cards[i] = card[0]
          self.validate_card(i, cards[i])
        except (KeyError, AssertionError):
          invalid_response(self.sockets, str(client.getpeername()))
      
      values = compare_cards(cards[0], cards[1])
      
      for i, client in enumerate(self.clients):
        write_to_socket(client, commands["PLAY_RESULT"], results[values[i]])
  
  
  def play_complete(self):
    """
    End of game has been reached without error.
    """
    print >> sys.stderr, "game finished."
    shutdown_sockets_and_exit(self.sockets, 0)
  
  
  def validate_card(self, deck_id, card):
    try:
      self.decks[deck_id].remove(card)
    except ValueError:
      print >> sys.stderr, str(self.clients[deck_id].getpeername()) + \
                           " played an invalid card: " + card
      shutdown_sockets_and_exit(self.sockets, 1)
  