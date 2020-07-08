"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Sweet-Cupcakes'

connect_db(app)

# ================ PART FIVE ================ #


@app.route("/", methods=["GET"])
def get_all():
    """index route - List all cupcakes from DB"""

    return render_template("index.html")


# ================= PART TWO ================= #


@app.route("/api/cupcakes", methods=["GET"])
def show_all_cupcakes():
    """Show all cupcake listings"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes/<int:id>", methods=["GET"])
def show_one_cupcake(id):
    """Show details of one cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes", methods=["POST"])
def add_cupcake():
    """Add a cupcake to the database"""
    new_cupcake = Cupcake(flavor=request.json["flavor"],
                          size=request.json["size"], rating=request.json["rating"], image=(request.json["image"] or None))
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake=new_cupcake.serialize()), 201)


# ================ PART THREE ================ #


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Edit single cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    """save info from form as json to var"""
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def del_cupcake(id):
    """Delete single cupcake"""
    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Cupcake Deleted")
