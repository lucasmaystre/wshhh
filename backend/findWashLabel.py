import numpy as np
import math
import cv2
import matching

def findWashLabel(label):
    template = cv2.imread('/home/ubuntu/wshhh/backend/Templates/2.jpg',0)
    
    # Binarize the label

    label = cv2.resize(label,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
    label_bin = cv2.equalizeHist(label)
    
    #scales = np.arange(1.5, 3, 0.1)
    scales = np.arange(0.2, 0.6, 0.01)

    matches = []
    for scale in scales:
        # reshape template for the current scale factor
        min_val, _, top_left, bottom_right, h, w, template_reshaped = matching.templateMatch(template, label_bin, scale)

        if top_left[1]>h/5 and top_left[0]>w/5:
            label_mini = label[top_left[1]-h/5:bottom_right[1]+h/5, top_left[0]-w/5:bottom_right[0]+w/5]
            match_value = matching.siftMatching(template_reshaped, label_mini)
            matches.append(match_value)

    matches = np.array(matches)
    best_scales = np.argsort(matches)
    best_scales = best_scales[-3:]   
    
    
    best_matching_score = math.inf
    best_label = 0

    best_num_of_matches = 0
    best_label_alt = 0

    for index_best_scale in best_scales:

        if 1:

            best_scale = scales[index_best_scale]
            min_val, center, top_left, bottom_right, h, w, template_reshaped = matching.templateMatch(template, label_bin, best_scale)        
            #matching.drawMatch(label_bin, top_left, bottom_right)

            label_mini = label_bin[top_left[1]-h/5:bottom_right[1]+h/5, top_left[0]-w/5:bottom_right[0]+w/5]


            for tmpl in [17, 1, 4, 5, 13]:
                template = cv2.imread('/home/ubuntu/wshhh/backend/Templates/'+str(tmpl)+'.jpg',0)
                template_reshaped = cv2.resize(template,None,fx=best_scale, fy=best_scale, interpolation = cv2.INTER_CUBIC)

                matching_transformation_norm, num_of_matches = matching.siftRefine(template_reshaped, label_mini, 0)
                #print(matching_transformation_norm, num_of_matches)

                if matching_transformation_norm<best_matching_score:
                    best_label = tmpl
                    best_matching_score = matching_transformation_norm

                if num_of_matches>=best_num_of_matches:
                    best_num_of_matches = num_of_matches
                    best_label_alt = tmpl


    if best_label==0:
        best_label = best_label_alt

    return best_label
