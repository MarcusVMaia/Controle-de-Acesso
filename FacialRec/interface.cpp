#include "interface.h"

fstream myfile;
int offset = 25;
int folder=0, foto = 0;
int flag;
int mode = 0;
String path_aux;
String NomeAdd;

void help()
{
    cout << "Digite no terminal: ./main cascade.xml ou ./main cascade.xml nestedCascade.xml" << endl;
}

int checkExecution(int argc,const char **argv){

    cascadeName = "haarcascade_frontalface_alt.xml";
    if( !cascade.load( cascadeName ) )
    {
        cerr << "ERROR: Could not load classifier cascade" << endl;
        return -1;
    }


    int lines = 0;
    if (ifstream("faces.csv")){
        ifstream file("faces.csv");
        String c;
        std::cout << "Arquivo ja existe" << std::endl;
        while ( std::getline(file, c) ){
            lines++;
        }
        std::cout << "linhas: "<< lines << std::endl;
        folder = lines;
        file.close();
        myfile.open ("faces.csv", ios::out | ios::app );
    }
    else{
        myfile.open ("faces.csv",std::fstream::in | std::fstream::out | std::fstream::app);
    }
    myfile.close();
}

void mouse_callback(int event, int x, int y, int, void * img)
{

    Mat image = *(Mat*)img;
    if (event == EVENT_LBUTTONDOWN){
        if (x >= image.cols - 4*offset && y >= image.rows - offset){
            ESTADO = DELETE;

            std::cout << "Delete" << std::endl;
            mode = 2;
        }
        else if (x < 4*offset && y >= image.rows - offset) {
            ESTADO = CADASTRO;

            if (flag == 0) { // flag usada pra saber se precisa criar uma nova pasta
                std::cout << "Add Person" << std::endl;
                ostringstream convert;   // stream used for the conversion
                convert << folder;      // insert the textual representation of 'i' in the characters in the stream

                String foldername = "s";
                foldername += convert.str();
                AddPerson(foldername);
                folder++;
                mode = 1;
            }
            else {
                if (isFaceDetected){
                    ostringstream convert;   // stream used for the conversion
                    convert << foto;      // insert the textual representation of 'i' in the characters in the stream

                    String photoname = "foto";
                    photoname += convert.str();
                    photoname += ".jpg";
                    AddPhoto(photoname);
                    foto++;
                }
            }
        }
    }
}

void AddPhoto(String photoname) {
    String Nomefoto;

    Nomefoto += path_aux;
    Nomefoto += photoname;
    std::cout << "Nome Foto:  "<< Nomefoto <<std::endl;
    imwrite(Nomefoto,face);

    std::cout << "Foto "<< foto+1 << "/10"<<std::endl;
    if (foto == 9){
        foto = 0;
        flag = 0; //Pronto para criar uma nova pasta
        mode = 0; //Modo da tela inicial

        /****************************** TREINAR NOVAMENTE ***************************/

        train();
        ESTADO = RECOGNIZE;
    }
}

void AddPerson(String FolderName){
    myfile.open ("faces.csv", ios::out | ios::app );	
    if (myfile.is_open())
    {
        std::cout << "file aberta" << std::endl;
    }
    string aux;
    string cadastro;

    std::cout << "Informe o nome a ser adicionado" << std::endl;
    std::cin >> NomeAdd;

    cadastro = NomeAdd + ';';
    std::cout << "Informe a senha" << std::endl;
    std::cin >> aux;

    cadastro += aux + ';';
    std::cout << "Informe o MAC" << std::endl;
    std::cin >> aux;

    cadastro += aux;

    sendData(cadastro);

    //String path = "/home/samuel/Documentos/OpenCV/FinalPVC/database/";
    //String path = "/home/bruno/openCV/face_dect/bin/database/";
    char cwd[100];
    getcwd(cwd, sizeof(cwd));
    String path = cwd;
    path += "/database/";

    String csvPath;
    path += FolderName;
    csvPath = path;
    path += "/";
    path_aux = path;
    const char * c = path.c_str();
    mkdir(c,0777);

    csvPath += ";";
    ostringstream convert;   // stream used for the conversion
    convert << (folder);
    csvPath += convert.str();

    csvPath += ";";
    csvPath += NomeAdd;
    csvPath += "\n";

    std::cout << "path:   " << csvPath <<std::endl;
    myfile << csvPath;

    flag = 1;
    myfile.close();
}
void StartDraw(Mat image) {

    if (mode == 0){
        string msg = "Click [Add Person] when ready to collect faces.";
        putText(image, msg, Point(image.cols/6, image.rows - 10), FONT_HERSHEY_PLAIN, 1.0, CV_RGB(0,255,0), 2.0);

//        cv::Point p(image.cols - 3*offset, image.rows - offset/2);
//        cv::Rect rec(image.cols - 4*offset, image.rows - offset, 4*offset, offset);
//        cv::rectangle(image,rec,cv::Scalar(0,0,0),-1);
//        cv::putText(image,"Delete",p,cv::FONT_HERSHEY_SIMPLEX,0.5,cv::Scalar(255,255,255));


        cv::Point p = cv::Point(offset/3, image.rows - offset/2);
        cv::Rect rec = cv::Rect(0, image.rows - offset, 4*offset, offset);
        cv::rectangle(image,rec,cv::Scalar(255,255,255),-1);
        cv::putText(image,"Add Person",p,cv::FONT_HERSHEY_SIMPLEX,0.5,cv::Scalar(0,0,0));
    }
    else if(mode == 1){
        string msg = "Clique em capturar para tirar a foto.";
        putText(image, msg, Point(image.cols/2, image.rows - 10), FONT_HERSHEY_PLAIN, 1.0, CV_RGB(0,255,0), 2.0);
        string msg2 = "Foto ";
        ostringstream convert;   // stream used for the conversion
        convert << (foto);      // insert the textual representation of 'i' in the characters in the stream
        msg2 += convert.str();
        msg2 += "/10";
        putText(image, msg2, Point(image.cols/6, image.rows - 10), FONT_HERSHEY_PLAIN, 1.0, CV_RGB(0,255,0), 2.0);

        Point p = cv::Point(offset/3, image.rows - offset/2);
        Rect rec = cv::Rect(0, image.rows - offset, 4*offset, offset);

        //so mostra para capturar se a face estiver detectada
        if (isFaceDetected){
            cv::rectangle(image,rec,cv::Scalar(255,255,255),-1);
            cv::putText(image,"Capturar",p,cv::FONT_HERSHEY_SIMPLEX,0.5,cv::Scalar(0,0,0));
        }
        else {
            cv::rectangle(image,rec,cv::Scalar(0,0,0),-1);
        }
    }
    else if (mode == 2){
        string msg = "Informe o nome da pessoa a ser deletada.";
        putText(image, msg, Point(image.cols/6, image.rows - 10), FONT_HERSHEY_PLAIN, 1.0, CV_RGB(0,255,0), 2.0);
        //DeletePerson();
    }
    else if (mode == 3){
        string msg = "Informe no terminal o nome da pessoa a ser adicionada.";
        putText(image, msg, Point(image.cols/6, image.rows - 10), FONT_HERSHEY_PLAIN, 1.0, CV_RGB(0,255,0), 2.0);
    }
}

void DeletePerson(){
    int numberToDelete;
    std::cin >> numberToDelete;


    //DEPOIS DE DELETAR, VOLTAR PARA O ESTADO RECOGNIZE

    ESTADO = RECOGNIZE;
}





