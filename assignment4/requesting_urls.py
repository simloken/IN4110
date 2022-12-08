from typing import Dict, Optional

import requests

## -- Task 1 -- ##


def get_html(url: str, params: Optional[Dict] = None, output: Optional[str] = None):
    """Get an HTML page and return its contents.

    Args:
        url (str):
            The URL to retrieve.
        params (dict, optional):
            URL parameters to add.
        output (str, optional):
            (optional) path where output should be saved.
    Returns:
        html (str):
            The HTML of the page, as text.
    """
    # passing the optional parameters argument to the get function
    if params:
        html_str = requests.get(url, params=params)
        
    else:
        html_str = requests.get(url)

    

    if output:
        # if output is specified, the response txt and url get printed to a
        # txt file with the name in `output`
        f = open(f'{output}'+'.txt', 'w', encoding="utf-8")
        f.write(html_str.text)
        f.close()
        return

    return html_str.text