from flask import *
import os

app = Flask(__name__)

ASSETS_FOLDER = "assets"
os.makedirs(ASSETS_FOLDER, exist_ok=True)

products = {}
current_id = 1

@app.route("/product", methods=["POST"])
def create_product():
    global current_id
    data = request.get_json()

    if not data or "name" not in data or "description" not in data:
        abort(400, "invalid request")

    product = {
        "id": current_id,
        "name": data["name"],
        "description": data["description"],
        "icon": None
    }

    products[current_id] = product
    current_id += 1

    return jsonify(product), 201


@app.route("/product/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = products.get(product_id)

    if not product:
        abort(404, description="product not found")

    return jsonify(product)


@app.route("/product/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = products.get(product_id)

    if not product:
        abort(404, description="product not found")

    data = request.get_json()

    if not data:
        abort(400, description="invalid request")

    if "name" in data:
        product["name"] = data["name"]
    
    if "description" in data:
        product["description"] = data["description"]
    
    return jsonify(product)


@app.route("/product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = products.pop(product_id, None)

    if not product:
        abort(404, description="product not found")

    if product["icon"]:
        icon_path = os.path.join(ASSETS_FOLDER, product["icon"])
        if os.path.exists(icon_path):
            os.remove(icon_path)
    
    return jsonify(product)

@app.route("/products", methods=["GET"])
def get_all_products():
    return jsonify(list(products.values()))

@app.route("/product/<int:product_id>/image", methods=["POST"])
def upload_image(product_id):
    product = products.get(product_id)
    if not product:
        abort(404, description="product not found")
    
    if not request.data:
        abort(400, description="no data")

    filename = f"product_{product_id}.png"
    filepath = os.path.join(ASSETS_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(request.data)

    product["icon"] = filename

    return jsonify({"message": "image uploaded", "icon": filename})

@app.route("/product/<int:product_id>/image", methods=["GET"])
def get_image(product_id):
    product = products.get(product_id)

    if not product:
        abort(404, description="product not found")

    if not product["icon"]:
        abort(404, description="image not found")

    return send_from_directory(ASSETS_FOLDER, product["icon"])


if __name__ == "__main__":
    app.run(debug=True)