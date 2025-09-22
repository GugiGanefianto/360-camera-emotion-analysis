"""### 4. Merge the Bounding-Boxes of the Objects Which are Shown in Several Sub-Images

Bounding-boxes that are needed to be merged are categorised into:

1. Objects crossing two sub-images.

2. Objects crossing at least three sub-images.


* bboxes_all: List of bounding-boxes after projection to the original image.

* classes_all, scores_all: Lists of categories and scores of the bounding-boxes.

* width, height: Width and Height of the original images

* bboxes_boundary: A list whose length is 8, and the Nth value represents the index of the bounding-box that is tangent to the Nth boundary.

The following functions are also defined.

* weighted_average_score(): Used to calculate the weighted average score of several bounding boxes.

* class_with_largest_score(): When the bboxes to merge are of different categories, this function is used to choose the class with the largest weighted score as the class of the new bbox.

* MBR_bboxes(): Calculate the MBR of several bboxes.
"""

def merge_bbox_across_boundary(bboxes_all,classes_all,scores_all,width,height,bboxes_boundary):

    ### a list to store the indeces of the bboxes that are to be deleted after we merge them ###
    bboxes_to_delete=[]

    ### first delete the bboxes which are on the boundary and are totally in the overlapped areas ###
    names = locals()
    for i in range(0,8,1):
        if bboxes_boundary[i] !=None:
            ### although the overlapped area is 30 degree in width, set the threshold as 40, since it produces better performances ###
            if (bboxes_all[bboxes_boundary[i]][2]-bboxes_all[bboxes_boundary[i]][0]) <= int(width/360*40):
                bboxes_to_delete.append(bboxes_boundary[i])
                bboxes_boundary[i] = None

    ### Assign each value in the array to 8 variables ###
    bboxes_boundary1=bboxes_boundary[0]
    bboxes_boundary2=bboxes_boundary[1]
    bboxes_boundary3=bboxes_boundary[2]
    bboxes_boundary4=bboxes_boundary[3]
    bboxes_boundary5=bboxes_boundary[4]
    bboxes_boundary6=bboxes_boundary[5]
    bboxes_boundary7=bboxes_boundary[6]
    bboxes_boundary8=bboxes_boundary[7]

    ### if the object crosses all 4 overlapped areas (12 34 56 78) ###
    if bboxes_boundary1!=None and bboxes_boundary2!=None and bboxes_boundary3!=None and bboxes_boundary4!=None and bboxes_boundary5!=None and bboxes_boundary6!=None and bboxes_boundary7!=None and bboxes_boundary8!=None and (bboxes_boundary1==bboxes_boundary4) and (bboxes_boundary3==bboxes_boundary6) and (bboxes_boundary5==bboxes_boundary8) :
        bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1],bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary5],bboxes_all[bboxes_boundary7]]))
        classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1],bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary5],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1],scores_all[bboxes_boundary3],scores_all[bboxes_boundary5],scores_all[bboxes_boundary7]],[classes_all[bboxes_boundary2],classes_all[bboxes_boundary1],classes_all[bboxes_boundary3],classes_all[bboxes_boundary5],classes_all[bboxes_boundary7]]))
        scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1],bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary5],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1],scores_all[bboxes_boundary3],scores_all[bboxes_boundary5],scores_all[bboxes_boundary7]])])
        bboxes_to_delete.extend([bboxes_boundary1,bboxes_boundary2,bboxes_boundary3,bboxes_boundary4,bboxes_boundary5,bboxes_boundary6,bboxes_boundary7,bboxes_boundary8])
    else :
        ### if the object crosses 3 overlapped areas (12 34 56) ###
        if bboxes_boundary1!=None and bboxes_boundary2!=None and bboxes_boundary3!=None and bboxes_boundary4!=None and bboxes_boundary5!=None and bboxes_boundary6!=None and (bboxes_boundary1==bboxes_boundary4) and (bboxes_boundary3==bboxes_boundary6) :
            bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1],bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary5]]))
            classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1],bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary5]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1],scores_all[bboxes_boundary3],scores_all[bboxes_boundary5]],[classes_all[bboxes_boundary2],classes_all[bboxes_boundary1],classes_all[bboxes_boundary3],classes_all[bboxes_boundary5]]))
            scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1],bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary5]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1],scores_all[bboxes_boundary3],scores_all[bboxes_boundary5]])])
            bboxes_to_delete.extend([bboxes_boundary1,bboxes_boundary2,bboxes_boundary3,bboxes_boundary4,bboxes_boundary5,bboxes_boundary6])

            ### if another object crosses the remaining overlapped area (78) ###
            if bboxes_boundary7!=None and bboxes_boundary8!=None :
                bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary7],bboxes_all[bboxes_boundary8]]))
                classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary8],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary8],scores_all[bboxes_boundary7]],[classes_all[bboxes_boundary8],classes_all[bboxes_boundary7]]))
                scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary8],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary8],scores_all[bboxes_boundary7]])])
                bboxes_to_delete.extend([bboxes_boundary7,bboxes_boundary8])


        ### if the object crosses 3 overlapped areas (34 56 78) ###
        if bboxes_boundary3!=None and bboxes_boundary4!=None and bboxes_boundary5!=None and bboxes_boundary6!=None and bboxes_boundary7!=None and bboxes_boundary8!=None and (bboxes_boundary3==bboxes_boundary6) and (bboxes_boundary5==bboxes_boundary8) :
            bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary4],bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary5],bboxes_all[bboxes_boundary7]]))
            classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary4],bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary5],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary4],scores_all[bboxes_boundary3],scores_all[bboxes_boundary5],scores_all[bboxes_boundary7]],[classes_all[bboxes_boundary4],classes_all[bboxes_boundary3],classes_all[bboxes_boundary5],classes_all[bboxes_boundary7]]))
            scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary4],bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary5],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary4],scores_all[bboxes_boundary3],scores_all[bboxes_boundary5],scores_all[bboxes_boundary7]])])
            bboxes_to_delete.extend([bboxes_boundary3,bboxes_boundary4,bboxes_boundary5,bboxes_boundary6,bboxes_boundary7,bboxes_boundary8])

            ### if another object crosses the remaining overlapped area (12) ###
            if bboxes_boundary1!=None and bboxes_boundary2!=None :
                bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1]]))
                classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1]],[classes_all[bboxes_boundary2],classes_all[bboxes_boundary1]]))
                scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1]])])
                bboxes_to_delete.extend([bboxes_boundary1,bboxes_boundary2])

        else :
            ### if the object crosses 2 overlapped areas (12 34) ###
            if bboxes_boundary1!=None and bboxes_boundary2!=None and bboxes_boundary3!=None and bboxes_boundary4!=None and (bboxes_boundary1==bboxes_boundary4) :
                bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1],bboxes_all[bboxes_boundary3]]))
                classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1],bboxes_all[bboxes_boundary3]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1],scores_all[bboxes_boundary3]],[classes_all[bboxes_boundary2],classes_all[bboxes_boundary1],classes_all[bboxes_boundary3]]))
                scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1],bboxes_all[bboxes_boundary3]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1],scores_all[bboxes_boundary3]])])
                bboxes_to_delete.extend([bboxes_boundary1,bboxes_boundary2,bboxes_boundary3,bboxes_boundary4])

                ### if another object crosses the remaining overlapped area (56) ###
                if bboxes_boundary5!=None and bboxes_boundary6!=None :
                    bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary5],bboxes_all[bboxes_boundary6]]))
                    classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary6],bboxes_all[bboxes_boundary5]],[scores_all[bboxes_boundary6],scores_all[bboxes_boundary5]],[classes_all[bboxes_boundary6],classes_all[bboxes_boundary5]]))
                    scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary6],bboxes_all[bboxes_boundary5]],[scores_all[bboxes_boundary6],scores_all[bboxes_boundary5]])])
                    bboxes_to_delete.extend([bboxes_boundary5,bboxes_boundary6])

                ### if another object crosses the remaining overlapped area (78) ###
                if bboxes_boundary7!=None and bboxes_boundary8!=None :
                    bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary7],bboxes_all[bboxes_boundary8]]))
                    classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary8],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary8],scores_all[bboxes_boundary7]],[classes_all[bboxes_boundary8],classes_all[bboxes_boundary7]]))
                    scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary8],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary8],scores_all[bboxes_boundary7]])])
                    bboxes_to_delete.extend([bboxes_boundary7,bboxes_boundary8])

            ### if the object crosses 2 overlapped areas (34 56) ###
            if bboxes_boundary3!=None and bboxes_boundary4!=None and bboxes_boundary5!=None and bboxes_boundary6!=None and (bboxes_boundary3==bboxes_boundary6) :
                bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary4],bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary5]]))
                classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary4],bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary5]],[scores_all[bboxes_boundary4],scores_all[bboxes_boundary3],scores_all[bboxes_boundary5]],[classes_all[bboxes_boundary4],classes_all[bboxes_boundary3],classes_all[bboxes_boundary5]]))
                scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary4],bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary5]],[scores_all[bboxes_boundary4],scores_all[bboxes_boundary3],scores_all[bboxes_boundary5]])])
                bboxes_to_delete.extend([bboxes_boundary3,bboxes_boundary4,bboxes_boundary5,bboxes_boundary6])

                ### if another object crosses the remaining overlapped area (12) ###
                if bboxes_boundary1!=None and bboxes_boundary2!=None :
                    bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1]]))
                    classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1]],[classes_all[bboxes_boundary2],classes_all[bboxes_boundary1]]))
                    scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1]])])
                    bboxes_to_delete.extend([bboxes_boundary1,bboxes_boundary2])

                ### if another object crosses the remaining overlapped area (78) ###
                if bboxes_boundary7!=None and bboxes_boundary8!=None :
                    bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary7],bboxes_all[bboxes_boundary8]]))
                    classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary8],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary8],scores_all[bboxes_boundary7]],[classes_all[bboxes_boundary8],classes_all[bboxes_boundary7]]))
                    scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary8],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary8],scores_all[bboxes_boundary7]])])
                    bboxes_to_delete.extend([bboxes_boundary7,bboxes_boundary8])


            ### if the object crosses 2 overlapped areas (56 78) ###
            if bboxes_boundary5!=None and bboxes_boundary6!=None and bboxes_boundary7!=None and bboxes_boundary8!=None and (bboxes_boundary5==bboxes_boundary8) :
                bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary6],bboxes_all[bboxes_boundary5],bboxes_all[bboxes_boundary7]]))
                classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary6],bboxes_all[bboxes_boundary5],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary6],scores_all[bboxes_boundary5],scores_all[bboxes_boundary7]],[classes_all[bboxes_boundary6],classes_all[bboxes_boundary5],classes_all[bboxes_boundary7]]))
                scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary6],bboxes_all[bboxes_boundary5],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary6],scores_all[bboxes_boundary5],scores_all[bboxes_boundary7]])])
                bboxes_to_delete.extend([bboxes_boundary5,bboxes_boundary6,bboxes_boundary7,bboxes_boundary8])

                ### if another object crosses the remaining overlapped area (12) ###
                if bboxes_boundary1!=None and bboxes_boundary2!=None :
                    bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1]]))
                    classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1]],[classes_all[bboxes_boundary2],classes_all[bboxes_boundary1]]))
                    scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1]])])
                    bboxes_to_delete.extend([bboxes_boundary1,bboxes_boundary2])

                ### if another object crosses the remaining overlapped area (34) ###
                if bboxes_boundary3!=None and bboxes_boundary4!=None :
                    bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary4]]))
                    classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary4],bboxes_all[bboxes_boundary3]],[scores_all[bboxes_boundary4],scores_all[bboxes_boundary3]],[classes_all[bboxes_boundary4],classes_all[bboxes_boundary3]]))
                    scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary4],bboxes_all[bboxes_boundary3]],[scores_all[bboxes_boundary4],scores_all[bboxes_boundary3]])])
                    bboxes_to_delete.extend([bboxes_boundary3,bboxes_boundary4])

            else :
                ### if the object crosses 1 overlapped area (12) ###
                if bboxes_boundary1!=None and bboxes_boundary2!=None :
                    bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1]]))
                    classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1]],[classes_all[bboxes_boundary2],classes_all[bboxes_boundary1]]))
                    scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary2],bboxes_all[bboxes_boundary1]],[scores_all[bboxes_boundary2],scores_all[bboxes_boundary1]])])
                    bboxes_to_delete.extend([bboxes_boundary1,bboxes_boundary2])

                ### if the object crosses 1 overlapped area (34) ###
                if bboxes_boundary3!=None and bboxes_boundary4!=None :
                    bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary3],bboxes_all[bboxes_boundary4]]))
                    classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary4],bboxes_all[bboxes_boundary3]],[scores_all[bboxes_boundary4],scores_all[bboxes_boundary3]],[classes_all[bboxes_boundary4],classes_all[bboxes_boundary3]]))
                    scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary4],bboxes_all[bboxes_boundary3]],[scores_all[bboxes_boundary4],scores_all[bboxes_boundary3]])])
                    bboxes_to_delete.extend([bboxes_boundary3,bboxes_boundary4])

                ### if the object crosses 1 overlapped area (56) ###
                if bboxes_boundary5!=None and bboxes_boundary6!=None :
                    bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary5],bboxes_all[bboxes_boundary6]]))
                    classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary6],bboxes_all[bboxes_boundary5]],[scores_all[bboxes_boundary6],scores_all[bboxes_boundary5]],[classes_all[bboxes_boundary6],classes_all[bboxes_boundary5]]))
                    scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary6],bboxes_all[bboxes_boundary5]],[scores_all[bboxes_boundary6],scores_all[bboxes_boundary5]])])
                    bboxes_to_delete.extend([bboxes_boundary5,bboxes_boundary6])

                ### if the object crosses 1 overlapped area (78) ###
                if bboxes_boundary7!=None and bboxes_boundary8!=None :
                    bboxes_all.extend(MBR_bboxes([bboxes_all[bboxes_boundary7],bboxes_all[bboxes_boundary8]]))
                    classes_all.append(class_with_largest_score([bboxes_all[bboxes_boundary8],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary8],scores_all[bboxes_boundary7]],[classes_all[bboxes_boundary8],classes_all[bboxes_boundary7]]))
                    scores_all.extend([weighted_average_score([bboxes_all[bboxes_boundary8],bboxes_all[bboxes_boundary7]],[scores_all[bboxes_boundary8],scores_all[bboxes_boundary7]])])
                    bboxes_to_delete.extend([bboxes_boundary7,bboxes_boundary8])

    ### delete the boxes that have been merged from the lists ###
    bboxes_to_delete=list(set(bboxes_to_delete))
    bboxes_to_delete.sort(reverse=True)
    for i in bboxes_to_delete :
        bboxes_all.pop(i)
        classes_all.pop(i)
        scores_all.pop(i)

    return bboxes_all, classes_all, scores_all

def weighted_average_score(bboxes,scores) :
    sum=0
    sum_area=0
    for bbox,score in zip(bboxes,scores) :
        area=(bbox[3]-bbox[1])*(bbox[2]-bbox[0])
        sum+=score*area
        sum_area+=area
    return float(sum/sum_area)

def class_with_largest_score(bboxes,scores,classes) :
    sum_area=0
    score_multi_area=[]
    for bbox,score in zip(bboxes,scores) :
        area=(bbox[3]-bbox[1])*(bbox[2]-bbox[0])
        score_multi_area.append(area*score)
        sum_area+=area
    weighted_score = [i / sum_area for i in score_multi_area]
    return classes[weighted_score.index(max(weighted_score))]

def MBR_bboxes(bboxes) :
    xs=[]
    ys=[]
    for bbox in bboxes :
        xs.append(bbox[0])
        xs.append(bbox[2])
        ys.append(bbox[1])
        ys.append(bbox[3])
    return [[min(xs),min(ys),max(xs),max(ys)]]