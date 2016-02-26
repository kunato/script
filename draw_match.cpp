#include "opencv2/calib3d/calib3d.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <cstdio>

#define ratio 1.0
using namespace cv;
using namespace std;
static void help()
{
    printf("draw_match between 2 images\n");
    printf("Format: \n./draw_match <input> <pano> <matchinfo_file> <matrix_file> <rot_file> <warp_point> <glproj_xy> \n");
}       

Mat DrawCorrespondences(const Mat& img1, const vector<Point2f>& features1, const Mat& img2,
                        const vector<Point2f>& features2,int from,int to);

void showFinal(Mat src1,Mat src2)
{
    //src2 = pano 
    Mat gray,gray_inv,src1final,src2final;
    // cvtColor(src2,gray,CV_BGR2GRAY);
    src2.copyTo(gray);
    threshold(gray,gray,0,255,CV_THRESH_BINARY);
    //adaptiveThreshold(gray,gray,255,ADAPTIVE_THRESH_MEAN_C,THRESH_BINARY,5,4);
    bitwise_not (gray, gray_inv );
    src1.copyTo(src1final,gray_inv);
    src2.copyTo(src2final,gray);
    Mat finalImage = src1final+src2final;

    Mat resiz;
    resize(finalImage,resiz,Size(),0.2,0.2);
    // namedWindow( "output", WINDOW_AUTOSIZE );
    // imshow("output",resiz);
    imwrite("homography.jpg",finalImage);
    // cvWaitKey(0);
 
}

