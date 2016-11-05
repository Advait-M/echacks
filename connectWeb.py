from flask import Flask, render_template
import pyredb as pydb

app = Flask(__name__)
@app.route("/")
def index():
    print("a")
    data = pydb.LogiticaPolitica().getAll()
    print(data)
    return render_template("index.html", data = data)

if __name__ == "__main__":
    pydb.LogiticaPolitica().start()
    app.run()
