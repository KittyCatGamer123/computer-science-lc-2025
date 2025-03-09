from flask import Flask, request, send_file, abort
from matplotlib import figure
import io

import visualisation.visualiser as Visualiser
import utils

app = Flask(__name__)

# Takes in a visualised plot and returns an Image class
def plot_to_image(fig: figure) -> bytes:
    if fig is None:
        return None
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
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
    return open("artefact.js", "r").read(), 200, {'Content-Type': 'text/javascript'}

# Add "artefact.html" to the virtual file system
@app.route("/")
def frontend_html():
    return open("artefact.html", "r").read()


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
        return send_file(plot_data, mimetype="image/png")

    return abort(400)

@app.route("/api/graph_weekly_earnings_trend")
def weeky_earnings():
    sector: str = ""
    year_min: int = 0
    year_max: int = 9999
    
    if "sector" not in request.args:
        return abort(400)
    
    sector = request.args.get("sector")
    
    if "min" in request.args: year_min = request.args.get("min")
    if "max" in request.args: year_max = request.args.get("max")
    
    plot_data = plot_to_image(Visualiser.graph_weekly_earnings_trend(sector, year_min, year_max))
    if plot_data is not None:
        return send_file(plot_data, mimetype="image/png")

    return abort(400)

@app.route("/api/data_sectors")
def get_sectors():
    data = utils.read_json("compiled_data.json")
    key = request.args.get("key")
    
    if key not in data.keys():
        return abort(400)
    
    sectors: list[str] = [] 
    
    for n in data[key]:
        if 'Sector' not in n.keys():
            return abort(400)
        
        if n['Sector'] not in sectors:
            sectors.append(n['Sector'])
    
    return sectors

@app.route("/api/data_years")
def get_years():
    data = utils.read_json("compiled_data.json")
    key = request.args.get("key")
    
    if key not in data.keys():
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