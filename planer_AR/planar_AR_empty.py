from mesh_renderer import MeshRenderer
import cv2 as cv, pickle, numpy as np, os
import matplotlib.pyplot as plt
from calibrations import calibrate

def getGoodKeyPoints(matches):
    """
    Given a list of matches, this function filters out matches with a low ratio of distance
    between the best and second best match. It returns the good keypoints of the template and frame.
    """
    good_and_second_good_match_list = []
    for m in matches:
        if m[0].distance / m[1].distance < 0.7:
            good_and_second_good_match_list.append(m)
    good_matches = np.asarray(good_and_second_good_match_list)[:, 0]
    good_kp_template = np.array([template_keypoints[m.queryIdx].pt for m in good_matches])
    good_kp_frame = np.array([frame_keypoints[m.trainIdx].pt for m in good_matches])
    return good_kp_template, good_kp_frame

def filter_matches(good_kp_template, good_kp_frame, H):
    """
    This function filters the good keypoints by applying a homography transform and then
    comparing the distance between the transformed keypoints and the frame keypoints.
    It returns the filtered keypoints.
    """
    transformed_pts = cv.perspectiveTransform(np.array([good_kp_template]),H)[0]
    best_kp = [(good_kp_frame[i], good_kp_template[i]) for i, (fc, tc) in enumerate(zip(good_kp_frame, transformed_pts)) if np.linalg.norm(fc-tc) < 10]
    subset_obidient_frameP, subset_obidient_templateP = zip(*best_kp)
    subset_obidient_frameP, subset_obidient_templateP = np.array(subset_obidient_frameP), np.array(subset_obidient_templateP)
    return subset_obidient_frameP, subset_obidient_templateP

def scale_template_points(subset_obidient_templateP, TEMPLATEHEIGHT, TEMPLATEWIDTH):
    """
    This function scales the template points to match the size of the template image.
    """
    temp = []
    for vec in subset_obidient_templateP:
        x = vec[0] *  TEMPLATEWIDTH / 1080
        y = vec[1] * TEMPLATEHEIGHT / 1920
        temp.append([x, y, 0])
    subset_obidient_templateP = np.array(temp)
    return subset_obidient_templateP

if not os.path.exists('calibration_values'):
    calibrate()

ret, camera_matrix, dist_coefs, rvecs, tvecs = pickle.load(open('calibration_values','rb'))

worksize = (1920, 1080)

TEMPLATEHEIGHT = 36
TEMPLATEWIDTH = 25

# Initialize the MeshRenderer object
meshrenderer = MeshRenderer(camera_matrix, worksize[0], worksize[1], 'data\drill\drill.obj')

# Read the template image
template = cv.imread(r'data\template2.jpg')

# Create feature extractor and matcher objects
feature_extractor = cv.SIFT_create()
bf = cv.BFMatcher()

# Open the video stream
stream = cv.VideoCapture(r"data\playground.mp4")
returned_a_value, frame = stream.read()

# Create an output video writer
out = cv.VideoWriter('video_out.avi', cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 60, worksize)

# Extract keypoints and descriptors from the template image
template_keypoints, template_descriptors = feature_extractor.detectAndCompute(cv.cvtColor(template, cv.COLOR_BGR2GRAY),
                                                                              None)

###### main loop ######

while stream.isOpened():
    # Read the next frame
    theres_more, frame = stream.read()
    if theres_more:
        # Extract keypoints and descriptors from the frame
        frame_keypoints, frame_descriptors = feature_extractor.detectAndCompute(cv.cvtColor(frame, cv.COLOR_BGR2GRAY),
                                                                                None)

        # Match the keypoints between the template and the frame
        matches = bf.knnMatch(template_descriptors, frame_descriptors, k=2)

        # Get the good keypoints
        good_kp_template, good_kp_frame = getGoodKeyPoints(matches)

        # Find the homography matrix
        H, Mask = cv.findHomography(good_kp_template, good_kp_frame, cv.RANSAC, 5.0)

        # Filter the matches
        subset_obidient_frameP, subset_obidient_templateP = filter_matches(good_kp_template, good_kp_frame, H)

        # Scale the template points
        subset_obidient_templateP = scale_template_points(subset_obidient_templateP, TEMPLATEHEIGHT, TEMPLATEWIDTH)

        # Solve for the pose
        retval, rvec, tvec = cv.solvePnP(subset_obidient_templateP, subset_obidient_frameP, camera_matrix, dist_coefs)

        # Render the mesh
        frame = meshrenderer.draw(cv.undistort(frame, camera_matrix, dist_coefs), rvec, tvec)

        # Write the frame to the output video
        out.write(frame)

        # Display the frame
        cv.imshow('frame', frame)
    else:
        break
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and output video writer
stream.release()
out.release()
cv.destroyAllWindows()