"""numba-optimized filters"""
from numba import jit
import numpy as np
from numba.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning, NumbaWarning
import warnings
#Couldn't get rid of the warnings so I'll just disable them. The code still works, albeit probably not at full efficiency
from copy import deepcopy

warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaWarning)

@jit
def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: image
    """
    togray = [0.21,0.72,0.07]
    
    image = deepcopy(image)
    
    for i in range(len(image[0,:])):
            p = np.uint8((np.dot(image[:,i], togray))/3)
            image[:,i] = np.transpose([p]*3)
        
    return image

@jit
def numba_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
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

