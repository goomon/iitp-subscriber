from sqlalchemy import Column, String, BigInteger
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
