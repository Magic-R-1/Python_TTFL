import sys
sys.path.append('C:/Users/egretillat/Documents/Personnel/Code/envPython/Python_TTFL/Mon_TI')

from flask import Flask

from k_Impact_poste import *

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/TI")

def TI():
    df_impact_poste = obtenir_transposer_df_delta()
    return df_impact_poste.to_html()