from sqlalchemy import Column, String, BigInteger, Double, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class EndRecord(Base):
    __tablename__ = "end_record"

    id = Column(
        BigInteger,
        primary_key=True
    )
    connection_id = Column(
        String(255),
        nullable=False,
    )
    timestamp = Column(
        BigInteger,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"ConsumerRecord(id={self.id}, consume_time={self.timestamp})"


class User(Base):
    __tablename__ = "users"

    id = Column(
        BigInteger,
        primary_key=True
    )
    age = Column(
        BigInteger,
        nullable=False,
    )
    gender = Column(
        String(255),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, age={self.age}, gender={self.gender})"


class SensorChest(Base):
    __tablename__ = "sensor_chests"

    id = Column(
        BigInteger,
        primary_key=True
    )
    user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
    )
    ecg = Column(
        Double,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"SensorChest(user_id={self.user_id})"
