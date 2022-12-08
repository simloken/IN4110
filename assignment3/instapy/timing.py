"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing`

For Task 6.
"""
import time
import instapy
#from . import io
from typing import Callable
import numpy as np
from PIL import Image


def time_one(Callable, arguments, f=None, calls=3):
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    # run the filter function `calls` times
    # return the _average_ time of one call
    tlist = []
    for i in range(calls):
        t0 = time.perf_counter() #start time, the first calculation starts here    
        Callable(arguments)
        tlist.append(time.perf_counter() - t0)
        
    time_avg=np.sum(tlist)/calls
    return time_avg

def make_reports(filename="../test/rain.jpg", calls=3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """

    # load the image
    imgRaw = Image.open(filename)
    image = np.array(imgRaw)
    # print the image name, width, height
    f = open('timing-report.txt', 'w')
    print(imgRaw.filename.replace('../test/', ''), imgRaw.size)
    f.write('Filename: %s ------- Dimensions: %i x %i \n' %(imgRaw.filename.replace('../test/', ''), imgRaw.size[0], imgRaw.size[1]))
    # iterate through the filters
    filter_names = ['numpy', 'numba', 'cython'] #these variable names are the wrong way around
    implementations = ['color2gray', 'color2sepia']
    for implementation in implementations:
        hasRef = False
        for filter_name in filter_names:
            # get the reference filter function
            # time the reference implementation
            if hasRef == False:
                reference_time = time_one(instapy.get_filter(implementation, 'python'), image, calls)
                print(
                    "Reference (pure Python) filter time %s: reference_time%.3fs (calls=%i)" %(implementation, reference_time, calls)
                )
                f.write("Reference (pure Python) filter time %s: reference_time%.3fs (calls=%i)\n" %(implementation, reference_time, calls))
                hasRef=True            
            # time the filter
            filter_time = time_one(instapy.get_filter(implementation, filter_name), image, calls)
            # compare the reference time to the optimized time
            speedup = reference_time/filter_time
            print(
                "Timing: %s %s: %f.3s speedup=%.2fx)" %(filter_name, implementation, filter_time, speedup)
            )
            f.write("Timing: %s %s: %f.3s speedup=%.2fx)\n" %(filter_name, implementation, filter_time, speedup))
    f.close()

if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports()
