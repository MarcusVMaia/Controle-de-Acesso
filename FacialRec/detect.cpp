#include "detect.h"


int testFace(Rect face, Mat smallImg){

    static int MAX_X = 0, MAX_Y = 0, MIN_X = 0, MIN_Y = 0, qtd = 0, ok = 0;
    int dist = 20;
    int samePlaceCont = 2; //a quantidade de faces no mesmo lugar é o dobro desse valor
    if (face.x < MAX_X && face.x > MIN_X &&
            face.y < MAX_Y && face.y > MIN_Y){
        ok++;
        qtd = 0;
    }
    else{
        if (qtd > samePlaceCont) {
            MAX_X = face.x + dist;
            MIN_X = face.x - dist;
            MAX_Y = face.y + dist;
            MIN_Y = face.y - dist;
            ok = 0;
            qtd = 0;
        }
        else{
            qtd++;
        }
    }

    if ( ok > samePlaceCont){

        //ajuste do retangulo da face
        //        int ajuste = 10;
        //        face.x = face.x + 0.6*ajuste;
        //        face.y = face.y - 2*ajuste;
        //        face.width = face.width - 0.8*ajuste;
        //        face.height = face.height + 2.5*ajuste;
        //        rectangle( smallImg, face, Scalar(0,0,255),1,8,0);

        return 1; //face detected
    }
    return 0; //face not detected
}

void separateEqualize(Mat *img){
    Mat all = *img,left, right;
    int w = img->cols;
    int h = img->rows;
    int midX = w/2;

    left = all(Rect(0,0, midX,h));
    right = all(Rect(midX,0, w-midX,h));

    //equalizacao
    equalizeHist(*img,all);
    equalizeHist(left, left);
    equalizeHist(right, right);

    for (int y=0; y<h; y++) {
        for (int x=0; x<w; x++) {
            int v;
            if (x < w/4) {
                // Left 25%: just use the left face.
                v = left.at<uchar>(y,x);
            }
            else if (x < w*2/4) {
                // Mid-left 25%: blend the left face & whole face.
                int lv = left.at<uchar>(y,x);
                int wv = all.at<uchar>(y,x);
                // Blend more of the whole face as it moves
                // further right along the face.
                float f = (x - w*1/4) / (float)(w/4);
                v = cvRound((1.0f - f) * lv + (f) * wv);
            }
            else if (x < w*3/4) {
                // Mid-right 25%: blend right face & whole face.
                int rv = right.at<uchar>(y,x-midX);
                int wv = all.at<uchar>(y,x);
                // Blend more of the right-side face as it moves
                // further right along the face.
                float f = (x - w*2/4) / (float)(w/4);
                v = cvRound((1.0f - f) * wv + (f) * rv);
            }
            else {
                // Right 25%: just use the right face.
                v = right.at<uchar>(y,x-midX);
            }
            img->at<uchar>(y,x) = v;
        }// end x loop
    }//end y loop
}

void posProcessing(Mat *img){

    //separateEqualize(img);

    //filtro
    Mat filtered;
    bilateralFilter(*img, filtered, 0, 20.0, 2.0);


    //elipse
    Mat mask = Mat(filtered.size(), CV_8UC1, Scalar(255));
    double dw = filtered.cols- 7.5;
    double dh = filtered.rows -7.5 ;
    Point faceCenter = Point( cvRound(2.5 + dw * 0.5),
                              cvRound(2.5 + dh * 0.4) );
    Size size = Size( cvRound(dw * 0.5), cvRound(dh * 0.8) );
    ellipse(mask, faceCenter, size, 0, 0, 360, Scalar(0),-1);
    filtered.setTo(Scalar(128), mask);

    *img = filtered;
}

Mat surfDetect(Mat img){

    //Detectores
    vector<cv::KeyPoint> keys;
    cv::SurfFeatureDetector surf(250);
    surf.detect(img,keys);

    //Descritores
    cv::SurfDescriptorExtractor surfDesc;
    cv::Mat Surfdescriptors;
    surfDesc.compute(img,keys,Surfdescriptors);

    Mat aux;
    drawKeypoints(img,keys,aux);
    return aux;

    //return Surfdescriptors;

}

void eyeDetect(Mat &img, Rect faceAjustada){

    vector<Rect> eyes;

    Mat olhos = img(faceAjustada);
    imshow("olho", olhos);
    nestedCascade.detectMultiScale(olhos, eyes,
                                   1.1, 2, 0
                                   //|CV_HAAR_FIND_BIGGEST_OBJECT
                                   //|CV_HAAR_DO_ROUGH_SEARCH
                                   |CV_HAAR_SCALE_IMAGE
                                   ,
                                   Size(10, 10) );

    for(int ii = 0; ii < eyes.size() ; ii++){
        rectangle( olhos, Point(eyes[ii].x, eyes[ii].y),
                   Point(eyes[ii].x + eyes[ii].width-1, eyes[ii].y + eyes[ii].height-1),
                   Scalar(0,0,255), 3, 8, 0);
    }
}

