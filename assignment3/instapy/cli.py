"""Command-line (script) interface to instapy"""

import argparse
import sys
import time

import numpy as np
from PIL import Image

import instapy
#from . import io


def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter_name: str = "color2gray",
    scale: int = 1,
    runtime: bool = False,
) -> None:
    """Convert rgb pixel array to sepia

    Args:
        file: str, filepath string
        out_file: str, 
            output filename. If None then the image is shown instead
        implementation: str, 
            which type of implementation to use
        filter_name: str, 
            which colour filter to apply to the image
        scale: float, 
            a factor with which to scale the image
        runtime: bool,
            if True returns an average runtime over 3 runs, else nothing
    """
    # load the image from a file
    image = Image.open(file)
    form = image.format
    if scale != 1:
        # Resize image, if needed
        width, height = image.size
        width = int(width*scale); height = int(height*scale)
        image = image.resize((width,height))

    # Apply the filter
    image = np.array(image)
    if runtime == True:
        tlist = []
        for i in range(2):
            t0 = time.perf_counter()
            instapy.get_filter(filter_name, implementation)(image)
            tlist.append(time.perf_counter() - t0)
        t0 = time.perf_counter()
        filtered = instapy.get_filter(filter_name, implementation)(image)
        tlist.append(time.perf_counter() - t0)
        print('Average time over 3 runs: %.3fs' %(np.average(tlist)))
        filtered = Image.fromarray(filtered)
    else:
        fun = instapy.get_filter(filter_name, implementation)
        filtered = fun(image)
        filtered = Image.fromarray(filtered)
        
    if out_file:
        # save the file
        filtered.save(out_file + '.%s' %(form))
    else:
        # not asked to save, display it instead
        filtered.show()


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]
        
    parser = argparse.ArgumentParser()
    
    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")
    parser.add_argument("-o", "--out", help="The output filename DEFAULT=[No filename, show image instead]")

    # Add required arguments
    parser.add_argument('-i','--implementation', help='The implementation to use [python, numpy, numba, cython] DEFAULT=[python]', default='python')
    parser.add_argument('-f', '--filter_name', help='The filter to use [color2gray, color2sepia] DEFAULT=[color2gray]', default='color2gray')
    parser.add_argument('-sc','--scale', help='Scaling factor for the output image DEFAULT=[1]', default=1)
    parser.add_argument('-r', '--runtime', help='Prints the average run time over 3 runs [True, False] DEFAULT=[False]', default=False)
    args = parser.parse_args()
    
    
    
    tlist = []
    for i in args.__dict__: #surely there is a better way to do this?!
        target = args.__dict__[i]
        if args.__dict__[i] == '-h':
            parser.print_help()
            return
        
        if target is None: #for -o if no input
            tlist.append(target)
            continue
        
        try: #converts from strings to numbers or booleans if applicable
            float(target)
        except:
            if isinstance(target, str):
                if target.lower() in ['true','false']:
                    if target.lower() == 'true':
                        tlist.append(True)
                    elif target.lower() == 'false':
                        tlist.append(False)
                
                else:
                    tlist.append(target)
        else:
            tlist.append(float(target))
           
    run_filter(*tlist)
