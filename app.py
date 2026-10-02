
import os
import sqlite3

from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    session,
    redirect,
    url_for
)

from dotenv import load_dotenv


# تحميل معلومات ملف .env
load_dotenv()


app = Flask(__name__)


# معلومات الأمان من .env
app.secret_key = os.getenv("SECRET_KEY")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


# إنشاء قاعدة البيانات والجدول
def create_database():

    connection = sqlite3.connect("restaurant.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            people INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            phone TEXT NOT NULL,
            notes TEXT
        )
    """)

    connection.commit()

    connection.close()


# الصفحة الرئيسية
@app.route("/")
def home():

    return render_template("index.html")


# تسجيل الدخول
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )


        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            session["admin_logged_in"] = True

            return redirect(
                url_for("admin")
            )


        return render_template(
            "login.html",
            error="اسم المستخدم أو كلمة المرور غير صحيحة"
        )


    return render_template("login.html")


# تسجيل الخروج
@app.route("/logout")
def logout():

    session.pop(
        "admin_logged_in",
        None
    )

    return redirect(
        url_for("login")
    )


# استقبال الحجز
@app.route("/booking", methods=["POST"])
def booking():

    data = request.get_json()


    if not data:

        return jsonify({
            "error":
                "لم يتم إرسال البيانات"
        }), 400


    name = data.get(
        "name",
        ""
    ).strip()

    people = data.get("people")

    date = data.get(
        "date",
        ""
    ).strip()

    time = data.get(
        "time",
        ""
    ).strip()

    phone = data.get(
        "phone",
        ""
    ).strip()

    notes = data.get(
        "notes",
        ""
    ).strip()


    # التحقق من الاسم
    if not name:

        return jsonify({
            "error":
                "الاسم مطلوب"
        }), 400


    if len(name) > 100:

        return jsonify({
            "error":
                "الاسم طويل جداً"
        }), 400


    # التحقق من عدد الأشخاص
    try:

        people = int(people)

    except (TypeError, ValueError):

        return jsonify({
            "error":
                "عدد الأشخاص غير صحيح"
        }), 400


    if people < 1 or people > 50:

        return jsonify({
            "error":
                "عدد الأشخاص يجب أن يكون بين 1 و50"
        }), 400


    # التحقق من التاريخ
    if not date:

        return jsonify({
            "error":
                "التاريخ مطلوب"
        }), 400


    # التحقق من الوقت
    if not time:

        return jsonify({
            "error":
                "الوقت مطلوب"
        }), 400


    # التحقق من الهاتف
    if not phone:

        return jsonify({
            "error":
                "رقم الهاتف مطلوب"
        }), 400


    if (
        not phone.startswith(("05", "06", "07"))
        or len(phone) != 10
        or not phone.isdigit()
    ):

        return jsonify({
            "error":
                "رقم الهاتف المغربي غير صحيح"
        }), 400


    # التحقق من الملاحظات
    if len(notes) > 500:

        return jsonify({
            "error":
                "الملاحظات طويلة جداً"
        }), 400


    # حفظ الحجز
    connection = sqlite3.connect(
        "restaurant.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        INSERT INTO bookings
        (name, people, date, time, phone, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        people,
        date,
        time,
        phone,
        notes
    ))


    connection.commit()

    connection.close()


    print(
        "Booking saved successfully!"
    )


    return jsonify({
        "message":
            "Booking saved successfully!"
    })


# عرض الحجوزات
@app.route("/bookings")
def get_bookings():

    if "admin_logged_in" not in session:

        return redirect(
            url_for("login")
        )


    connection = sqlite3.connect(
        "restaurant.db"
    )

    cursor = connection.cursor()


    cursor.execute(
        "SELECT * FROM bookings"
    )


    bookings = cursor.fetchall()


    connection.close()


    return render_template(
        "bookings.html",
        bookings=bookings
    )


# حذف حجز
@app.route(
    "/delete-booking/<int:booking_id>",
    methods=["POST"]
)
def delete_booking(booking_id):

    if "admin_logged_in" not in session:

        return jsonify({
            "error":
                "غير مصرح لك"
        }), 403


    connection = sqlite3.connect(
        "restaurant.db"
    )

    cursor = connection.cursor()


    cursor.execute(
        "DELETE FROM bookings WHERE id = ?",
        (booking_id,)
    )


    connection.commit()

    connection.close()


    return jsonify({
        "message":
            "تم حذف الحجز بنجاح"
    })


# تعديل حجز
@app.route(
    "/edit-booking/<int:booking_id>",
    methods=["PUT"]
)
def edit_booking(booking_id):

    if "admin_logged_in" not in session:

        return jsonify({
            "error":
                "غير مصرح لك"
        }), 403


    data = request.get_json()


    if not data:

        return jsonify({
            "error":
                "لم يتم إرسال البيانات"
        }), 400


    name = data.get(
        "name",
        ""
    ).strip()

    people = data.get("people")

    date = data.get(
        "date",
        ""
    ).strip()

    time = data.get(
        "time",
        ""
    ).strip()

    phone = data.get(
        "phone",
        ""
    ).strip()

    notes = data.get(
        "notes",
        ""
    ).strip()


    if not name:

        return jsonify({
            "error":
                "الاسم مطلوب"
        }), 400


    if len(name) > 100:

        return jsonify({
            "error":
                "الاسم طويل جداً"
        }), 400


    try:

        people = int(people)

    except (TypeError, ValueError):

        return jsonify({
            "error":
                "عدد الأشخاص غير صحيح"
        }), 400


    if people < 1 or people > 50:

        return jsonify({
            "error":
                "عدد الأشخاص يجب أن يكون بين 1 و50"
        }), 400


    if not date:

        return jsonify({
            "error":
                "التاريخ مطلوب"
        }), 400


    if not time:

        return jsonify({
            "error":
                "الوقت مطلوب"
        }), 400


    if not phone:

        return jsonify({
            "error":
                "رقم الهاتف مطلوب"
        }), 400


    if (
        not phone.startswith(
            ("05", "06", "07")
        )
        or len(phone) != 10
        or not phone.isdigit()
    ):

        return jsonify({
            "error":
                "رقم الهاتف المغربي غير صحيح"
        }), 400


    if len(notes) > 500:

        return jsonify({
            "error":
                "الملاحظات طويلة جداً"
        }), 400


    connection = sqlite3.connect(
        "restaurant.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        UPDATE bookings

        SET
            name = ?,
            people = ?,
            date = ?,
            time = ?,
            phone = ?,
            notes = ?

        WHERE id = ?
    """, (
        name,
        people,
        date,
        time,
        phone,
        notes,
        booking_id
    ))


    connection.commit()

    connection.close()


    return jsonify({
        "message":
            "تم تعديل الحجز بنجاح"
    })


# لوحة التحكم
@app.route("/admin")
def admin():

    if "admin_logged_in" not in session:

        return redirect(
            url_for("login")
        )


    connection = sqlite3.connect(
        "restaurant.db"
    )

    cursor = connection.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM bookings"
    )

    total_bookings = cursor.fetchone()[0]


    cursor.execute("""
        SELECT *
        FROM bookings
        ORDER BY id DESC
        LIMIT 5
    """)

    latest_bookings = cursor.fetchall()


    connection.close()


    return render_template(
        "admin.html",
        total_bookings=total_bookings,
        latest_bookings=latest_bookings
    )


# تشغيل Flask
if __name__ == "__main__":

    create_database()

    app.run(debug=True)