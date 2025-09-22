"""### 3. Match the Serial Number of the Sub-Images with the Serial Number of the Boundaries

* number_of_subimage: The serial number (0,1,2,3) of the sub-image.
"""

def number_of_left_and_right_boundary(number_of_subimage) :
    if number_of_subimage == 0 :
        return [2, 5]
    elif number_of_subimage == 1 :
        return [4, 7]
    elif number_of_subimage == 2 :
        return [6, 1]
    else :
        return [0, 3]