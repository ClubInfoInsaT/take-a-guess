from uuid import uuid4

import socketio
from gevent import pywsgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Player, Room

# FIXME: Replace later on production
sio = socketio.Server(
    cors_allowed_origins="*", logger=False, engineio_logger=False, async_mode="gevent"
)
app = socketio.WSGIApp(sio)


def make_response(status: str, message: str, **extra):
    return {"status": status, "reason": message, **extra}


@sio.on("create-room")
def onCreateRoom(sid: str, data: dict):
    """Whenever the admin creates a new room

    Args:
        sid (str): the client's socket io who emitted the event
        data (dict): data passed alongside the event
    """

    lifes = data.get("lifes", None)

    if lifes:
        query = session.query(Room).filter_by(id=room_id).first()
        if query:
            sio.emit(
                "create-room",
                data=make_response("error", "Room is already taken"),
                to=sid,
            )
        else:
            room = Room(
                id=room_id,
                admin_id=sid,
                locked=False,
                answer="",
                question=0,
                timer=0,
                max_lives=int(lifes),
            )
            session.add(room)
            sio.emit(
                "create-room",
                data=make_response("success", "Successfully created the room"),
            )


@sio.on("join-room")
def onJoinRoom(sid: str, data: dict):
    """Whenever a new player tries to join the room

    Args:
        sid (str): the user's socket iod
        data (dict): Data passed alongside the event
    """
    username = data.get("username", None)
    room = session.query(Room).filter_by(id=room_id).first()
    player = session.query(Player).filter_by(name=username).first()

    if not username:
        sio.emit(
            "join-room",
            data=make_response("error", "Unspecified username"),
            to=sid,
        )
    else:
        if room:
            if room.locked:
                sio.emit(
                    "join-room",
                    data=make_response("error", "Game has already started"),
                )
            elif player != None:
                sio.emit(
                    "join-room",
                    data=make_response("error", "This name is already taken"),
                )
            else:
                room.players.append(
                    Player(
                        sid=sid,
                        name=username,
                        answer="",
                        hearts=room.max_lives,
                        death_at=0,
                    )
                )
                sio.enter_room(sid, room=room.id)
                sio.emit(
                    "join-room",
                    data=make_response("success", "Successfully entered the lobby"),
                    to=sid,
                )

                players = [player.to_dict() for player in room.players]

                # Tell the admin a new player joined the room
                sio.emit("user-joined", data={"players": players}, to=room.admin_id)
                # Tell the players someone joined the room too
                sio.emit("user-joined", data={"players": players}, room=room.id)
        else:
            sio.emit(
                "join-room",
                data=make_response("error", "There's no room to join at the moment"),
            )


@sio.on("leave-room")
def onLeaveRoom(sid: str):
    """Whenever the admin or players leave the game once the leaderboard is shown

    Args:
        sid (str): The emitter's SID
    """
    room = session.query(Room).filter_by(id=room_id).first()
    players = session.query(Player).filter_by(room=room_id).all()

    if room:
        # If the emitter is a player then remove him from the table
        player = session.query(Player).filter_by(sid=sid).first()
        if player:
            room.players = [p for p in room.players if p.sid != player.sid]
            sio.emit("leave-room", to=sid)
        elif room.admin_id == sid:
            room.players = []
            sio.emit("leave-room", to=room.admin_id)
            session.delete(room)
            for player in players:
                session.delete(player)
    else:
        sio.emit("leave-room", to=sid)


@sio.on("get-game-info")
def get_game_info(sid: str):
    """Send various info to the players once they joined the waiting room

    Args:
        sid (str): the user's socket id
    """
    room = session.query(Room).filter_by(id=room_id).first()
    players = [player.to_dict() for player in room.players]
    settings = {"lives": room.max_lives, "timer": room.timer}
    sio.emit(
        "get-game-info",
        data={"players": players, "settings": settings, "question": room.question},
        to=sid,
    )


@sio.on("lock-room")
def lock_room(sid: str):
    """When the admin starts the game which means all the players joined the room

    Args:
        sid (str): the emitter socket id
    """

    room = session.query(Room).filter_by(id=room_id).first()
    room.locked = 1

    # Send a response to the admin
    sio.emit("lock-room-response", to=sid)

    # Tell the players to be ready
    room.question += 1
    sio.emit("be-ready", data={"question": room.question}, room=room.id)


@sio.on("get-player-info")
def get_player_info(sid: str):
    room = session.query(Room).filter_by(id=room_id).first()
    player = session.query(Player).filter_by(sid=sid).first()
    sio.emit(
        "get-player-info",
        data={
            "hearts": room.max_lives,
            "left": player.hearts,
            "timer": room.timer,
            "question": room.question,
            "isCorrect": room.answer == player.answer,
            "answer": room.answer,
        },
        to=sid,
    )


@sio.on("set-question-settings")
def set_question_settings(sid: str, data: dict):
    """Whenver the admin finish settings up the nex question

    Args:
        sid (str): the emitter's socket id
        data (dict): Data passed alongside the event
    """
    timer = data.get("timer", None)
    answer = data.get("answer", None)

    if not timer:
        sio.emit(
            "set-question-settings-response",
            data=make_response("error", "Unspecified timer value"),
            to=sid,
        )
    elif int(timer) <= 0:
        sio.emit(
            "set-question-settings-response",
            data=make_response("error", "Timer value must be a positive number"),
            to=sid,
        )
    elif answer not in ["A", "B", "C", "D"]:
        sio.emit(
            "set-question-settings-response",
            data=make_response("error", "This answer is not valid"),
            to=sid,
        )
    else:
        room = session.query(Room).filter_by(id=room_id).first()

        room.answer = answer
        room.timer = int(timer)

        # Send the response to the admin
        sio.emit(
            "set-question-settings-response",
            data=make_response("success", "Successfully set settings"),
            to=sid,
        )
        # Send a response the entire room
        sio.emit("question-start", data={"timer": timer}, room=room.id)


