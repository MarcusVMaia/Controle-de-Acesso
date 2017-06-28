#include "detect.h"

/***********************************
*
*CRIAR PASTA "database" no diretorio de execucao desse programa
*
***********************************/



int main( int argc, const char** argv )
{

    int retorno = checkExecution(argc, argv);
    if (retorno == -1){
        return -1;
    }
    if (!capture.isOpened()){
        cout << "Sem camera conectada" << endl;
        return -1;
    }

    namedWindow("Video");
    setMouseCallback("Video", mouse_callback, &frameCopy);

    vector<Mat> vazio1;
    vector<int> vazio2;
    //chama essa funcao apenas para pegar os nomes do arquivo csv
    read_csv("faces.csv", vazio1,vazio2);

    clientConnection();

    while( capture.read(frame) )
    {
        frameCopy = frame.clone();
        faceDetect(frame);
        StartDraw(frameCopy);

        cv::imshow( "Video", frameCopy );

        char c = waitKey(10);
        if( c == 27 ) //esc
        {
            break;
        }
    }

    closeConnection();

    return 0;
}
