import json
from flask import Flask, request, send_file, abort
from matplotlib import figure
import io

import visualisation.visualiser as Visualiser
import utils

app = Flask(__name__)

# Takes in a visualised plot and returns an Image class
def plot_to_image(fig: figure) -> bytes:
    if fig is None:
        # If figure has issues as decided by Visualiser
        return None
    
    buf = io.BytesIO()             # Create new Bytes buffer
    fig.savefig(buf, format="png") # Save figure in 'png' format
    buf.seek(0)                    # Seek to the start of the buffer
    return buf

# Add "artefact.css" to the virtual file system
# in which can be used in a stylesheet tag
@app.route("/artefact.css")
def frontend_css():
    return open("artefact.css", "r").read(), 200, {'Content-Type': 'text/css'}

# Add "artefact.js" to the virtual file system
# in which can be used in a <script> tag
@app.route("/artefact.js")
def frontend_js():
    return open("artefact.js", "r", encoding="utf-8").read(), 200, {'Content-Type': 'text/javascript'}

# Add "artefact.html" to the virtual file system
@app.route("/")
def frontend_html():
    return open("artefact.html", "r").read()

### graph_occupations endpoint for 
# Occupations pie chart
# Requires queries "Year"

@app.route("/api/graph_occupations")
def occupations():
    year = 0
    
    try:
        year = int(request.args.get("year"))
    except ValueError:
        # Client Error (invalid parameter)
        return abort(400)
    
    plot_data = plot_to_image(Visualiser.graph_occupations(year))
    if plot_data is not None:
        # Return a response as an image
        return send_file(plot_data, mimetype="image/png")

    # Bad Request (No file to return)
    return abort(400)

### graph_employment_trend endpoint for 
# Employment levels Trend graph
# Requires queries "Sector", "Min", and "Max"

@app.route("/api/graph_employment_trend")
def employment_trend():
    sector: str = ""
    year_min: int = 0
    year_max: int = 9999
    
    if "sector" not in request.args:
        # Bad Request (Sector not given)
        return abort(400)
    
    sector = request.args.get("sector")
    
    # It's okay if these parameters are not provided
    if "min" in request.args: year_min = request.args.get("min")
    if "max" in request.args: year_max = request.args.get("max")
    
    plot_data = plot_to_image(Visualiser.graph_employment_trend(sector, year_min, year_max))
    if plot_data is not None:
        # Return a response as an image
        return send_file(plot_data, mimetype="image/png")

    # Bad Request (No file to return)
    return abort(400)

### graph_weekly_earnings_trend endpoint for 
# Weekly Earnings Trend graph
# Requires queries "Sector", "Min", and "Max"

@app.route("/api/graph_weekly_earnings_trend")
def weeky_earnings():
    sector: str = ""
    year_min: int = 0
    year_max: int = 9999
    
    if "sector" not in request.args:
        # Bad Request (Sector not given)
        return abort(400)
    
    sector = request.args.get("sector")
    
    # It's okay if these parameters are not provided
    if "min" in request.args: year_min = request.args.get("min")
    if "max" in request.args: year_max = request.args.get("max")
    
    plot_data = plot_to_image(Visualiser.graph_weekly_earnings_trend(sector, year_min, year_max))
    if plot_data is not None:
        # Return a response as an image
        return send_file(plot_data, mimetype="image/png")

    # Bad Request (No file to return)
    return abort(400)

### Returns all "Sectors" referenced in given data
# Parameter "key" must be supplied
# The key must be a key of the compiled_data.json dictionary

@app.route("/api/data_sectors")
def get_sectors():
    data = utils.read_json("compiled_data.json")
    key = request.args.get("key")
    
    if key not in data.keys():
        # Bad Request (Key not found in data)
        return abort(400)
    
    sectors: list[str] = [] 
    
    for n in data[key]:
        if 'Sector' not in n.keys():
            # Bad Request (This data doesn't have "Sector" data)
            return abort(400)
        
        if n['Sector'] not in sectors:
            sectors.append(n['Sector'])
    
    return sectors

### Returns all "Years" referenced in given data
# See data_sectors for parameters

@app.route("/api/data_years")
def get_years():
    data = utils.read_json("compiled_data.json")
    key = request.args.get("key")
    
    if key not in data.keys():
        # Bad Request (Key not found in data)
        return abort(400)
    
    years: list[int] = [] 
    
    for n in data[key]:
        if n['Year'] not in years:
            years.append(n['Year'])
    
    years.sort()
    return years
    
### Unit Testing
# .../api/graph_occupations?year=2017     => Image success
# .../api/graph_occupations?year=2025     => Response 400
# .../api/graph_occupations?year=-55.6    => Response 400

@app.route("/api/user_data_graph")
def user_data():
    sample_data = utils.read_json("user_form/user_data.json")[0]
    key = request.args.get("key")
    
    if key not in sample_data.keys():
        # Bad Request (Key a part of data)
        return abort(400)
    
    match key:
        case "Gender":
            plotimg = plot_to_image(Visualiser.user_data_gender())
            return send_file(plotimg, mimetype="image/png")
    
        case "Age":
            plotimg = plot_to_image(Visualiser.user_data_age())
            return send_file(plotimg, mimetype="image/png")
    
        case "AnnualIncome":
            plotimg = plot_to_image(Visualiser.user_data_payrange())
            return send_file(plotimg, mimetype="image/png")
        
        case _:
            return abort(400)

@app.route("/api/form_options")
def form_options():
    return utils.read_json("user_form/user_form_options.json")

@app.route("/api/user_form_entry")
def new_entry():
    user_data: list[dict] = utils.read_json("user_form/user_data.json")
    next_id = user_data[-1]['Id'] + 1

    user_data.append({
        "Id": next_id,
        "Gender": request.args.get("gender"),
        "Age": request.args.get("age"),
        "County": request.args.get("county"),
        "JobSector": request.args.get("sector"),
        "AnnualIncome": request.args.get("annualincome"),
        "Satisfaction": request.args.get("satisfaction")
    })

    with open("user_form/user_data.json", "w") as ud:
        ud.write(json.dumps(user_data))

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}