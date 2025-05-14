from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# Cấu hình MySQL (dùng pymysql)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Cong2004!',
    'database': 'sinhvien_db',
    'cursorclass': pymysql.cursors.DictCursor
}

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    error = None
    if request.method == 'POST':
        query = request.form['query']
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
            connection.close()
        except Exception as e:
            error = str(e)
    return render_template('index.html', results=results, error=error)

if __name__ == '__main__':
    app.run(debug=True)
