#Homework 2: implementing a stateful network protocol

####Language agnostic edition!

This assignment will require you to write an implementation of a very simple
stateful network protocol in the language of your choice. You will implement
both the server and the client, and they will be expected both to speak the
protocol correctly to each other as well as to speak the protocol correctly
with our own reference implementation.

####WAR: A Card game

Hearthstone: Heroes of Warcraft is a cross-platform online card game with “war”
in the title. No matter whether using a Mac, PC, iOS, or Android device, anyone
can play the game with anyone else. The original card game [war](https://en.wikipedia.org/wiki/War_(card_game)), however, is much
simpler than that game (although probably not more popular). For this
assignment, we will be programming a cross-platform implementation of the “war”
card game, both the client and the server. If you implement the protocol
correctly, your code will be able to communicate with any other student’s code
regardless of the choice of language.

####WAR: The simplified rules

The simplified rules for our version of war are as follows: the dealer (server)
deals half of the deck, at random, to the two players (clients). Each player
“turns over” (sends) one of their cards to the server, and the server responds
to each player “win” “lose” or “draw.” Unlike normal war (as this class is
about network programming not videogame programming), in the event of a tie
neither player receives a “point” and play simply moves on to the next round.
After all of the cards have been used, play stops and each client knows (based
on the number of points they received) whether they won or they lost (hint:
rather than keeping track of 1 point for a win and 0 points for a draw or loss,
keep track of 1 for win, -1 for loss, and 0 for draw, and
positive/negative/zero score corresponds to win/lose/draw at the end of the
game).

####WAR version .1: The message format

For homework 1, all WAR game messages follow the WAR version .1 message format.
V .1 messages consist of a one byte “command” followed by either a one byte
payload or a 26 byte payload. The command values map as such:

| Command       | Value |
| ------------- |:-----:|
| want game     |   0   |
| game start    |   1   |
| play card     |   2   |
| play result   |   3   |

Within a play result message, the one byte payload values map as such:

| Result        | Value |
| ------------- |:-----:|
| win     |   0   |
| lose    |   1   |
| draw    |   2   |

For want game, play card, and play result, the payload is one byte long. For
the “want game” message, the “result” should always be the value 0. For the
“play result” message, the result values above.

For the “game start” message (where the payload is a set of 26 cards), the
payload is 26 bytes representing 26 cards. The byte representation of cards are
a mapping between each of the 52 cards in a standard deck to the integers
[0..51]. Mapping cards follows the suit order clubs, diamonds, hearts, spades,
and within each suit, the rank order by value (i.e. 2, 3, 4, … , 10, Jack,
Queen, King, Ace). Thus, 0, 1, and 2 map onto 2 of Clubs, 3 of Clubs, 4 of
Clubs; 11, 12, 13, and 14 map onto the King of Clubs, the Ace of Clubs, the 2
of Diamonds, and the 3 of Diamonds; and finally 49, 50, and 51 map onto the
Queen, King, and Ace of Spades. Note that you cannot compare card values
directly to determine the winner of a “war” - you’ll need to write a custom
comparator which maps two different card values onto win, lose, or draw.

When sending a “game start” message, the server sends half of the deck, at
random, to each player by sending 26 bytes with the values [0..51] to one
player and the remaining 26 to the other player.

When sending a “play card” message, the client sends one byte which represents
one of their cards. Which card to send is undefined, but you cannot send the
same card twice within the same game.

####WAR: the network protocol

Parallel to the simplified rules, the WAR protocol is as follows. A war server
listens for new TCP connections on a given port. It waits until two clients
have connected to that port. Once both have connected, the clients send a
message containing the “want game” command. If both clients do this correctly,
the server responds with a message containing the “game start” command, with a
payload containing the list of cards dealt to that client.

After each client has received their half of the deck, the clients send
messages including the “play card” message, and set the payload to their chosen
card. After the server has received a “play card” message from both clients, it
will respond with a “play result” message to both clients, telling each one
whether they won or lost. This process continues until each player has sent all
of their cards and received all of their play results; after receiving the last
play result, the clients disconnect; after sending the last play result, the
server also disconnects.

For War v.1, your server and client only need to play one game, and then exit.</p>

####Template

For this homework, as you can use whatever language you want, there is no
provided temlpate, only the game protocol. Feel free to test your
implementation against your friends’ implementation - as long as you aren’t
copying or looking at each other’s code, “playing against” each other is
totally allowed and encouraged.

####Hints / gotchas

You should write a test harness that verifies, at the very least, that your
message encoding and decoding methods work correctly. Whatever you do, do not
try to write the entire program without testing it along the way. A good rule
of thumb is that you should be able to test every 10 lines of code you write -
going any further than that risks wasting effort / causing debugging to take
way too long.

If you use one of the ‘global’ ipv6 addresses assigned to your virtual machine
to serve a war game, you can share that address with a friend and they will be
able to connect directly to your server as long as they correctly set up their
vpn during homework 1.

While the homework can be completed in any language, we can only guarantee that
we can provide help in C and python. In any other language we’ll try to help,
but provide no guarantees about being able to answer your questions.

Like homework 1, you need to keep your code IP version agnostic. If you
continue using getaddrinfo like in homework 1, this should not be exceedingly
difficult.

####Turn-in instructions

While this project allows you to use any langauge you want, you need to ensure
that we will be able to grade your submission on our class Ubuntu VM. If you
need to install the jvm, compile source files, or otehrwise prepare the
environment, you’ll need to provde a Makefile which will do so. You will also
provide a __play.sh__ script which we can run to start the code. __play.sh__ will
take three arguments:

```shell
./play.sh (client|server) [hostname] [portnumber]
```

when run with the __client__ argument, the code will connect to a war v.1 server
at __hostname:portnumber__ and execute the war v.1 protocol. When run with the
__server__ argument, it will listen for connections

####Grading

We will run your client and server against a reference implementation for the
server and clients. If at any time a client or server sends an incorrect
message, your code should exit with a non-zero return value. For instance, in C
you would use exit(1) for an error situation, and exit(0) for successful
operation.

Any output to stdout or stderr will not be considered - feel free to send
debugging output, the result of each war, etc, to the screen.

####Due date

This assignment is due __Friday, September 11__. You need to implement both the
client and the server for this assignment, so get started early.