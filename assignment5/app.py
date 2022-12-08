import datetime
from typing import List, Optional
import nest_asyncio
nest_asyncio.apply() #for running in an IDE like Spyder
import pathlib
path = pathlib.Path(__file__).parent.resolve()
import altair as alt
from fastapi import FastAPI, Query, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

app = FastAPI()
app.mount("/help", StaticFiles(directory="docs/_build/html", html=True), name="help")
templates = Jinja2Templates(directory='templates')

@app.get("/")
def strompris_html(request: Request):
    """Baseline HTML GET for when redirecting to "/"

    parameters:
        none
        
    returns:
        strompris.html: The HTML file and the "index" of our project. Contains a modifiable chart that can be modified client-side/on the user-end.
    """
    return templates.TemplateResponse(
        "strompris.html",
        {
            "request": request,
            "locations": LOCATION_CODES,
        },
    )
    
@app.get("/activity.html")
def activity_html(request: Request):
    """Baseline HTML GET for when redirecting to "/"

    parameters:
        none
        
    returns:
        activity.html: The HTML file containing a chart that can be modifed client-side/user-end
    """
    return templates.TemplateResponse(
        "activity.html",
        {
            "request": request,
            "locations": LOCATION_CODES,
            "activity": ACTIVITIES,
        },
    )


#awful solution
#@app.get("/help/strompris.html")
#def help(request: Request):
#    fullpath = str(path) + '\\docs\\_build\\html\\'
#    f = open(fullpath+'strompris.html').read()
#    return HTMLResponse(f)

@app.get("/plot_prices.json")
def plot_prices_json(
    end: datetime.date = Query(default=None),
    days: int = Query(default=7),
    locations: Optional[List[str]] = Query(default=None)):
    """Handler that handles user input data to return an appropriate chart (General prices). Passes data collected from the HTML and returns it as a JSONable vega-lite structure

    parameters:
        end (datetime.date): The day to end our data
        days (int): The number of days to collect data from
        locations (str or array-like): The locations to collect data from
        
    returns:
        alt.chart.to_dict(): a JSONable vega-lite structure that can then be displayed as the requested chart
    """
    # altair Chart.to_dict() is a JSONable vega-lite structure
    fig = plot_prices(fetch_prices(end, days, list(LOCATION_CODES.values())), locations)
    return fig.to_dict()
    
@app.get("/plot_activity_prices.json")
def plot_activity_json(
    activity: str = Query(default='Shower'),
    minutes: int = Query(default=10),
    location: str = Query(default='NO1')):
    """Handler that handles user input data to return an appropriate chart (activity prices). Passes data collected from the HTML and returns it as a JSONable vega-lite structure

    parameters:
        activity (str): A string for which activity prices should be returned for
        minutes (int): Number of minutes an activity will be happening
        location (str): The location to use price data from.
        
    returns:
        alt.chart.to_dict(): a JSONable vega-lite structure that can then be displayed as the requested chart
    """
    fig = plot_activity_prices(activity, minutes, location)
    return fig.to_dict()
    

if __name__ == "__main__":
    # use uvicorn to launch your application on port 5000
    
    import uvicorn
    
    uvicorn.run(app, port=5000)
