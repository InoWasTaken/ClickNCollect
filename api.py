from flask import Flask, request, jsonify


def api(app, db):
    @app.route("/<product_type>", methods=['GET'])
    def get_products(product_type):
        if product_type != 'snacks' and product_type != 'drinks':
            return "Product type not found", 404
        cursor = db.execute(
            f"SELECT name, in_stock, rowid FROM {product_type}")
        products = cursor.fetchall()
        return jsonify(products)

    @app.route("/<product_type>/<id>", methods=['PATCH'])
    def update_products(product_type, id):
        if product_type != 'snacks' and product_type != 'drinks':
            return "Product type not found", 404
        cursor = db.execute(
            f"SELECT rowid FROM {product_type} WHERE rowid = (?)", (id,))
        if cursor.fetchone() == None:
            return "Product not found", 404
        cursor = db.execute(
            f"UPDATE {product_type} SET in_stock = ? WHERE rowid = ?", (request.json['in_stock'], id))
        cursor = db.execute(
            f"SELECT name, in_stock, rowid FROM {product_type} WHERE rowid = ?", (id,))
        products = cursor.fetchone()
        return jsonify(products)
