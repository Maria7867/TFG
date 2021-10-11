//cliente TCP
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <iostream>
#include <fstream>
#include <string>
//

#define BUFFER_SIZE 256

void error(const char *msg){
    perror(msg);
    exit(0);
}
int send_image(int socket, char* imagen){

  FILE *picture;
  int size, read_size, stat, packet_index;
  char send_buffer[10240], read_buffer[256];
  packet_index = 1;

  picture = fopen(imagen, "r");


  if(picture == NULL) {
       printf("Error Opening Image File"); }

  fseek(picture, 0, SEEK_END);
  size = ftell(picture);
  fseek(picture, 0, SEEK_SET);


  //Send Picture Size
  write(socket, (void *)&size, sizeof(int));

  //Send Picture as Byte Array

  do { //Read while we get errors that are due to signals.
     stat=read(socket, &read_buffer , 255);
  } while (stat < 0);

  while(!feof(picture)) {
     //Read from the file into our send buffer
     read_size = fread(send_buffer, 1, sizeof(send_buffer)-1, picture);
     //Send data through our socket
     do{
       stat = write(socket, send_buffer, read_size);
     }while (stat < 0);

     packet_index++;

     //Zero out our send buffer
     bzero(send_buffer, sizeof(send_buffer));
    }
    return 0;
 }

int main(int argc, char *argv[]){
  int sockfd, port, n;
  struct sockaddr_in serv_addr;
  struct hostent *server;


  char buffer[256];
  if (argc < 3) {
    fprintf(stderr,"usage %s hostname port\n", argv[0]);
    exit(0);
  }

  port = atoi(argv[2]);//coge el puerto del argumento y lo pasa a int
  sockfd = socket(AF_INET, SOCK_STREAM, 0);//AF_INET= IPv4, SOCK_STREAM=TCP, 0=IP (internet protocol)
  if (sockfd < 0)
    error("ERROR opening socket");
  server = gethostbyname(argv[1]); //coge el nombre del host del argumento y lo convierte en una dierccion IP
  if (server == NULL) {
    fprintf(stderr,"ERROR, no such host\n");
    exit(0);
  }
  // CLEAR ADDRESS STRUCTURE
  bzero((char *) &serv_addr, sizeof(serv_addr));
  // server byte order
  serv_addr.sin_family = AF_INET;
  bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);//¿¿¿¿¿Copia en la estructura hostent creada (server) los valores ?????
  //convert short integer value for port must be converted into network byte order
  serv_addr.sin_port = htons(port);

  if (connect(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
    error("ERROR connecting");
  //printf("Please enter the message: ");
  //pone el buffer a 0
  bzero(buffer,256);
  //lee lo escrito en la terminal
  //fgets(buffer,255,stdin);

  //const char *pathname = buffer;
  /*std::string div = argv[3];
  std::string delimiter = ".";
  std::string token =div.substr(0,div.find(delimiter));

  printf("wtf: %s\n", argv[3]);
  //printf("tokendiv: %d\n", div);
  printf("token1: %d\n", token[0]);
  printf("token2: %d\n", token[1]);
*/
  std::string filepath;
  char* data = argv[3];
  int size = strlen(data);
  filepath.assign(data, size);

  if(filepath.substr(filepath.find_last_of(".") + 1) == "txt") {
    std::cout << "Yes..." << std::endl;
    FILE *fd = fopen(argv[3], "rb");
    if (fd==NULL){
      printf("ERROR\n");
    }
    size_t rret, wret;
    int bytes_read;
    while (!feof(fd)) {
        if ((bytes_read = fread(&buffer, 1, BUFFER_SIZE, fd)) > 0)
            send(sockfd, buffer, bytes_read, 0);
        else
            break;
    }
    fclose(fd);
  }
  if(filepath.substr(filepath.find_last_of(".") + 1) == "jpeg") {
    send_image(sockfd, argv[3]);
  }



  //escribe lo leido de la terminal en el socket
  /*n = write(sockfd, buffer, strlen(buffer));
  if (n < 0)
    error("ERROR writing to socket");*/
  //se vuelve a poner el buffer a 0
  bzero(buffer,256);
  //se lee el socket
  n = read(sockfd, buffer, 255);
  if (n < 0)
    error("ERROR reading from socket");
  printf("%s\n", buffer);

  close(sockfd);
  return 0;
}
