"""
### 1. Projection Transformation from Equirectangular to Perspective View

* input_img: The input image which to be represented by the multidimensional matrix.

* FOV: The field of view of the sub-images.

* THETAs: A list that contains the theta of each sub-image (its length should be equal to the number of sub-images).

* PHIs: A list that contains the phi of each sub-image (its length should be equal to the number of sub-images).

* output_height, output_width: Height and Width of the output images (both should be the same).
"""

import os
import cv2

### import the Perspective and Equirectangular libraries ###
from .lib import Equirec2Perspec as E2P
from .lib import Perspec2Equirec as P2E
from .lib import multi_Perspec2Equirec as m_P2E


def equir2pers(input_img, FOV, THETAs, PHIs, output_height, output_width) :
    ### load the equirectangular image ###
    equ = E2P.Equirectangular(input_img)

    ### outputs save directory ###
    output_dir = "./output_sub/"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    ### define maps that define the projection from equirectangular to perspective ###
    lon_maps = []
    lat_maps = []
    imgs = []  # output images



    for i in range(len(PHIs)): # for each sub-image
        img1, lon_map1, lat_map1 = equ.GetPerspective(FOV, THETAs[i], PHIs[i], output_height, output_width)

        ### save the outputs ##
        output1 = output_dir + str(i) + ".png"
        cv2.imwrite(output1, img1)
        lon_maps.append(lon_map1)
        lat_maps.append(lat_map1)
        imgs.append(img1)

    return lon_maps, lat_maps, imgs