void faceDetect( Mat& img )
{
    double t = 0;
    vector<Rect> faces;

    Mat gray, smallImg( cvRound (img.rows/scale), cvRound(img.cols/scale), CV_8UC1 );

    cvtColor( img, gray, CV_BGR2GRAY );
    resize( gray, smallImg, smallImg.size(), 0, 0, INTER_LINEAR );
    equalizeHist( smallImg, smallImg );

    t = (double)cvGetTickCount();
    cascade.detectMultiScale( smallImg, faces,
                              1.1, 2, 0
                              //|CV_HAAR_FIND_BIGGEST_OBJECT
                              //|CV_HAAR_DO_ROUGH_SEARCH
                              |CV_HAAR_SCALE_IMAGE
                              ,
                              Size(30, 30) );

    t = (double)cvGetTickCount() - t;
    printf( "detection time = %g ms\n", t/((double)cvGetTickFrequency()*1000.) );

    //so processa se for detectada uma face (condicao de contorno)
    if (faces.size() == 1 && testFace(faces[0], smallImg)){

        //debug
        //        rectangle( img, cvPoint(cvRound(faces[0].x*scale), cvRound(faces[0].y*scale)),
        //                cvPoint(cvRound((faces[0].x + faces[0].width-1)*scale), cvRound((faces[0].y + faces[0].height-1)*scale)),
        //                Scalar(0,0,255), 3, 8, 0);


        //deteccao dos olhos
        //        Rect eyeAux = Rect(Point(cvRound(faces[0].x*scale), cvRound((faces[0].y + faces[0].height/4) *scale)),
        //                Point(cvRound((faces[0].x + faces[0].width-1)*scale),
        //                cvRound((faces[0].y + faces[0].height/2)*scale)));
        //        eyeDetect(img, eyeAux);

        //        cvtColor(img, img, CV_BGR2GRAY);
        //        equalizeHist( img, img );

        //equalizacao do rosto grande (melhora a equalizacao)
        Mat cropped = img(
                    Rect(Point(cvRound(scale*(faces[0].x )), cvRound(scale*(faces[0].y))),
                Point(cvRound(scale*(faces[0].x + faces[0].width)),
                cvRound(scale*(faces[0].y + faces[0].height))))
                );
        cvtColor(cropped, cropped, CV_BGR2GRAY);
        equalizeHist(cropped,cropped);

        //ajuste da face para conter apenas o rosto
        Mat finalFace = cropped(
                    Rect(Point(cvRound(cropped.cols/6), cvRound(cropped.rows/4)),
                         Point(cvRound( cropped.cols - cropped.cols/6),
                               cvRound(cropped.rows)))
                    );
        posProcessing(&finalFace);
        resize(finalFace,finalFace,Size(92,112));
        //surfDetect(finalFace);
        imshow("crop", finalFace);

        isFaceDetected = 1;
        face = finalFace;

        //ajuste da face para conter apenas o rosto - equalizacao somente do rosto ja ajustado
//        finalFace = img(
//                    Rect(Point(cvRound(scale*(faces[0].x + faces[0].width/6)), cvRound(scale*(faces[0].y + faces[0].height/4))),
//                Point(cvRound(scale*(faces[0].x + faces[0].width - faces[0].width/6)),
//                cvRound(scale*(faces[0].y + faces[0].height))))
//                );
//        cvtColor(finalFace, finalFace, CV_BGR2GRAY);
//        resize(finalFace,finalFace,Size(92,112));
//        //surfDetect(finalFace);
//        imshow("semEqual", finalFace);

//        equalizeHist(finalFace,finalFace);
//        posProcessing(&finalFace);
//        resize(finalFace,finalFace,Size(92,112));
//        //surfDetect(finalFace);
//        imshow("final", finalFace);




        if (ESTADO == RECOGNIZE){
            //****************************CHAMAR EIGENFACES/SURF****************************//
            t = (double)cvGetTickCount();

            //SO MANDA O NOME E RECONHECE SE O SERVIDOR PEDIR
            if (receiveServer()){
                cout << "Reconhecendo" << endl;
                recognizeFace(face);
            }
//            if (serverConnection()){
//                cout << "Reconhecendo" << endl;
//                recognizeFace(face);
//            }

            t = (double)cvGetTickCount() - t;
            printf( "detection time = %g ms\n", t/((double)cvGetTickFrequency()*1000.) );

        }


    }
    else{
        isFaceDetected = 0;
        cout << "Mais de uma face detectada ou nenhuma detectada" << endl;
        return;
    }

}
