#include "recognize.h"

string inputName = "";
string cascadeName = "";

double scale = 3.5; //DEFINIR ESCALA

VideoCapture capture(0); //DEFINIR DISPOSITIVO INTERNO (CAMERA)
Mat frame = Mat();
Mat frameCopy = Mat();
Mat face = Mat();

int isFaceDetected = 0;
int ESTADO = RECOGNIZE;

vector<string> names;

Ptr<FaceRecognizer> model = createEigenFaceRecognizer();

CascadeClassifier cascade = CascadeClassifier();
CascadeClassifier nestedCascade = CascadeClassifier();

void read_csv(const string& filename, vector<Mat>& images, vector<int>& labels) {
    std::ifstream file(filename.c_str(), ifstream::in);
    if (!file) {
        string error_message = "No valid input file was given, please check the given filename.";
        CV_Error(CV_StsBadArg, error_message);
    }
    char separator = ';';
    string line, path, classlabel, name;

    vector<String> filenames;

    names.clear();

    while (getline(file, line)) {
        stringstream liness(line);
        getline(liness, path, separator);
        getline(liness, classlabel, separator);
        getline(liness,name);
        if(!path.empty() && !classlabel.empty()) {

            cout << path << endl;
            glob(path, filenames);

            for(size_t i = 0; i < filenames.size(); ++i)
            {
                Mat src = imread(filenames[i], CV_LOAD_IMAGE_GRAYSCALE);
                resize(src,src, Size(92,112));

                if(!src.data)
                    cerr << "Problem loading image!!!" << endl;
                else{

                    images.push_back(src);
                    labels.push_back(atoi(classlabel.c_str()));
                    names.push_back(name);
                    //                    imshow("Treino", src);
                    //                    waitKey(0);
                }
            }
            filenames.clear();
        }
    }
}



void train(){

    vector<Mat> images;
    vector<int> labels;

    // Read in the data. This can fail if no valid
    // input filename is given.
    try {
        read_csv("faces.csv", images, labels);
    } catch (cv::Exception& e) {
        cerr << "Error opening file. Reason: " << e.msg << endl;
        exit(1);
    }
    // Quit if there are not enough images for this demo.
    if(images.size() <= 1) {
        string error_message = "This demo needs at least 2 images to work. Please add more images to your data set!";
        CV_Error(CV_StsError, error_message);
        return;
    }

    // The following lines create an Eigenfaces model for
    // face recognition and train it with the images and
    // labels read from the given CSV file.
    // This here is a full PCA, if you just want to keep
    // 10 principal components (read Eigenfaces), then call
    // the factory method like this:
    //
    //      cv::createEigenFaceRecognizer(10);
    //
    // If you want to create a FaceRecognizer with a
    // confidence threshold (e.g. 123.0), call it with:
    //
    //      cv::createEigenFaceRecognizer(10, 123.0);
    //
    // If you want to use _all_ Eigenfaces and have a threshold,
    // then call the method like this:
    //
    //      cv::createEigenFaceRecognizer(0, 123.0);
    //

    model->train(images, labels);
    model->save("recognition.xml");

}

double getSimilarity(const Mat A, const Mat B) {
    // Calculate the L2 relative error between the 2 images.
    double errorL2 = norm(A, B, CV_L2);
    // Scale the value since L2 is summed across all pixels.
    double similarity = errorL2 / (double)(A.rows * A.cols);
    return similarity;
}

void recognizeFace(Mat face) {

    if (!ifstream("recognition.xml")){
        cout << "Arquivo de reconhecimento não detectado. Insira pelo menos duas pessoas" << endl;
        return;
    }

    model->load("recognition.xml");

    double confidence = 0.0;
    int predictedLabel = -1;
    resize(face,face, Size(92,112));

    //model->set("threshold", 5000.0);
    model->predict(face,predictedLabel,confidence);
    predictedLabel = model->predict(face);
    //cout << "Classe " << predictedLabel << " Distancia " << confidence <<endl;
    cout << "Pessoa reconhecida: " << names[predictedLabel] << "  Distancia: " << confidence << endl;

    sendData(names[predictedLabel]);

}

void surfRecognition(Mat SurfdescriptorsTemplate, Mat SurfdescriptorsComp){

    //Matches
    cv::BFMatcher matcher;
    std::vector<cv::DMatch> matches;

    //Surf matching
    matcher.match(SurfdescriptorsTemplate,SurfdescriptorsComp, matches);

    //verificar a quantidade de matches e suas distancia


}
