from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import DictCursor
from typing import List, Dict, Any

app = FastAPI()

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname='GRPC',
    user='postgres',
    password='1111',
    host='localhost',
    port='5432'
)
cursor = conn.cursor(cursor_factory=DictCursor)

# Модели Pydantic для валидации данных
class Club(BaseModel):
    clubid: str
    clubname: str
    foundedyear: int | None = None
    city: str | None = None
    country: str | None = None

class Player(BaseModel):
    playerid: str
    jersey: int | None = None
    fname: str | None = None
    sname: str | None = None
    position: str | None = None
    birthday: str | None = None
    weight: int | None = None
    height: int | None = None
    birthcity: str | None = None
    birthstate: str | None = None
    clubid: str | None = None

# Эндпоинты для клубов
@app.get("/clubs", response_model=List[Dict[str, Any]])
async def get_clubs():
    cursor.execute("SELECT clubid, clubname, foundedyear, city, country FROM clubs")
    clubs = cursor.fetchall()
    return [dict(club) for club in clubs]

@app.get("/clubs/{club_id}", response_model=Dict[str, Any])
async def get_club(club_id: str):
    cursor.execute("SELECT clubid, clubname, foundedyear, city, country FROM clubs WHERE clubid = %s", (club_id,))
    club = cursor.fetchone()
    if club:
        return dict(club)
    raise HTTPException(status_code=404, detail="Club not found")

@app.post("/clubs", status_code=201)
async def create_club(club: Club):
    cursor.execute("""
        INSERT INTO clubs (clubid, clubname, foundedyear, city, country) 
        VALUES (%s, %s, %s, %s, %s)
    """, (club.clubid, club.clubname, club.foundedyear, club.city, club.country))
    conn.commit()
    return {"status": "success"}

@app.put("/clubs/{club_id}")
async def update_club(club_id: str, club: Club):
    cursor.execute("""
        UPDATE clubs 
        SET clubname = %s, foundedyear = %s, city = %s, country = %s
        WHERE clubid = %s
    """, (club.clubname, club.foundedyear, club.city, club.country, club_id))
    conn.commit()
    return {"status": "success"}

@app.delete("/clubs/{club_id}")
async def delete_club(club_id: str):
    cursor.execute("DELETE FROM clubs WHERE clubid = %s", (club_id,))
    conn.commit()
    return {"status": "success"}

# Эндпоинт для игроков клуба
@app.get("/clubs/{club_id}/players", response_model=List[Dict[str, Any]])
async def get_players_by_club(club_id: str):
    cursor.execute("SELECT playerid, jersey, fname, sname, position, birthday, weight, height, birthcity, birthstate, clubid FROM roster WHERE clubid = %s", (club_id,))
    players = cursor.fetchall()
    return [dict(player) for player in players]

# Эндпоинт для обновления игрока
@app.put("/players/{player_id}")
async def update_player(player_id: str, player: Player):
    cursor.execute("""
        UPDATE roster 
        SET jersey = %s, fname = %s, sname = %s, position = %s, birthday = %s,
            weight = %s, height = %s, birthcity = %s, birthstate = %s, clubid = %s
        WHERE playerid = %s
    """, (
        player.jersey, player.fname, player.sname, player.position, player.birthday,
        player.weight, player.height, player.birthcity, player.birthstate, player.clubid,
        player_id
    ))
    conn.commit()
    return {"status": "success"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)