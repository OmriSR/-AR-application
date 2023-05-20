import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv


def warpTwoImages(img1, img2, H):
    """
    Warps two images using a given homography matrix.
    :param img1: The first image.
    :param img2: The second image.
    :param H: The homography matrix.
    :return: The warped image.
    """
    # Get the height and width of the two images
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    # Create an array of 4 points for the corners of the first image
    pts1 = np.float32([[0, 0], [0, h1], [w1, h1], [w1, 0]]).reshape(-1, 1, 2)

    # Create an array of 4 points for the corners of the second image
    pts2 = np.float32([[0, 0], [0, h2], [w2, h2], [w2, 0]]).reshape(-1, 1, 2)

    # Transform the second image's corners using the homography matrix
    pts2_ = cv.perspectiveTransform(pts2, H)

    # Concatenate the two arrays of corners
    pts = np.concatenate((pts1, pts2_), axis=0)

    # Get the minimum and maximum values of x and y of the corners
    [xmin, ymin] = np.int32(pts.min(axis=0).ravel() - 0.5)
    [xmax, ymax] = np.int32(pts.max(axis=0).ravel() + 0.5)

    # Create a translation matrix
    t = [-xmin, -ymin]
    Ht = np.array([[1, 0, t[0]], [0, 1, t[1]], [0, 0, 1]])

    # Warp the second image using the homography matrix and the translation matrix
    result = cv.warpPerspective(img2, Ht @ H, (xmax - xmin, ymax - ymin))
    return result


def overrideFrameWithProjection(warped_proj, frame):
    """
    Overrides the frame with the given projection.
    :param warped_proj: The projection image.
    :param frame: The frame to be overridden.
    :return: The overridden frame.
    """
    # Convert the projection image to grayscale
    warped_proj_gray = cv.cvtColor(warped_proj, cv.COLOR_BGR2GRAY)

    # Iterate over every pixel in the projection image
    for i in range(warped_proj.shape[0]):
        for j in range(warped_proj.shape[1]):

            # If the pixel is not black (i.e. if the pixel has a value)
            if (warped_proj_gray[i, j]):
                # Override the corresponding pixel in the frame with the pixel from thep rojection image
                frame[i, j] = warped_proj[i, j]
    return frame

worksize = (1920,1080)
# Read in the template image and convert it to grayscale
template = cv.imread('data\life_is_fragile.jpg')
template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

# Read in the projection image and resize it to the same size as the template image
projection = cv.resize(cv.imread('data\Mona_Lisa.jpg'), (template_gray.shape[1], template_gray.shape[0]))
# Create a SIFT feature extractor
feature_extractor = cv.SIFT_create()

# Create a brute force matcher
bf = cv.BFMatcher()

# Open the video stream
stream = cv.VideoCapture(r"data\video_in.mp4")

# Read the first frame
returned_a_value, frame = stream.read()

# Create a video writer to save the output
out = cv.VideoWriter('video_out.avi', cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 17 ,worksize)

# Compute keypoints and descriptors for the template image
template_kp, template_dsc = feature_extractor.detectAndCompute(template_gray, None)

while stream.isOpened():
    # Read the next frame
    returned_a_value, frame = stream.read()

    # If a frame was read successfully
    if returned_a_value:
        # Resize the frame to the specified worksize
        frame = cv.resize(frame, worksize)

        # Compute keypoints and descriptors for the current frame
        frame_keypoints, frame_descriptors = feature_extractor.detectAndCompute(cv.cvtColor(frame, cv.COLOR_BGR2GRAY),None)

        # Match keypoints between the template and the current frame
        matches = bf.knnMatch(template_dsc, frame_descriptors, k=2)

        # Create a list to store good and second good matches
        good_and_second_good_match_list = []
        for m in matches:
            if m[0].distance / m[1].distance < 0.5:
                good_and_second_good_match_list.append(m)

        # Extract the good matches from the list
        good_matches = np.asarray(good_and_second_good_match_list)[:, 0]

        # Get the keypoints of the good matches in the template and frame
        good_kp_template = np.array([template_kp[m.queryIdx].pt for m in good_matches])
        good_kp_frame = np.array([frame_keypoints[m.trainIdx].pt for m in good_matches])

        # Compute the homography matrix using RANSAC
        H, _ = cv.findHomography(good_kp_template, good_kp_frame, cv.RANSAC, 5.0)

        # Warp the projection image using the homography matrix
        warped_proj = warpTwoImages(frame, projection, H)
        # Override the current frame with the warped projection
        frame = overrideFrameWithProjection(warped_proj, frame)
        # Write the current frame to the output video
        out.write(frame)
    else:
        break

# Release the video stream and output video writer
stream.release()
out.release()

# Close all open windows
cv.destroyAllWindows()