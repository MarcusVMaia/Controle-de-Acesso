#include "recognize.h"

void help();
int checkExecution(int argc,const char **argv);
void StartDraw(Mat image);
void AddPerson(String FolderName);
void AddPhoto(String photoname);
void mouse_callback(int event, int x, int y, int, void * img);
void DeletePerson();
