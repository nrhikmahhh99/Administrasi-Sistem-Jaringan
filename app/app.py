from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)

# Konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class Tas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255))
    harga = db.Column(db.String(255))
    deskripsi = db.Column(db.String(255))
    gambar_url = db.Column(db.String(255))
    shopee_link = db.Column(db.String(255))

# Home
@app.route("/")
def home():
    return render_template("home.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    tas_list = Tas.query.all()
    return render_template("list.html", tas_list=tas_list)

# Form Tambah
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        tas = Tas(
            nama=request.form['nama'],
            harga=request.form['harga'],
            deskripsi=request.form['deskripsi'],
            gambar_url=request.form['gambar_url'],
            shopee_link=request.form['shopee_link']
        )
        db.session.add(tas)
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("create.html")

# Form Edit
@app.route("/edit/<int:tas_id>", methods=["GET", "POST"])
def edit(tas_id):
    tas = Tas.query.get_or_404(tas_id)
    if request.method == "POST":
        tas.nama = request.form['nama']
        tas.harga = request.form['harga']
        tas.deskripsi = request.form['deskripsi']
        tas.gambar_url = request.form['gambar_url']
        tas.shopee_link = request.form['shopee_link']
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("edit.html", tas=tas)

# Hapus
@app.route("/delete/<int:tas_id>")
def delete(tas_id):
    tas = Tas.query.get_or_404(tas_id)
    db.session.delete(tas)
    db.session.commit()
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
