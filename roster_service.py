import grpc
from concurrent import futures
import roster_pb2
import roster_pb2_grpc
import psycopg2
import psycopg2.extras

class RosterService(roster_pb2_grpc.RosterServiceServicer):
    def __init__(self):
        # Connect to your PostgreSQL database
        self.conn = psycopg2.connect(
            dbname='GRPC',      # Replace with your database name
            user='postgres',        # Replace with your username
            password='1111',    # Replace with your password
            host='localhost',       # Replace with your host
            port='5432'             # Replace with your port
        )
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def GetClubs(self, request, context):
        self.cursor.execute("SELECT clubid, clubname, foundedyear, city, country FROM clubs")
        clubs = [roster_pb2.Club(
            ClubID=row['clubid'],
            ClubName=row['clubname'],
            FoundedYear=row['foundedyear'] if row['foundedyear'] is not None else 0,
            City=row['city'] if row['city'] is not None else '',
            Country=row['country'] if row['country'] is not None else ''
        ) for row in self.cursor.fetchall()]
        return roster_pb2.ClubList(clubs=clubs)

    # Example: If you have GetPlayersByClub
    def GetPlayersByClub(self, request, context):
        self.cursor.execute(
            "SELECT playerid, jersey, fname, sname, position, birthday, weight, height, birthcity, birthstate, clubid "
            "FROM roster WHERE clubid = %s OR (clubid IS NULL AND %s IS NULL)",
            (request.ClubID, request.ClubID)
        )
        players = [roster_pb2.Player(
            playerid=row['playerid'],
            jersey=row['jersey'] if row['jersey'] is not None else 0,
            fname=row['fname'] if row['fname'] is not None else '',
            sname=row['sname'] if row['sname'] is not None else '',
            position=row['position'] if row['position'] is not None else '',
            birthday=str(row['birthday']) if row['birthday'] is not None else '',
            weight=row['weight'] if row['weight'] is not None else 0,
            height=row['height'] if row['height'] is not None else 0,
            birthcity=row['birthcity'] if row['birthcity'] is not None else '',
            birthstate=row['birthstate'] if row['birthstate'] is not None else '',
            ClubID=row['clubid'] if row['clubid'] is not None else ''
        ) for row in self.cursor.fetchall()]
        return roster_pb2.PlayerList(players=players)

    # Example: If you have UpdatePlayer
    def UpdatePlayer(self, request, context):
        try:
            self.cursor.execute("""
                UPDATE roster
                SET jersey = %s, fname = %s, sname = %s, position = %s, birthday = %s,
                    weight = %s, height = %s, birthcity = %s, birthstate = %s, clubid = %s
                WHERE playerid = %s
            """, (
                request.jersey, request.fname, request.sname, request.position, request.birthday,
                request.weight, request.height, request.birthcity, request.birthstate, request.ClubID,
                request.playerid
            ))
            self.conn.commit()
            return roster_pb2.UpdatePlayerResponse(success=True)
        except Exception as e:
            print(f"Ошибка обновления игрока: {e}")
            self.conn.rollback()
            return roster_pb2.UpdatePlayerResponse(success=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    roster_pb2_grpc.add_RosterServiceServicer_to_server(RosterService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()