@sio.on("user-answer")
def user_answer(sid: str, data: dict):
    """Whenever a player just answered the question

    Args:
        sid (str): the player's socket io
        data (dict): Data passed alongside the event
    """
    answer = data.get("answer", None)

    if answer:
        room = session.query(Room).filter_by(id=room_id).first()

        player = session.query(Player).filter_by(sid=sid).first()
        player.answer = answer

        # Increase the number of turns played for player who are still alive
        if player.hearts > 0:
            player.death_at += 1

        # If th player is already dead (from  previous turn), pass
        if player.hearts == 0:
            pass
        # If the answer is incorrect remove a life if he is still alive
        elif answer != room.answer:
            if player.hearts > 0:
                player.hearts -= 1
            # Check whether the player is alive or not
            if player.hearts == 0:
                player.death_at = room.question

        # Send the answers to the admin
        dead_players = [p for p in room.players if p.hearts == 0]
        players_alive = [p for p in room.players if p.hearts > 0]
        sio.emit(
            "update-answers",
            data={
                "players": len(room.players),
                "alive": [
                    len([p for p in players_alive if p.answer == "A"]),
                    len([p for p in players_alive if p.answer == "B"]),
                    len([p for p in players_alive if p.answer == "C"]),
                    len([p for p in players_alive if p.answer == "D"]),
                    len([p for p in players_alive if p.answer == "X"]),
                ],
                "dead": [
                    len([p for p in dead_players if p.answer == "A"]),
                    len([p for p in dead_players if p.answer == "B"]),
                    len([p for p in dead_players if p.answer == "C"]),
                    len([p for p in dead_players if p.answer == "D"]),
                    len([p for p in dead_players if p.answer == "X"]),
                ],
            },
            to=room.admin_id,
        )
    else:
        print(f"An error occured while answering: '{answer}'")


@sio.on("question-stats")
def question_stats(sid: str):
    """Sends the result of the question to all players

    Args:
        sid (str): the admin's socket io
    """
    room = session.query(Room).filter_by(id=room_id).first()

    # Send the answers to the admin
    dead_players = [p for p in room.players if p.hearts == 0]
    players_alive = [p for p in room.players if p.hearts > 0]
    sio.emit(
        "question-stats",
        data={
            "players": len(room.players),
            "alive": [
                len([p for p in players_alive if p.answer == "A"]),
                len([p for p in players_alive if p.answer == "B"]),
                len([p for p in players_alive if p.answer == "C"]),
                len([p for p in players_alive if p.answer == "D"]),
                len([p for p in players_alive if p.answer == "X"]),
            ],
            "dead": [
                len([p for p in dead_players if p.answer == "A"]),
                len([p for p in dead_players if p.answer == "B"]),
                len([p for p in dead_players if p.answer == "C"]),
                len([p for p in dead_players if p.answer == "D"]),
                len([p for p in dead_players if p.answer == "X"]),
            ],
        },
        room=room.id,
    )


@sio.on("next-question")
def next_question(sid: str):
    room = session.query(Room).filter_by(id=room_id).first()
    room.question += 1

    # Emit to the admin and players
    sio.emit("next-question", to=room.admin_id)
    sio.emit("next-question", to=room.id)


@sio.on("invalidate")
def invalidate(sid: str):
    room = session.query(Room).filter_by(id=room_id).first()

    for player in room.players:
        # Restore one heart to players
        if player.hearts < room.max_lives:
            player.hearts += 1
            # FIXME: Si un joueur meurs T1, on joue 2T normalement et T3 on invalide. Le joueur mort revient à la vie ?

    # Update question progress
    room.question += 1

    # The the admin the invalidation is done
    sio.emit("invalidate", to=sid)

    # Let the players waiting in the waiting room
    sio.emit("next-question", room=room.id)


@sio.on("get-players")
def get_players(sid: str):
    room = session.query(Room).filter_by(id=room_id).first()
    players = [player.to_dict() for player in room.players]
    sio.emit("get-players", data={"players": players}, to=sid)


@sio.on("show-leaderboard")
def show_leaderboard(sid: str):
    """Show the leaderboard to the entire room

    Args:
        sid (str): the emitter's socket id
    """
    room = session.query(Room).filter_by(id=room_id).first()

    # Emit to the admin
    sio.emit("show-leaderboard", to=room.admin_id)

    # Emit to players
    sio.emit("show-leaderboard", to=room.id)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)
    # TODO: Remove disconnected player from the ROOM and emit events


if __name__ == "__main__":
    print("Starting:")
    print("\t - Creating engine...", end="")
    engine = create_engine("sqlite:///:memory:", echo=False)
    print("OK !!")

    print("\t - Creating table...", end="")
    Base.metadata.create_all(engine)
    print("OK !!")

    print("\t - Creating session...", end="")
    Session = sessionmaker()
    print("OK !!")

    print("\t - Binding to engine...", end="")
    Session.configure(bind=engine)
    session = Session()
    print("OK !!")

    room_id = str(uuid4())
    print(f"\t - ROOM ID: {room_id}\n")

    print("Socket server running: 'localhost:3001'")
    pywsgi.WSGIServer(("", 3001), app).serve_forever()
