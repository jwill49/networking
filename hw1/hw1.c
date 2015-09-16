/* 

   Minimal TCP client example. The client connects to port 8080 on the 
   local machine and prints up to 255 received characters to the console, 
   then exits. To test it, try running a minimal server like this on your
   local machine:

   echo "Here is a message" | nc -l -6 8080

*/


#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>

#define BUFSZ 255

int main(int argc, char** argv) 
{	
  /* inpsired heavily by man 3 getaddrinfo 
  */
  
  char host[BUFSZ], resource[BUFSZ], protocol[BUFSZ], filename[BUFSZ];
  struct addrinfo hints;
  struct addrinfo * result, * rp;
  int sock_fd, s;

  memset(&host, 0, BUFSZ);
  memset(&protocol, 0, BUFSZ);
  memset(&resource, 0, BUFSZ);
  memset(&filename, 0, BUFSZ);
  memset(&hints,0,sizeof(struct addrinfo));
  hints.ai_socktype = SOCK_STREAM;
  
  // Retrieve command line args
  if( argc < 2 ) {
    fprintf(stderr, "usage: hw1 link\n");
    exit(1);
  }
  char *host_start;
  if((host_start = strstr(argv[1], "//")) == NULL) {
    // TODO: Not a very robust test for invalid host...
    fprintf(stderr, "Invalid hostname\n");
    exit(1);
  }
  
  // Get protocol
  int protocol_len = strlen(argv[1]) - strlen(host_start) - 1; // remove colon
  strncpy(protocol, argv[1], protocol_len);
  
  // Get host + resource
  strcpy(host, host_start+2);
  char *resource_start = strstr(host, "/");
  
  // Default to root if no resource requested
  if(resource_start == NULL || strcmp(resource, "/") == 0) {
    strcpy(resource, "/");
    strcpy(filename, "index.html");
  }
  
  else {
    strcpy(resource, resource_start);
    int host_length = strlen(host) - strlen(resource);
    host[host_length] = '\0';
    strcpy(filename, (char*) strrchr(resource, '/') + 1);
    
    if(filename[0] == '\0')
      strcpy(filename, "index.html");
  }
  
  printf("Connecting to: %s  %s\n", host, resource);
  
  // Resolve address info
  if ((s = getaddrinfo(host, protocol, &hints, &result)) != 0){
    fprintf(stderr, "ERROR: %s\n", gai_strerror(s));
    exit(1);
  }
  
  // Connect
  for (rp = result; rp != NULL; rp = rp->ai_next) {
    sock_fd = socket(rp->ai_family, rp->ai_socktype,
        rp->ai_protocol);
    if (sock_fd == -1)
      continue;

    if (connect(sock_fd, rp->ai_addr, rp->ai_addrlen) != -1)
      break; /* Success */

    close(sock_fd);
  }

  if (rp == NULL) {
    fprintf(stderr, "could not connect\n");
    exit(1);
  }

  freeaddrinfo(result);
  
  char query[BUFSZ];
  memset(query, 0, sizeof(query));
  sprintf(query,
      "GET %s HTTP/1.0\r\nHost: %s\r\n\r\n",
      resource,
      host);

  // Send query
  write(sock_fd, query, strlen(query));
  
  // Create buffer and file for response
  char *buf = (char *) calloc(BUFSZ+1, sizeof(char));
  char *buf2 = (char *) calloc(BUFSZ+1, sizeof(char));

  // Process response
  int recv_count = recv(sock_fd, buf, BUFSZ, 0);
  if(recv_count == -1) {
    fprintf(stderr, "Error: receive failed\n");
    exit(1);
  }
  
  if(strstr(buf, "200 OK") == NULL) {
    fprintf(stderr, "Error: response is not 200\n");
    exit(1);
  }
  
  FILE *output = fopen(filename, "w");
  int output_fd = fileno(output);
  char *response = NULL;
  char *curr = buf;
  char *prev = buf2;
  int response_len = 0;
  
  do {
    // Found "...\r\n\r\n..."
    if((response = strstr(curr, "\r\n\r\n")) != NULL) {
      response += 4;
      response_len = BUFSZ - (response - curr);
      break;
    }
    
    // First time around
    if(prev == NULL)
      continue;
    
    else {
      prev = curr;
      if((recv_count = recv(sock_fd, curr, BUFSZ, 0)) < 1) {
        fprintf(stderr, "Error: end of transmission reached without EOH\n");
        exit(1);
      }
      
      // Found "...\r\n\r" + "\n..."
      if(curr[0] == '\n' && prev[BUFSZ-3] == '\r' && 
         prev[BUFSZ-2] == '\n' && prev[BUFSZ-1] == '\r')
      {
        response = curr + 1;
        response_len = BUFSZ - 1;
        break;
      }
      
      // Found "...\r\n" + "\r\n..."
      if(curr[0] == '\r' && curr[1] == '\n' && 
         prev[BUFSZ-2] == '\r' && prev[BUFSZ-1] == '\n')
      {
        response = curr + 2;
        response_len = BUFSZ - 2;
        break;
      }
      // Found "...\r" + "\n\r\n..."
      if(curr[0] == '\n' && curr[1] == '\r' && 
         curr[2] == '\n' && prev[BUFSZ-1] == '\r')
      {
        response = curr + 3;
        response_len = BUFSZ - 3;
        break;
      }
    }
  } while(response == NULL);
  
  write(output_fd, response, response_len);
  
  while((recv_count = recv(sock_fd, buf, BUFSZ, 0)) > 0)
    write(output_fd, buf, recv_count);
  
  if(recv_count == -1) {
    fprintf(stderr, "Receive failed\n");
    exit(1);
  }
  
  printf("Downloaded %s\n", filename);
  shutdown(sock_fd,SHUT_RDWR);
  exit(0);
}
