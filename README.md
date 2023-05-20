# AR Filter Generator

The AR Filter Generator is a powerful tool for creating augmented reality (AR) filters using computer vision techniques. It enables the development of immersive AR experiences by leveraging transformation, camera calibration, and feature detection. Inspired by the popularity of Instagram filters, this project allows users to unleash their creativity and build stunning visual effects.

## Getting Started

To get started with the AR Filter Generator, follow these steps:

1. Clone the repository to your local machine.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Calibrate your camera by following the instructions in the `calibration_notebook.ipynb` file.
4. Explore the different modules and scripts available in the repository to understand the functionalities and possibilities of the AR Filter Generator.

## Usage

To create your own AR filters:

1. Choose a feature-rich image as the reference image for tracking.
2. Print the reference image and record a video of it on a planar surface, capturing various rotations, translations, and scale changes.
3. Use the `perspective_warping.py` script to perform perspective warping on the recorded video, transforming it based on the tracked features.
4. Calibrate the camera using the printed chessboard and the provided calibration notebook.
5. Generate the final AR filter using the `planar_AR.py` script. Replace the warping lines with appropriate lines to enhance the AR visualization.
6. Experiment with rendering more elaborate 3D objects using the provided drill files and functions.

## Contributing

Contributions to the AR Filter Generator project are welcome! Please submit a pull request for any ideas, improvements, or bug fixes. For major changes, open an issue to discuss the proposed modifications.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgments

We would like to express our gratitude to our Computer Vision lecturer for their guidance throughout this project, as well as to our project partner, GAL, for their invaluable collaboration and support.

## Contact

For any questions, suggestions, or collaborations, feel free to reach out to us:

- Email: Omri.196s@gmail.com
- LinkedIn: (https://www.linkedin.com/in/omri-shahar-38909a1b0/)
Let's collaborate and create amazing AR experiences together!

#AugmentedReality #ARDevelopment #ComputerVision #Transformation #CameraCalibration #FeatureDetection
