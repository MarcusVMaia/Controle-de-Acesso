#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>

//struct sockaddr_in, htons() e outras
#include <netinet/in.h>
//funções inet_*()
#include <arpa/inet.h>

#include <errno.h> /*perror()*/
#include <unistd.h> /*close()*/

#include <cctype>
#include <iostream>
#include <iterator>
#include <stdio.h>
#include <fstream>
#include <sstream>
#include <sys/stat.h>
#include "opencv2/opencv.hpp"
#include "opencv2/nonfree/nonfree.hpp"

using namespace std;
using namespace cv;

void clientConnection();
int receiveServer();
void sendData(string);
void closeConnection();
