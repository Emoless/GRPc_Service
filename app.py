from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return clubs()

@app.route('/clubs')
def clubs():
    try:
        response = requests.get('http://127.0.0.1:5001/clubs')
        response.raise_for_status()  # Проверяем успешность запроса
        clubs = response.json()
        print(f"Полученные данные клубов: {clubs}")  # Для отладки
        return render_template('clubs.html', clubs=clubs)
    except requests.RequestException as e:
        print(f"Ошибка при получении клубов: {e}")
        return jsonify({'status': 'failure', 'error': str(e)}), 500

@app.route('/club/<club_id>')
def club_players(club_id):
    try:
        response = requests.get(f'http://127.0.0.1:5001/clubs/{club_id}/players')
        response.raise_for_status()
        players = response.json()
        print(f"Полученные данные игроков: {players}")  # Для отладки
        return render_template('players.html', players=players, club_id=club_id)
    except requests.RequestException as e:
        print(f"Ошибка при получении игроков: {e}")
        return jsonify({'status': 'failure', 'error': str(e)}), 500

@app.route('/update_player', methods=['POST'])
def update_player():
    try:
        player_id = request.form['playerid']
        data = {
            'playerid': request.form['playerid'],
            'jersey': int(request.form['jersey']) if request.form['jersey'] else None,
            'fname': request.form['fname'],
            'sname': request.form['sname'],
            'position': request.form['position'],
            'birthday': request.form['birthday'],
            'weight': int(request.form['weight']) if request.form['weight'] else None,
            'height': int(request.form['height']) if request.form['height'] else None,
            'birthcity': request.form['birthcity'],
            'birthstate': request.form['birthstate'],
            'clubid': request.form['clubid']
        }
        print(f"Отправляемые данные для обновления: {data}")  # Для отладки
        response = requests.put(f'http://127.0.0.1:5001/players/{player_id}', json=data)
        response.raise_for_status()
        return jsonify({'status': 'success'})
    except (requests.RequestException, ValueError) as e:
        print(f"Ошибка при обновлении игрока: {e}")
        return jsonify({'status': 'failure', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)