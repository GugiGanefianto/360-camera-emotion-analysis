"""### 2. Project the Bounding-Boxes on the Sub-Images Back to the Original Image

Also return the bounding-boxes whose Left/Right borders are tangent to a border of the sub-image which are required to be merged


* bboxes: a list of bounding-boxes in [x_min y_min x_max y_max] format.

* lon_map_original, lat_map_original: Map matrix obtained through the projection transformation from equirectangular to perspective (i.e., lon_maps, lat_maps returned by equir2pers() ).

* classes, scores: list of classes and scores predicted by the object detection model.

* interval: A value that determines the pixel interval used for calculating the corresponding coordinate point of the bounding-box in the sub-images. Smaller interval means higher accuracy.

* num_of_subimage: Serial number of the current sub-image (i.e., 0, 1, 2, or 3, see paper).

* input_video_width, input_video_height: Width and Height of the input video.

* num_of_subimages: The total number of sub-images, should be 4 by default.

* threshold_of_boundary: Threshold to determine whether the Left/Right border of a bounding box is tangent to the border of the sub-image (i.e., distance > threshold_of_boundary).

* is_split_image2: Whether to split the bboxes into two across the centre line of the sub-image, default to True.
"""

def reproject_bboxes(
    bboxes,
    lon_map_original,
    lat_map_original,
    classes,
    scores,
    interval,
    num_of_subimage,
    input_video_width,
    input_video_height,
    num_of_subimages,
    threshold_of_boundary,
    is_split_image2=True) :

    ### lists for storing the new bboxes, classes, and scores after reprojection ###
    new_bboxes = []
    new_classes = []
    new_scores = []

    ### variables that store the index of the bboxes from the new_bboxes list ###
    ### which coincide with the Left/Right boundaries of the sub-image ###
    left_boundary_box = None
    right_boundary_box = None

    ### calculate the degree of overlap between each pair of adjacent sub-images ###
    ### if the number of sub-images is 4, this will result to 30 ###
    overlaped_degree = (num_of_subimages * 120 - 360) / num_of_subimages

    ### calculate which subimage to be splited into two parts ###
    ### if the number of sub-images is 4, this will result to image 2 ###
    num_of_splited_subimage = num_of_subimages / 2

    index = 0

    ### number of pixels occupied by (overlaped_degree/2) degrees on the sub-image ###
    margin = int(lon_map_original.shape[0] / 120 * (overlaped_degree / 2))



    for bbox, class1, score in zip(bboxes, classes, scores) :
        ### get the coordinates of the top-left point and the right-bottom point ###
        left_top_x = int(bbox[0])
        left_top_y = int(bbox[1])
        right_bottom_x = int(bbox[2])
        right_bottom_y = int(bbox[3])

        ### only reproject bboxes that are not fully inside the overlapping area, and their y-values are less than 70 degress ###
        ### specific to the problem in which otherwise, the backpack of the cyclist will be incorrectly detected as a car ###
        if (margin <= ((left_top_x + right_bottom_x) / 2)
            <= (lon_map_original.shape[0] - margin)
            and left_top_y <= lon_map_original.shape[0] / 120 * 70 ) :

            ### for an a*b sub image, the size of lon_map and lat_map is (a-1)*(b-1), when the right_bottom_x or the right_bottom_y equals to a or b ###
            ### to get the corresponding value in lon_map and lat_map (which represent he corresponding position on the original image) we have to subtract them by 1 ###
            if right_bottom_x == lon_map_original.shape[0] :
                right_bottom_x -= 1
            if right_bottom_y == lon_map_original.shape[1] :
                right_bottom_y -= 1

            ### check if the bbox coincides with the Left/Right boundaries of the sub-image ###
            ### if yes, assign its index to left_boundary_box/right_boundary_box ###
            ### if the bbox is large (>subimage size/5), use the threshold to do the judgement ###
            if (right_bottom_x - left_top_x) * (right_bottom_y - left_top_y)  <  lon_map_original.shape[0] * lon_map_original.shape[0] / 5 :

                if left_top_x <= threshold_of_boundary :
                    left_boundary_box = index
                if right_bottom_x >= lon_map_original.shape[0] - threshold_of_boundary :
                    right_boundary_box = index

            ### if the bbox is small (<=subimage size/5), set the threshold a little bit larger ###
            ### this is arbitrarily determined through experiments ###
            else :
                if left_top_x <= (threshold_of_boundary + 15 * int(lon_map_original.shape[0] / 640) ) :
                    left_boundary_box = index
                if right_bottom_x >= lon_map_original.shape[0] - (threshold_of_boundary + 15 * int(lon_map_original.shape[0] / 640) ) :
                    right_boundary_box = index


            ### lists to store the corresponding x and y coordinates of each point on the bbox on the original image ###
            xs = []
            ys = []


            ### if the current sub-image is the one which crosses the boundary (e.g., image 2, when the number of sub-image is 4) ###
            ### and the current bbox is across the center line ###
            if (num_of_subimage == num_of_splited_subimage
                and left_top_x <= int(lon_map_original.shape[0] / 2) - 1
                and right_bottom_x >= int(lon_map_original.shape[0] / 2) ) :

                ### lists to store the x coordinates of each point on the Left/Right part of the bbox on the original image ###
                xs_left = []
                xs_right = []

                ### calculation for the left and right borders ###
                for i in range(left_top_y, right_bottom_y, interval) :
                    ### left border ###
                    x = int(round(lon_map_original[i, left_top_x]))
                    y = int(round(lat_map_original[i, left_top_x]))
                    xs.append(x)
                    ys.append(y)
                    xs_left.append(x)
                    ### right border ###
                    x = int(round(lon_map_original[i, right_bottom_x]))
                    y = int(round(lat_map_original[i, right_bottom_x]))
                    xs.append(x)
                    ys.append(y)
                    xs_right.append(x)

                ### calculation for the left part of the top and bottom borders ###
                for i in range(left_top_x, int(lon_map_original.shape[0] / 2) - 1, interval) :
                    x = int(round(lon_map_original[left_top_y, i]))
                    y = int(round(lat_map_original[left_top_y, i]))
                    xs.append(x)
                    ys.append(y)
                    xs_left.append(x)
                    x = int(round(lon_map_original[right_bottom_y, i]))
                    y = int(round(lat_map_original[right_bottom_y, i]))
                    xs.append(x)
                    ys.append(y)
                    xs_left.append(x)

                ### calculation for the right part of the top and bottom borders ###
                for i in range(int(lon_map_original.shape[0] / 2), right_bottom_x, interval) :
                    x = int(round(lon_map_original[left_top_y, i]))
                    y = int(round(lat_map_original[left_top_y, i]))
                    xs.append(x)
                    ys.append(y)
                    xs_right.append(x)
                    x = int(round(lon_map_original[right_bottom_y, i]))
                    y = int(round(lat_map_original[right_bottom_y, i]))
                    xs.append(x)
                    ys.append(y)
                    xs_right.append(x)



                ymax = max(ys)
                ymin = min(ys)
                xmin_left = min(xs_left)
                xmax_right = max(xs_right)

                ### if it is needed to split the bbox into two parts, create two bboxes with the MBRs of the left and right part seperately ###
                if is_split_image2 == True :
                    new_bboxes.append([xmin_left, ymin, input_video_width, ymax])
                    new_bboxes.append([0, ymin, xmax_right, ymax])
                    new_classes.append(int(class1))
                    new_classes.append(int(class1))
                    new_scores.append(score)
                    new_scores.append(score)
                    index += 2

                ### if not, create one bbox which extends outside the right boundary ###
                else :
                    new_bboxes.append([xmin_left, ymin, input_video_width + xmax_right, ymax])
                    new_classes.append(int(class1))
                    new_scores.append(score)
                    index += 1

            ### if the current sub-image is not the one which crosses the boundary ###
            else :
                ### in case the interval is set larger than the length of the border, if so, set it as the length of the short side of the bbox ###
                if (right_bottom_x - left_top_x < interval or right_bottom_y - left_top_y < interval) :
                    interval = min(right_bottom_x - left_top_x, right_bottom_y - left_top_y)

                ### get the corresponding coordinates of each point on the boundary on the original image ###
                for i in range(left_top_y, right_bottom_y, interval):
                    x = int(round(lon_map_original[i, left_top_x]))
                    y = int(round(lat_map_original[i, left_top_x]))
                    xs.append(x)
                    ys.append(y)
                    x = int(round(lon_map_original[i, right_bottom_x]))
                    y = int(round(lat_map_original[i, right_bottom_x]))
                    xs.append(x)
                    ys.append(y)
                for i in range(left_top_x, right_bottom_x, interval):
                    x = int(round(lon_map_original[left_top_y, i]))
                    y = int(round(lat_map_original[left_top_y, i]))
                    xs.append(x)
                    ys.append(y)
                    x = int(round(lon_map_original[right_bottom_y, i]))
                    y = int(round(lat_map_original[right_bottom_y, i]))
                    xs.append(x)
                    ys.append(y)

                ### create one bbox with the MBR ###
                xmax = max(xs)
                xmin = min(xs)
                ymax = max(ys)
                ymin = min(ys)
                new_bboxes.append([xmin, ymin, xmax, ymax])
                new_classes.append(int(class1))
                new_scores.append(score)
                index += 1

    return new_bboxes, new_classes, new_scores, left_boundary_box, right_boundary_box