import grpc
from concurrent import futures
import roster_pb2
import roster_pb2_grpc
import psycopg2

class RosterService(roster_pb2_grpc.RosterServiceServicer):
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="GRPC",
            user="postgres",
            password="1111",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()

    def GetPlayers(self, request, context):
        """Handle gRPC request to fetch players based on filters."""
        query = "SELECT * FROM roster WHERE 1=1"
        params = []

        if request.position:
            query += " AND position = %s"
            params.append(request.position)
        if request.birth_year_from:
            query += " AND EXTRACT(YEAR FROM birthday) >= %s"
            params.append(request.birth_year_from)
        if request.birth_year_to:
            query += " AND EXTRACT(YEAR FROM birthday) <= %s"
            params.append(request.birth_year_to)
        if request.weight_from:
            query += " AND weight >= %s"
            params.append(request.weight_from)
        if request.weight_to:
            query += " AND weight <= %s"
            params.append(request.weight_to)
        if request.height_from:
            query += " AND height >= %s"
            params.append(request.height_from)
        if request.height_to:
            query += " AND height <= %s"
            params.append(request.height_to)   
        
        print("Received request:", request)

        self.cursor.execute(query, params)
        players = self.cursor.fetchall()

        player_list = roster_pb2.PlayerList()
        for player in players:
            p = roster_pb2.Player(
                playerid=player[0],
                jersey=player[1],
                fname=player[2],
                sname=player[3],
                position=player[4],
                birthday=str(player[5]),
                weight=player[6],
                height=player[7],
                birthcity=player[8],
                birthstate=player[9]
            )
            player_list.players.append(p)
        return player_list

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    roster_pb2_grpc.add_RosterServiceServicer_to_server(RosterService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()