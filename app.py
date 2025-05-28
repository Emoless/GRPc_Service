from flask import Flask, render_template, request, jsonify
import grpc
import roster_pb2
import roster_pb2_grpc

app = Flask(__name__)

@app.route('/')
def index():
    return clubs()

@app.route('/clubs')
def clubs():
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = roster_pb2_grpc.RosterServiceStub(channel)
            response = stub.GetClubs(roster_pb2.GetClubsRequest())
            clubs = response.clubs
        return render_template('clubs.html', clubs=clubs)
    except Exception as e:
        print(f"Ошибка при получении клубов: {e}")
        return jsonify({'status': 'failure', 'error': str(e)}), 500

@app.route('/club/<club_id>')
def club_players(club_id):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = roster_pb2_grpc.RosterServiceStub(channel)
            grpc_request = roster_pb2.GetPlayersByClubRequest(ClubID=club_id)
            response = stub.GetPlayersByClub(grpc_request)
            players = response.players
        return render_template('players.html', players=players, club_id=club_id)
    except Exception as e:
        print(f"Ошибка при получении игроков: {e}")
        return jsonify({'status': 'failure', 'error': str(e)}), 500

@app.route('/update_player', methods=['POST'])
def update_player():
    try:
        print(f"Полученные данные формы: {request.form}")
        playerid = request.form['playerid']
        jersey = int(request.form['jersey']) if request.form['jersey'] else 0
        fname = request.form['fname']
        sname = request.form['sname']
        position = request.form['position']
        birthday = request.form['birthday']
        weight = int(request.form['weight']) if request.form['weight'] else 0
        height = int(request.form['height']) if request.form['height'] else 0
        birthcity = request.form['birthcity']
        birthstate = request.form['birthstate']
        club_id = request.form['ClubID']

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = roster_pb2_grpc.RosterServiceStub(channel)
            grpc_request = roster_pb2.UpdatePlayerRequest(
                playerid=playerid,
                jersey=jersey,
                fname=fname,
                sname=sname,
                position=position,
                birthday=birthday,
                weight=weight,
                height=height,
                birthcity=birthcity,
                birthstate=birthstate,
                ClubID=club_id
            )
            response = stub.UpdatePlayer(grpc_request)
            if response.success:
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'failure', 'error': 'Ошибка на сервере gRPC'}), 500
    except Exception as e:
        print(f"Ошибка в update_player: {e}")
        return jsonify({'status': 'failure', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)