from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1988Sh@wn",
    "database": "samurai_db"
}


def get_db_connection():
    """Create and return a MySQL database connection."""
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/inventory")
def inventory():
    search = request.args.get("search", "").strip()
    conn = None
    cursor = None
    figures = []

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if search:
            query = """
                SELECT * FROM samurai_figures
                WHERE name LIKE %s OR clan LIKE %s OR material LIKE %s
                ORDER BY figure_id DESC
            """
            like_search = f"%{search}%"
            cursor.execute(query, (like_search, like_search, like_search))
        else:
            cursor.execute("SELECT * FROM samurai_figures ORDER BY figure_id DESC")

        figures = cursor.fetchall()
    except Error as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return render_template("inventory.html", figures=figures, search=search)


@app.route("/add", methods=["GET", "POST"])
def add_figure():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        clan = request.form.get("clan", "").strip()
        material = request.form.get("material", "").strip()
        height_cm = request.form.get("height_cm", "0").strip()
        price = request.form.get("price", "0").strip()
        quantity = request.form.get("quantity", "0").strip()
        description = request.form.get("description", "").strip()
        image_file = request.form.get("image_file", "samurai1.jpg").strip()

        if not name or not clan:
            flash("Name and clan are required.", "error")
            return render_template("add.html")

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO samurai_figures
                (name, clan, material, height_cm, price, quantity, description, image_file)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, clan, material, height_cm, price, quantity, description, image_file))
            conn.commit()
            flash("Figure added successfully.", "success")
            return redirect(url_for("inventory"))
        except Error as e:
            flash(f"Database error: {e}", "error")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    return render_template("add.html")


@app.route("/edit/<int:figure_id>", methods=["GET", "POST"])
def edit_figure(figure_id):
    conn = None
    cursor = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        clan = request.form.get("clan", "").strip()
        material = request.form.get("material", "").strip()
        height_cm = request.form.get("height_cm", "0").strip()
        price = request.form.get("price", "0").strip()
        quantity = request.form.get("quantity", "0").strip()
        description = request.form.get("description", "").strip()
        image_file = request.form.get("image_file", "samurai1.jpg").strip()

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE samurai_figures
                SET name=%s, clan=%s, material=%s, height_cm=%s, price=%s,
                    quantity=%s, description=%s, image_file=%s
                WHERE figure_id=%s
            """
            cursor.execute(query, (name, clan, material, height_cm, price, quantity, description, image_file, figure_id))
            conn.commit()
            flash("Figure updated successfully.", "success")
            return redirect(url_for("inventory"))
        except Error as e:
            flash(f"Database error: {e}", "error")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM samurai_figures WHERE figure_id=%s", (figure_id,))
        figure = cursor.fetchone()
        if not figure:
            flash("Figure not found.", "error")
            return redirect(url_for("inventory"))
    except Error as e:
        flash(f"Database error: {e}", "error")
        return redirect(url_for("inventory"))
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return render_template("edit.html", figure=figure)


@app.route("/delete/<int:figure_id>", methods=["POST"])
def delete_figure(figure_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM samurai_figures WHERE figure_id=%s", (figure_id,))
        conn.commit()
        flash("Figure deleted successfully.", "success")
    except Error as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return redirect(url_for("inventory"))


if __name__ == "__main__":
    app.run(debug=True)