int main(int argc, char** argv)
{

    
    help();
    std::string img1_name = std::string(argv[1]);
    std::string img2_name = std::string(argv[2]);
    std::string point2_name = std::string(argv[3]);
    std::string matrix_name = std::string(argv[4]);
    std::string point3_name = std::string(argv[5]);
    std::string rot_name = std::string(argv[6]);
    std::string warp_name = std::string(argv[7]);
    std::string glproj_name = std::string(argv[8]);
    std::string gl_img_name = std::string(argv[9]);
    FILE * pFile,* mFile , * rFile, *p4File, *warpFile,*glprojFile; 
    double x1,y1,x2,y2;
    double tmp[1000];
    std::vector<Point2f> keypoints1;
    std::vector<Point2f> keypoints2;
    std::vector<Mat> keypoints3;
    std::vector<Point2f> warpPoint;
    std::vector<Point2f> projPoint;
    std::vector<Point2f> projOrigPoint;
    mFile = fopen (matrix_name.c_str(),"r+");
    pFile = fopen (point2_name.c_str(),"r+");
    rFile = fopen (rot_name.c_str(),"r+");
    p4File = fopen(point3_name.c_str(),"r+");
    warpFile = fopen(warp_name.c_str(),"r+");
    glprojFile = fopen(glproj_name.c_str(),"r+");

    double rot[16];
    int k = 0;
    
    while(fscanf (pFile, "(%lf,%lf) (%lf,%lf)\n", &x1,&y1,&x2,&y2) == 4){
        Point2f pt =  Point(x1,y1);
        Point2f pt2 = Point(x2,y2);

        // pt*=5;
        // pt2*=5;
        keypoints1.push_back(pt);
        keypoints2.push_back(pt2);
        k++;
    }
    double xyz[4];
    while(fscanf (warpFile, "%lf %lf", &x1,&y1) == 2){
        Point2f pt(x1,y1);
        warpPoint.push_back(pt);
    }

    std::cout << "rot" << endl;
    fscanf(rFile,"[%lf, ",&rot[0]);
    std::cout << rot[0] << endl;
    for(int i = 1 ; i < 16 ; i++){
        fscanf(rFile,"%lf, ",&rot[i]);
        std::cout << rot[i] << endl;
    }

    std::cout << "HomoMatrix " << endl;
    for(int i = 0 ; i < 3 ; i++){
        
        fscanf(mFile, "[%lf %lf %lf]\n",&tmp[i*3],&tmp[i*3+1],&tmp[i*3+2]);
        std::cout << tmp[i*3] << "," << tmp[i*3+1] <<","<<tmp[i*3+2] << endl;
    }

    Mat homography(3,3,CV_64F,tmp);
    Mat rott(4,4,CV_64F,rot);
    for(int i = 0; i < keypoints1.size();i++){
        cout << keypoints1[i] << "," << keypoints2[i] << endl;
    }
    cout << "P4F" << endl;


    //printf("Reading the images...\n");
    //input
    Mat img1,img2;
    Mat full_img1 = imread(img1_name, CV_LOAD_IMAGE_GRAYSCALE);
    //pano
    Mat full_img2 = imread(img2_name, CV_LOAD_IMAGE_GRAYSCALE);
    Mat resize_tmp;
    Mat gl_img = imread(gl_img_name, CV_LOAD_IMAGE_GRAYSCALE);
    resize(full_img1,resize_tmp,Size(),1.0,1.0);
    img1 = resize_tmp;
    resize(full_img2,resize_tmp,Size(),0.2,0.2);
    img2 = resize_tmp;
    Mat img3(img1.rows,img1.cols,CV_8UC3);
    Mat warped;
    Mat H = findHomography(keypoints1,keypoints2,CV_RANSAC);

    // cout <<"H" << endl << H << endl;
    // cout <<"Homography" << endl << homography << endl;
    warpPerspective(full_img1,img3,H,full_img2.size());
    
    Mat img_corr = DrawCorrespondences(img1, keypoints1, img2, keypoints2,0,1);
    Mat small_img;
    for(int i = 0 ;i < warpPoint.size();i++){

        cout << warpPoint[i] << endl;
        circle(img2, warpPoint[i], 3, Scalar(255));
    }



    Mat gl_img_small,proj_small;
    resize(gl_img,gl_img_small,Size(),0.2,0.2);

    double height = gl_img_small.rows;
    double width = gl_img_small.cols;
    cout << "projPoint" << endl;
    while(fscanf(glprojFile,"(%lf %lf) (%lf %lf)\n",&x1,&y1,&x2,&y2)==4){
        Point2f p(x1*0.2,height-y1*0.2);
        Point2f p2(x2*0.2,y2*0.2);
        projPoint.push_back(p);
        projOrigPoint.push_back(p2);
        cout << p  << "_,_"<<  p2<<endl;
    }
    // Mat tt;
    // flip(gl_img_small,tt,0);
    // gl_img_small = tt;
    cout << "GL Point Size : " << projPoint.size() <<  endl;
    Mat proj_corr = DrawCorrespondences(gl_img_small,projPoint,img2,projOrigPoint,0,-1);

    for(int i = 0; i < projPoint.size() ;i++){
        circle(gl_img_small, projPoint[i],3 , Scalar(255));
        cout << "write :" <<projPoint[i] << endl;
    }
    resize(proj_corr,proj_small,Size(),1,1);
    imshow("proj",proj_small);
    // imshow("gl_img",gl_img_small);
    cout << img2.cols << "," << img2.rows << endl;
    // imshow("warpPoint",img2);
    resize(img_corr,small_img,Size(),0.2,0.2);
    resize(img3,warped,Size(),0.2,0.2);
    imshow("correspondences", img_corr);
    // imshow("warp", warped);
    showFinal(img3,full_img2);
    imwrite("correspondences.jpg",img_corr);
    cout << "FINISH" << endl;
    waitKey(0);
}

Mat DrawCorrespondences(const Mat& img1, const vector<Point2f>& features1, const Mat& img2,
                        const vector<Point2f>& features2,int from,int to)
{
    if(to == -1){
        to = features1.size();
    }
    Mat part, img_corr(Size(img1.cols + img2.cols, MAX(img1.rows, img2.rows)), CV_8UC3);
    cout << "img1 (" << img1.cols << "," << img1.rows << ")" << endl;
    img_corr = Scalar::all(0);
    part = img_corr(Rect(0, 0, img1.cols, img1.rows));
    cvtColor(img1, part, COLOR_GRAY2RGB);
    cout << "img2 (" << img2.cols << "," << img2.rows << ")" << endl;
    part = img_corr(Rect(img1.cols, 0, img2.cols, img2.rows));
    cvtColor(img2, part, COLOR_GRAY2RGB);

    for (size_t i = from; i < to; i++)
    {
        circle(img_corr, features1[i], 3, Scalar(0, 0, 255));
    }

    for (size_t i = from; i < to; i++)
    {
        Point pt(cvRound(features2[i].x + img1.cols), cvRound(features2[i].y));
        circle(img_corr, pt, 3, Scalar(0, 0, 255));
        line(img_corr, features1[i], pt, Scalar(0, 255, 0));
    }

    return img_corr;
}
