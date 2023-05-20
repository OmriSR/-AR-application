AR Filter Generator
The AR Filter Generator is a project designed to enable the creation of augmented reality (AR) filters using computer vision techniques. By leveraging concepts such as transformation, camera calibration, and feature detection, this project provides a platform to develop immersive and engaging AR experiences. Whether you're a developer, designer, or AR enthusiast, this generator gives you the tools to unleash your creativity and build stunning visual effects.

Getting Started
To get started with the AR Filter Generator, follow the steps below:

Clone the repository to your local machine using the following command:

bash
Copy code
git clone <repository-url>
Install the necessary dependencies by running:

Copy code
pip install -r requirements.txt
Calibrate your camera by following the instructions in the calibration_notebook.ipynb file. This calibration process will provide the required camera parameters for accurate AR visualization.

Explore the different modules and scripts available in the repository to understand the functionalities and possibilities of the AR Filter Generator.

Usage
To create your own AR filters, follow these steps:

Choose a feature-rich image as the reference image for tracking the desired features.

Print the reference image and record a video of it on a planar surface while capturing various rotations, translations, and scale changes. This video will serve as the input for the AR filter generation.

Use the perspective_warping.py script to perform perspective warping on the recorded video, transforming it based on the tracked features.

Once the camera is calibrated using the printed chessboard and the provided calibration notebook, use the planar_AR.py script to generate the final AR filter. Replace the warping lines with appropriate lines to enhance the AR visualization.

To go beyond basic shapes, experiment with rendering more elaborate 3D objects by using the provided drill files and functions.

Contributing
We welcome contributions to the AR Filter Generator project. If you have any ideas, improvements, or bug fixes, please submit a pull request. For major changes, kindly open an issue first to discuss the proposed modifications.

License
This project is licensed under the MIT License.

Acknowledgments
We would like to express our gratitude to our Computer Vision lecturer for their guidance throughout this project, as well as to our project partner, GAL, for their invaluable collaboration and support.

Contact
For any questions, suggestions, or collaborations, please feel free to reach out to us:

Email: Omris.1996s@gmail.com
LinkedIn: https://www.linkedin.com/in/omri-shahar-38909a1b0/
Let's collaborate and create amazing AR experiences together!

#AugmentedReality #ARDevelopment #ComputerVision #Transformation #CameraCalibration #FeatureDetection
