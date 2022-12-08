from instapy.python_filters import python_color2gray, python_color2sepia
import numpy as np


def test_color2gray(image):
    """Tests color2gray function against control"""
    imgTest = python_color2gray(image)
    assert imgTest.shape == image.shape
    i = np.random.randint(0, 600); j = np.random.randint(0,400)
    assert imgTest[j,i][0] == imgTest[j,i][1] == imgTest[j,i][2]
    
    return 

def test_color2sepia(image):
    """Tests color2sepia function against control"""
    imgTest = python_color2sepia(image)
    assert imgTest.shape == image.shape
    sepia_matrix = [
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131],
]
    i = np.random.randint(0, 600); j = np.random.randint(0,400)
    assert np.allclose(imgTest[j,i], np.uint8(np.dot(sepia_matrix,image[j,i])/1.5))
    
    return
    
