#include <iostream>
#include <opencv2/opencv.hpp>
#include <raspicam/raspicam_cv.h>

int main() {
    raspicam::RaspiCam_Cv camera;
    
    // Open the camera
    if (!camera.open()) {
        std::cerr << "Error opening camera" << std::endl;
        return -1;
    }

    cv::Mat image;
    camera.grab();
    camera.retrieve(image);

    // Compress the image using JPEG format with compression parameters
    std::vector<int> compression_params;
    compression_params.push_back(cv::IMWRITE_JPEG_QUALITY);
    compression_params.push_back(95);  // You can adjust the quality (0-100)

    std::vector<uchar> encoded_image;
    cv::imencode(".jpg", image, encoded_image, compression_params);

    // Save the compressed image to a file
    std::ofstream file("compressed_image.jpg", std::ios::binary);
    file.write(reinterpret_cast<const char*>(encoded_image.data()), encoded_image.size());
    file.close();

    std::cout << "Image saved as compressed_image.jpg" << std::endl;

    return 0;
}
