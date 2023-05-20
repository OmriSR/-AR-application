import numpy as np
import cv2 as cv
import pickle



def calibrate():
    # Define the workspace resolution
    worksize = (1920, 1080)

    # Calibration parameters for an iPhone 11
    square_size = 1.8
    pattern_size = (9, 6)

    # Create the pattern points for the calibration
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    # Open the video stream for calibration
    calibration_stream = cv.VideoCapture(r"data\chessboard.mp4")
    iters = 0
    # Initialize variables to store the points
    obj_points = []
    img_points = []

    # Initialize variables to store the frames and iteration count
    chosen_frames = []
    while calibration_stream.isOpened():
        iters += 1
        print(iters)
        returned_a_value, frame = calibration_stream.read()

        # Only save every 42nd frame
        if returned_a_value:
            if iters % 42 == 0:
                chosen_frames.append(frame)
        else:
            break

    # Iterate through the chosen frames
    for pic in chosen_frames:
        # Convert the frame to grayscale
        imgBGR = pic
        imgRGB = cv.cvtColor(imgBGR, cv.COLOR_BGR2RGB)
        img = cv.cvtColor(imgRGB, cv.COLOR_RGB2GRAY)

        # Find the chessboard corners
        found, corners = cv.findChessboardCorners(img, pattern_size)
        if found:
            # Append the image and object points if corners are found
            img_points.append(corners.reshape(-1, 2))
            obj_points.append(pattern_points)
    # Release the video stream
    calibration_stream.release()
    # Calibrate the camera and save the values to a file
    pickle.dump(cv.calibrateCamera(obj_points, img_points, worksize[::-1], None, None), open("calibration_values","wb"))


