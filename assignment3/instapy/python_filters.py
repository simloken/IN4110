"""pure Python implementation of image filters"""

import numpy as np
from PIL import Image
from copy import deepcopy

def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: image
    """
    togray = (0.21,0.72,0.07)
    
    image = deepcopy(image) #this is because of a dumb error where image outside of our function gets changed
    
    width = len(image[0,:])
    height = len(image[:,:])
    
    
    for i in range(width):
        for j in range(height):
            p = image[j,i]
            p = (np.uint8((a*b)/3) for a, b in zip(p,togray)) #list comprehension (very pythonic!)
            p = sum(p)
            image[j,i] = 3*[p]
            

    return image

def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: image
    """
    sepia_matrix = [
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131],
]
    
    image = deepcopy(image)
    scaler = 1.5   #stops weird colours from appearing
        
    for i in range(len(image[0,:])):
        for j in range(len(image[:,0])):  
            p = []
            for a in sepia_matrix:
                p.append(np.uint8(sum(a*image[j,i])/scaler))
                
            image[j,i] = p

    # Return image
    # don't forget to make sure it's the right type!
    return image
