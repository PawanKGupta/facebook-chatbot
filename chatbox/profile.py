from flask import Flask, render_template

app = Flask(__name__)


@app.route("/profile/")
def profile():
    return render_template("index.html", name="pawan")

@app.route("/profile/test.js")
def test():
	return True


if __name__ == "__main__":
    app.run(debug = True)
