from flask import Flask, request, redirect, render_template, url_for, jsonify, session
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from hops import *
import config

app = Flask(__name__)
Bootstrap(app)

app.secret_key = config.secret_key

app.config.update(dict(
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = config.mail_username,
    MAIL_PASSWORD = config.mail_password
))
mail = Mail(app)

@app.before_first_request
def create_user():
    if "user" not in session:
        #ip = jsonify({'ip': request.remote_addr}), 200
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        session["user"] = ip

@app.route("/", methods=["GET", "POST"])
def calculate():

    if request.method == "POST":

        hops_amount = request.values.get("hops_amount", type=float)
        session["hops_amount"] = hops_amount
        alpha_percent = request.values.get("alpha_percent", type=float)
        session["alpha_percent"] = alpha_percent
        boiling_time = request.values.get("boiling_time", type=float)
        session["boiling_time"] = boiling_time

        IBU = calc_ibu(hops_amount, alpha_percent, boiling_time)
        if request.form.get("calculate_button") == "True":
            return render_template("index.html", page="calculate_ibu",
                                                 calc=True,
                                                 ibu=IBU,
                                                 hops_amount=session["hops_amount"],
                                                 alpha_percent=session["alpha_percent"],
                                                 boiling_time=session["boiling_time"])

    return render_template("index.html", page="calculate_ibu", calc=False, ibu=0)

@app.route("/hops_explorer_name", methods=["GET", "POST"])
def hops_explorer_name():
    df = get_data()
    df = get_sort("Name", df)
    return render_template("index.html", page="display_hops_table", data_type='Name', data=df)

@app.route("/hops_explorer_alpha_ascending", methods=["GET", "POST"])
def hops_explorer_alpha_ascending():
    df = get_data()
    df = get_sort("alpha_ascending", df)
    return render_template("index.html", page="display_hops_table", data_type='alpha_ascending', data=df)

@app.route("/hops_explorer_alpha_descending", methods=["GET", "POST"])
def hops_explorer_alpha_descending():
    df = get_data()
    df = get_sort("alpha_descending", df)
    return render_template("index.html", page="display_hops_table", data_type='alpha_descending', data=df)

@app.route("/hops_explorer_beta_ascending", methods=["GET", "POST"])
def hops_explorer_beta_ascending():
    df = get_data()
    df = get_sort("beta_ascending", df)
    return render_template("index.html", page="display_hops_table", data_type='beta_ascending', data=df)

@app.route("/hops_explorer_beta_descending", methods=["GET", "POST"])
def hops_explorer_beta_descending():
    df = get_data()
    df = get_sort("beta_descending", df)
    return render_template("index.html", page="display_hops_table", data_type='beta_descending', data=df)

@app.route("/beer_styles", methods=["GET", "POST"])
def beer_styles_data():
    #df = get_styles_data("name", True)
    df = get_styles_values_only()
    col_list = ["name", "flavor", "examples", "tags", "ibu", "og", "fg",  "srm", "abv", "bugu"]
    col_options = ['name', 'aroma', 'appearance', 'flavor', 'mouthfeel', 'impression',
       'comments', 'history', 'ingredients', 'comparison', 'examples', 'tags', 'ibu', 'og', 'fg', 'srm', 'abv', 'bugu']
    col_headers = {'name':"Name", 'aroma':"Aroma", 'appearance':"Appearance", 'flavor':"Flavor", 'mouthfeel':"Mouthfeel", 'impression':"Impression",
       'comments':"Comments", 'history':"History", 'ingredients':"Ingredients", 'comparison':"Comparison", 'examples':"Examples", 'tags':"Tags", 'ibu':"IBU", 'og':"OG", 'fg':"FG", 'srm':"SRM", 'abv':"ABV", 'bugu':"BU:GU"}

    if request.method == "POST":
        col_list = []
        for col in col_options:
            col_list.append(str(request.values.get(col)))
        return render_template("index.html", page="beer_styles", data_type='name', data=df, col_list=col_list, col_headers=col_headers, col_options=col_options)

    return render_template("index.html", page="beer_styles", data_type='name', data=df, col_list=col_list, col_headers=col_headers, col_options=col_options)

@app.route("/sources_methods", methods=["GET", "POST"])
def sources_methods():
    return render_template("index.html", page="sources_methods")

@app.route('/contact', methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.values.get("name")
        email = request.values.get("email")
        message = request.values.get("message")
        msg = Message(email, sender=email, recipients=['Joshackerman417@gmail.com'])
        msg.body = message #Customize based on user input
        mail.send(msg)
        return str(name) + "  " + str(email) + "   " + str(message)
    else:
        return render_template("index.html", page="contact")



if __name__ == "__main__":
    app.run(debug=True)
