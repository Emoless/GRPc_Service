from flask import Flask, render_template, request
import grpc
import roster_pb2
import roster_pb2_grpc

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page with the filter form."""
    return render_template('index.html')

@app.route('/players', methods=['POST'])
def get_players():
    """Handle form submission and fetch players via gRPC."""
    position = request.form.get('position')
    birth_year_from = request.form.get('birth_year_from')
    birth_year_to = request.form.get('birth_year_to')
    weight_from = request.form.get('weight_from')
    weight_to = request.form.get('weight_to')
    height_from = request.form.get('height_from')
    height_to = request.form.get('height_to')

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = roster_pb2_grpc.RosterServiceStub(channel)
        filter_request = roster_pb2.PlayerFilter(
            position=position if position else "",
            birth_year_from=int(birth_year_from) if birth_year_from else 0,
            birth_year_to=int(birth_year_to) if birth_year_to else 0,
            weight_from=int(weight_from) if weight_from else 0,
            weight_to=int(weight_to) if weight_to else 0,
            height_from=int(height_from) if height_from else 0,
            height_to=int(height_to) if height_to else 0
        )
        response = stub.GetPlayers(filter_request)
        players = [(p.playerid, p.jersey, p.fname, p.sname, p.position, 
                    p.birthday, p.weight, p.height, p.birthcity, p.birthstate) 
                   for p in response.players]

    return render_template('players.html', players=players)

if __name__ == '__main__':
    app.run(debug=True)