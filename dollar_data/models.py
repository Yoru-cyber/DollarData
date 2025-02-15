from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, REAL

from dollar_data.database import Base


class Dollar(Base):
    __tablename__ = "HistoricalDollar"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(50))
    currency: Mapped[str] = mapped_column(String(3))
    buybid: Mapped[float] = mapped_column(REAL)

    def __repr__(self) -> str:
        return f"Dollar(id={self.id!r}, date={self.date!r}, currency={self.currency!r}, buybid={self.buybid!r})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
