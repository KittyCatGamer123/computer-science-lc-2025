from flask import Flask, request, send_file, abort
from matplotlib import figure
import io

import visualisation.visualiser as Visualiser

app = Flask(__name__)

# Takes in a visualised plot and returns an Image class
def plot_to_image(fig: figure) -> bytes:
    if fig is None:
        return None
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Add "artefact.html" to the virtual file system
@app.route("/")
def frontend_html():
    return open("artefact.html", "r").read()

# Add "artefact.js" to the virtual file system
# in which can be used in a <script> tag
@app.route("/artefact.js")
def frontend_js():
    return open("artefact.js", "r").read()

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
    
### Unit Testing
# .../api/graph_occupations?year=2017     => Image success
# .../api/graph_occupations?year=2025     => Response 400
# .../api/graph_occupations?year=-55.6    => Response 400