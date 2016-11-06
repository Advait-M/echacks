from flask import *
import pyredb as pydb
app = Flask(__name__)

@app.route('/')
def index():
    data = pydb.LogiticaPolitica().getAll()
    #data = "asdad"
    return render_template("index.html", data = data)
if __name__ == "__main__":

    app.run()
    pydb.LogiticaPolitica().start()