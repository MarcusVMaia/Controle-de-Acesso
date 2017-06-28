#include "interface.h"


void faceDetect( Mat& img );
void eyeDetect(Mat& img, Rect faceAjustada);
Mat surfDetect(Mat img);
void posProcessing(Mat *img);
void separateEqualize(Mat *img);
int testFace(Rect face, Mat smallImg); //funcao que elimina ruido do detector, para evitar processamento do eigenfaces

