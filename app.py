from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# Database connection configuration
conn = psycopg2.connect(
    dbname="GRPC",
    user="postgres",
    password="1111",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

@app.route('/')
def index():
    """Render the main page with the filter form."""
    return render_template('index.html')

@app.route('/players', methods=['POST'])
def get_players():
    """Handle form submission, query the database, and display results."""
    position = request.form.get('position')
    birth_year_from = request.form.get('birth_year_from')
    birth_year_to = request.form.get('birth_year_to')
    weight_from = request.form.get('weight_from')
    weight_to = request.form.get('weight_to')
    height_from = request.form.get('height_from')
    height_to = request.form.get('height_to')

    query = "SELECT * FROM roster WHERE 1=1"
    params = []

    if position:
        query += " AND position = %s"
        params.append(position)
    if birth_year_from:
        query += " AND EXTRACT(YEAR FROM birthday) >= %s"
        params.append(birth_year_from)
    if birth_year_to:
        query += " AND EXTRACT(YEAR FROM birthday) <= %s"
        params.append(birth_year_to)
    if weight_from:
        query += " AND weight >= %s"
        params.append(weight_from)
    if weight_to:
        query += " AND weight <= %s"
        params.append(weight_to)
    if height_from:
        query += " AND height >= %s"
        params.append(height_from)
    if height_to:
        query += " AND height <= %s"
        params.append(height_to)

    cursor.execute(query, params)
    players = cursor.fetchall()
    return render_template('players.html', players=players)

if __name__ == '__main__':
    app.run(debug=True)