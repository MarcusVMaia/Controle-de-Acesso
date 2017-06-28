#ifndef RECOGNIZE_H
#define RECOGNIZE_H

#include "socket.h"


#define RECOGNIZE 1
#define CADASTRO  2
#define DELETE    3

extern string inputName;
extern string cascadeName;

extern VideoCapture capture;
extern Mat frame, frameCopy, face;
extern CascadeClassifier cascade, nestedCascade;
extern double scale;

extern int ESTADO;
extern int isFaceDetected;

extern Ptr<FaceRecognizer> model;

void recognizeFace(Mat);
void train();
void read_csv(const string& filename, vector<Mat>& images, vector<int>& labels);
void surfRecognition(Mat , Mat );

#endif

