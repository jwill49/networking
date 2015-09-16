import string
import sys

from connect import *
from shared import *

class WarClient:
  def __init__(self, sock):
    self.server = sock
    self.score = 0
    
  
  def play_init(self):
    """
    Initial state of game. 
    Sends want game message to server.
    """
    write_to_socket(self.server, commands["WANT_GAME"], '\x00')
  
  
  def play_ready(self):
    """
    Game is ready to play.
    Receive cards from server
    """
    command, payload = read_from_socket(self.server, 27)
  
    try:
      assert commands[command] == "GAME_START"
      self.deck = payload
    except (KeyError, AssertionError):
      invalid_response(self.server, "server")
      
      
  def play_in_progress(self):
    """
    Play is in progress
    """
    while self.deck:
      write_to_socket(self.server, commands["PLAY_CARD"], self.deck.pop())
      command, payload = read_from_socket(self.server, 2)
  
      try:
        assert commands[command] == "PLAY_RESULT"
        self.score += results[payload[0]]
      except (KeyError, AssertionError):
        invalid_response(self.server, "server")
  
  
  def play_complete(self):
    print >> sys.stderr, "score: " + str(self.score) + "\ngame over."
    shutdown_sockets_and_exit(self.server, 0)
    