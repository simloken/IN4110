"""Cython implementation of filter functions"""

import numpy as np
cimport numpy as np
from copy import deepcopy


def cython_color2gray(image):
    
    togray = (0.21,0.72,0.07)
    
    image = deepcopy(image)
    
    for i in range(len(image[0,:])):
            p = np.uint8((np.dot(image[:,i], togray))/3)
            image[:,i] = np.transpose([p]*3)
        
    return image

def cython_color2sepia(image):
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    sepia_matrix = [
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131],
]
    scaler=1.5  
    
    image = deepcopy(image)
    
    for i in range(len(image[0,:])):
        for j in range(len(image[:,0])):  
            p = np.uint8((np.dot(sepia_matrix,image[j,i]))/scaler)
            image[j,i] = p
    return image
