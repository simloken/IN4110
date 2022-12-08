"""numpy implementation of image filters"""

import numpy as np
from copy import deepcopy

def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: image
    """

    togray = (0.21,0.72,0.07)
    
    image = deepcopy(image)
    
    for i in range(len(image[0,:])):
            p = np.uint8((np.dot(image[:,i], togray))/3)
            image[:,i] = np.transpose([p]*3)
        
    return image
        
        
    
    # Hint: use numpy slicing in order to have fast vectorized code
    ...
    # Return image (make sure it's the right type!)
    return image


def numpy_color2sepia(image: np.array, k=1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
    you may ignore it for Task 9)

    Returns:
        np.array: image
    """

    if not 0 <= k <= 1:
        raise ValueError("k must be between [0-1], %g" %(k))
        
    

    sepia_matrix = [
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131],
]
    
    if k == 0:
        scaler = 1
    else:
        scaler = 1.5
    
    if k != 1:
        I = np.array(((1,0,0),(0,1,0),(0,0,1)))
        sepiaNumpy = np.array(sepia_matrix)
        dif = sepiaNumpy-I
        sepia_matrix = I+dif*k
        sepia_matrix = sepia_matrix.tolist()
    
    image = deepcopy(image)
    
    for i in range(len(image[0,:])):
        for j in range(len(image[:,0])):  
            p = np.uint8((np.dot(sepia_matrix,image[j,i]))/scaler)
            image[j,i] = p
    return image
