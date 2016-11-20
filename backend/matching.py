import numpy as np
import math
import cv2
import matplotlib.pyplot as plt

def templateMatch(template, label_bin_blur, scale):
    template_reshaped = cv2.resize(template,None,fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC)
    w, h = template_reshaped.shape[::-1]

    label_current = label_bin_blur.copy()
    method = eval('cv2.TM_CCOEFF_NORMED')

    # Apply template Matching
    res = cv2.matchTemplate(label_current,template_reshaped,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    center = (top_left[0] + w/2, top_left[1] + h/2)
    
    return min_val, center, top_left, bottom_right, h, w, template_reshaped

def drawMatch(label, top_left, bottom_right):

    label_current = label.copy()
    # draw a rectangle
    cv2.rectangle(label_current,top_left, bottom_right, 100, 20)

    # draw the template with label
    plt.figure()
    plt.imshow(label_current,cmap = 'gray')
    
def siftMatching(template_reshaped, image_mini):
    
    
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(template_reshaped,None)
    kp2, des2 = sift.detectAndCompute(image_mini,None)
    if len(kp1)>1 and len(kp2)>1:

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1,des2,k=2)

        good = []
        for m,n in matches:
            if m.distance < 0.8*n.distance:
                good.append(m)

        match_value = len(good)
    else:
        match_value = -math.inf
    
    return match_value

def drawSiftMatch(matchesMask, template_reshaped, kp1, image_mini, kp2, good):
    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

    img3 = cv2.drawMatches(template_reshaped,kp1,image_mini,kp2,good,None,**draw_params)

    plt.imshow(img3),plt.show()
    
def siftRefine(template_reshaped, image_mini, draw):
    
    matching_transformation_norm = math.inf
    good = []
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(template_reshaped,None)
    kp2, des2 = sift.detectAndCompute(image_mini,None)
    MIN_MATCH_COUNT = 5
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    if not(des1 is None) and not(des2 is None):
        

        matches = flann.knnMatch(des1,des2,k=2)
        # store all the good matches as per Lowe's ratio test.
        for m,n in matches:
            good.append(m)

        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            if M is None:
                matching_transformation_norm = math.inf
            else:
                matching_transformation_norm = np.linalg.norm(M-np.eye(3))

            if draw  and not(M is None):
                matchesMask = mask.ravel().tolist()

                h,w = template_reshaped.shape
                pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
                dst = cv2.perspectiveTransform(pts,M)

                im_new = cv2.polylines(image_mini,[np.int32(dst)],True,255,3, cv2.LINE_AA)

        else:
            print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
            matchesMask = None

        if draw and not(M is None):
            draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                           singlePointColor = None,
                           matchesMask = matchesMask, # draw only inliers
                           flags = 2)

            img3 = cv2.drawMatches(template_reshaped,kp1,image_mini,kp2,good,None,**draw_params)

            plt.imshow(img3),plt.show()
    
    return matching_transformation_norm, len(good)
    