#include "socket.h"

int sockfd1;
int bytes1;
socklen_t length1;
char recv_buffer1[32];
struct sockaddr_in server1; //declara servidor

void clientConnection(){

    //cria socket
    sockfd1 = socket(AF_INET, SOCK_STREAM, 0);
    struct timeval tv;
    tv.tv_sec = 0;  /* 30 Secs Timeout */
    tv.tv_usec = 100;  // Not init'ing this can cause strange errors
    setsockopt(sockfd1, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv,sizeof(struct timeval));
    if(sockfd1 < 0)
    {
        perror("client_sockfd:::");
        exit(1);
    }

    //parametros de conexão com servidor
    server1.sin_family  =  AF_INET;
    server1.sin_port    =  htons(5005);
    server1.sin_addr.s_addr  =  inet_addr("127.0.0.1");
    memset(&(server1.sin_zero), 0x00, 8);


    //conectando-se ao servidor
    length1 = sizeof(struct sockaddr);
    while(connect(sockfd1, (struct sockaddr *)&server1, length1) < 0)
    {
        perror("client_connect:::");
        //close(sockfd1);
        //return;
    }
    cout << "Conexao com server estabelicida" << endl;
}

int receiveServer(){
    //recebe do servidor
    bytes1 = recv(sockfd1, recv_buffer1, 32, 0);

    //servidor fechou a conexão ou ocorreu um erro
    if(bytes1 <= 0)//ocorreu um erro = -1, fechou conexão = 0
    {
        //perror("client_recv:::");
        //close(sockfd1);

        //cout << "Nada recebido" << endl;
        return 0;
    }

    //supondo que não ocorreu um erro acima
    recv_buffer1[bytes1] = 0x00;//ponha o caractere '{FONTE}'

    if (!strcmp(recv_buffer1,"ok")){
        return 1; //fazer reconhecimento
    }
    else {
        return 0;
    }
}

void sendData(string data){

    cout << data << endl;

    while (send(sockfd1, data.c_str(), data.size(), 0) < 0);

//    if(bytes1 < 0)
//    {
//        perror("client_send:::");
//        close(sockfd1);
//        return;
//    }
}

void closeConnection(){
    close(sockfd1);
}
