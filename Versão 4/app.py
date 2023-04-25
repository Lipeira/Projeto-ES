from flask import Flask, render_template, request, redirect, url_for, blueprints, Blueprint
from views import views
import psycopg2

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    app.run(debug=True)
