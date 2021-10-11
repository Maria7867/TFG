//servidor TCP
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define BUFFER_SIZE 256
//To run this code ./server #puerto (e.g 80)

void error(const char *msg){
  perror(msg);
  exit(1);
}
int receive_image(int socket){

  int buffersize = 0, recv_size = 0,size = 0, read_size, write_size, packet_index =1,stat;

  char imagearray[10241],verify = '1';
  FILE *image;

  //Find the size of the image
  do{
  stat = read(socket, &size, sizeof(int));
  }while(stat<0);

  char buffer[] = "Got it";

  //Send our verification signal
  do{
  stat = write(socket, &buffer, sizeof(int));
  }while(stat<0);

  image = fopen("crecibido.jpeg", "w");

  if( image == NULL) {
  printf("Error has occurred. Image file could not be opened\n");
  return -1;
}

  //Loop while we have not received the entire file yet
  int need_exit = 0;
  struct timeval timeout = {10,0};

  fd_set fds;
  int buffer_fd, buffer_out;

  while(recv_size < size) {
      FD_ZERO(&fds);
      FD_SET(socket,&fds);

      buffer_fd = select(FD_SETSIZE,&fds,NULL,NULL,&timeout);

      if (buffer_fd < 0)
         printf("error: bad file descriptor set.\n");

      if (buffer_fd == 0)
         printf("error: buffer read timeout expired.\n");

      if (buffer_fd > 0)
      {
          do{
                 read_size = read(socket,imagearray, 10241);
              }while(read_size <0);
          //Write the currently read data into our image file
           write_size = fwrite(imagearray,1,read_size, image);

               if(read_size !=write_size) {
                   printf("error in read write\n");    }


               //Increment the total number of bytes read
               recv_size += read_size;
               packet_index++;
      }

  }


    fclose(image);
    printf("Image successfully Received!\n");
    return 0;
  }


int main(int argc, char *argv[]){
  int sockfd, newsockfd, port;
  socklen_t cli_len;
  char buffer[256];
  struct sockaddr_in serv_addr, cli_addr;
  int n;
  bool received = false;
  if (argc < 2) {
     fprintf(stderr,"ERROR, no port provided\n");
     exit(1);
  }

  // CREAT A SOCKET
  // socket(int domain, int type, int protocol)
  sockfd =  socket(AF_INET, SOCK_STREAM, 0); //AF_INET= IPv4, SOCK_STREAM=TCP, 0=IP (internet protocol)
  if (sockfd < 0)
    error("ERROR opening socket");
 // CLEAR ADDRESS STRUCTURE
 bzero((char *) &serv_addr, sizeof(serv_addr));// ¿¿¿para evitar el error de address already in use???
 port = atoi(argv[1]);//coge el puerto del argumento y lo pasa a int

 /* SETUP THE host_addr STRUCTURE FOR USE IN BIND CALL*/
 // server byte order
 serv_addr.sin_family = AF_INET;
 // automatically be filled with current host's IP address
 serv_addr.sin_addr.s_addr = INADDR_ANY;
 // convert short integer value for port must be converted into network byte order
 serv_addr.sin_port = htons(port);

 // bind(int fd, struct sockaddr *local_addr, socklen_t addr_length)
 // bind() passes file descriptor, the address structure, and the length of the address structure
 // This bind() call will bind  the socket to the current IP address on port, portno
 if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
          error("ERROR on binding");
 //LISTEN
 // This listen() call tells the socket to listen to the incoming connections.
 // The listen() function places all incoming connection into a backlog queuen until accept() call accepts the connection.
 // Here, we set the maximum size for the backlog queue to 5.
 listen(sockfd,5);

 //ACCEPT
 // The accept() call actually accepts an incoming connection
 cli_len = sizeof(cli_addr);

// This accept() function will write the connecting client's address info into the the address structure and the size of that structure is cli_len.
// The accept() returns a new socket file descriptor for the accepted connection. So, the original socket file descriptor can continue to be used
// for accepting new connections while the new socker file descriptor is used for communicating with the connected client.
newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &cli_len);
if (newsockfd < 0)
  error("ERROR on accept");

printf("server: got connection\n");

//ESTA PARTE DE AQUÍ TENGO QUE REVISAR QUE HACE Y A LO MEJOR CAMBIARLA PARA QUE HAGA OTRA COSA, porque creo que solo envía el mensaje de hello world
// This send() function sends the 13 bytes of the string to the new socket

send(newsockfd, "sent\n", 13, 0);

FILE* fd = fopen("recibido.txt", "wb");
int datasize = recv(newsockfd, buffer, sizeof(buffer), 0);
fwrite(&buffer, 1, datasize, fd);
fclose(fd);
receive_image(newsockfd);

bzero(buffer,256); //deja el buffer a 0, es decir, limpia el buffer


close(newsockfd);
close(sockfd);
return 0;

}
