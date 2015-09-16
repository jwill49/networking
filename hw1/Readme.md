#The Programming Part!
For this week’s programming exercise, we will create a barebones web client (think wget). Based on the example tcp client code in the hw1 in the public repository, and the HTTP example sessions shown in class, you will write a command-line program called hw1 that takes a URL as its only parameter, retrieves the indicated file, and stores it in the local directory with the appropriate filename. If the URL does not end in a filename, your program should automatically request the file ‘index.html’. Make sure it works for both text and images by opening the stored file in a web browser.

You may assume that the URL is on the form http://host/path, where path may or may not be an empty string, may or may not contain multiple slashes (for subdirectories), and may or may not contain a file name. You may assume files to be no larger than one megabyte, and you are not expected to follow any HTTP redirect (3xx); your code can simply exit without saving any file.

The hostname may be a name like www.google.com, but the example code requires an ip address (like 64:ff9b::83c1:201d). To look up the IP address of a given host name, use getaddrinfo(). man 3 getaddrinfo on the command line will give you the details, or use this link, and see the getaddrinfo.c example.

####Template

For this homework, there is a prepared skeleton directory that you may use located in the public git repository.

####A few hints

Use http version 1.0. Version 1.1 can get a lot more complicated.
Good functions to use for handling filenames and text include sprintf, sscanf, strstr, strchr.
Section 2.2.2-2.2.3 in the book should also be helpful. Your book talks about the “request line” and “header lines” for an HTTP request. You will only need to use the request line and the host line of the header.
Read more about these using the man pages. For example, try man sprintf on the command line.

A “newline” in http consists of two ascii characters: __\r\n, not just \n__.

Your program will be tested (at least) on these urls:

http://www.google.com/
http://www.google.com/intl/en_ALL/images/logo.gif
http://www.google.com/thispagedoesnotexist
http://www.thissitedoesnotexist1776.com 
http://www.engadget.com/2010/08/27/amazon-kindle-review
http://www.engadget.com/2010/08/27/amazon-kindle-review/
Make sure you handle all these cases gracefully. If you don’t send a host
header, the first should produce a file index.html, the second the google logo saved into the file logo.gif, and the rest should produce an error because they do not give you a 200 OK response; you can thus quit your program by calling exit(1). Beej’s Guide to Network Programming is a great resource you may want to make use of.

If you’re curious, try firing up Wireshark, and then fetching the URL with wget or curl. You’ll find the request they sent (which may have a lot of additional parameters in it) in one of the packets with destination port 80.

Spend some time thinking about how to do the string manipulation. It does not have to be complicated. The complete program, including comments, error handling etc. can be written in about 100 leisurely lines.
####Turn-in instructions
For your turn-in, prepare a Makefile that compiles the hw1 target. To make sure your submission is complete, try the following in a temporary directory, i.e. create and change into a temporary directory under the /tmp filesystem:

```shell
./hw1 http://www.google.com/index.html 
```
This process should produce a file called index.html in the current working directory, containing the source for the google front page.

```shell
./hw1 http://www.google.com/intl/en_ALL/images/logo.gif 
```
Running this line should produce a file called logo.gif, containing the google logo.

####Grading

Grading will be done automatically using a script. We will publish this script after grading has completed; you are responsible for writing your own test cases. If you wish, you can share test cases you have written with the class. Students who share test cases publicly will very likely receive extra participation credit.

####Due Date
This assignment is due Wednesday, September 2nd, at 3pm. See the syllabus for the late turnin policy. This assignment is worth just as much as every other homework, so getting as much credit on it as possible is important (don’t turn in late!).