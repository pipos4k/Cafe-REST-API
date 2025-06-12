from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, select

app = Flask(__name__)

class Base(DeclarativeBase):
  pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafe.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app=app)

class Cafe(db.Model):
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
  map_url: Mapped[str] = mapped_column(String(500), nullable=False)
  img_url: Mapped[str] = mapped_column(String(500), nullable=False)
  location: Mapped[str] = mapped_column(String(250), nullable=False)
  seats: Mapped[str] = mapped_column(String(250), nullable=False)
  has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
  has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
  has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
  can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
  coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

  def to_dict(self):
     return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.route("/random")
def get_random_cafe():
  import random
  result = db.session.execute(db.select(Cafe))
  all_cafes = result.scalars().all()
  random_cafe = random.choice(all_cafes)
  return jsonify(Cafe=random_cafe.to_dict())

@app.route("/all_cafes")
def get_all_cafes():
  result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
  all_cafes = result.scalars().all()
  all_cafes_test = db.session.query(Cafe).all()
  return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes_test])
   
@app.route("/search")
def search_cafe():
  query_location = request.args.get("loc")
  result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
  all_cafes = result.scalars().all()
  if all_cafes:
     return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
  else:
    return jsonify(error={"Not found": "Sorry, no cafe with this location."}), 404

@app.route("/add", methods=["POST"])
def post_new_cafe():
  new_cafe = Cafe(
    name=request.form.get("name"),
    map_url=request.form.get("map_url"),
    img_url=request.form.get("img_url"),
    location=request.form.get("loc"),
    has_sockets=bool(request.form.get("sockets")),
    has_toilet=bool(request.form.get("toilet")),
    has_wifi=bool(request.form.get("wifi")),
    can_take_calls=bool(request.form.get("calls")),
    seats=request.form.get("seats"),
    coffee_price=request.form.get("coffee_price"),
    )
  db.session.add(new_cafe)
  db.session.commit()
  return jsonify(response={"success": "Successfully added the new cafe."})
   
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_price(cafe_id):
  new_price = request.args.get("new_price")
  if not new_price:
    return jsonify(error={"No price": "Please provide a price."}), 400
  
  cafe = db.session.get(Cafe, cafe_id)
  if cafe is None:
    return jsonify(error={"Not found": "Sorry, no cafe with this ID."}), 404 
  
  cafe.coffee_price = new_price
  db.session.commit()
  return jsonify(response={"success:": "Successfully edit cafe's price."}), 200


import os 
from dotenv import load_dotenv
load_dotenv()
SECRET_API_KEY = os.environ.get("FLASK_API_KEY")

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
  api_key = request.args.get("api_key")
  if api_key != SECRET_API_KEY or api_key is None:
    return jsonify(error={"Wrong key": "Invalid or missing API key."}), 403
  
  cafe = db.session.get(Cafe, cafe_id)
  if cafe is None:
    return jsonify(error={"Not found": "Cafe with this ID doesn't exist."}), 404
  
  db.session.delete(cafe)
  db.session.commit()

  return jsonify(response={"success": "Cafe successfully deleted."})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ✅ This creates the Cafe table in cafe.db
    print("DB created")
    app.run(debug=True)    
