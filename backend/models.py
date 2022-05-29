from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String

Base = declarative_base()

# Mapping classes


class Room(Base):
    """SQL Table for rooms"""

    __tablename__ = "rooms"

    id = Column(String, primary_key=True)
    admin_id = Column(String)
    locked = Column(Integer)
    answer = Column(String)
    timer = Column(Integer)
    max_lives = Column(Integer)
    question = Column(Integer)

    def __repr__(self) -> str:
        r = f"Room(id={self.id}, admin_id={self.admin_id}, locked={self.locked}, answer={self.answer}, timer={self.timer}, max_lives={self.max_lives}, question={self.question})\n"
        players = ""
        for player in self.players:
            players += f" - {repr(player)}\n"
        return r + players


class Player(Base):
    """SQL Table for players"""

    __tablename__ = "players"

    room = Column(String, ForeignKey("rooms.id"))
    sid = Column(String, primary_key=True)
    name = Column(String)
    answer = Column(String)
    hearts = Column(Integer)
    death_at = Column(Integer)
    disconnected = Column(Integer, default=0)

    player = relationship("Room", back_populates="players")

    def __repr__(self) -> str:
        return f"Player(name={self.name}, sid={self.sid}, answer={self.answer}, hearts={self.hearts}, death_at={self.death_at}, disconnected={self.disconnected == 1})"

    def to_dict(self) -> dict:
        return {
            "id": self.sid,
            "name": self.name,
            "answer": self.answer,
            "hearts": self.hearts,
            "deathAt": self.death_at,
            "disconnected": self.disconnected == 1,
        }


Room.players = relationship("Player", order_by=Player.sid, back_populates="player")
