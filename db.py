from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from sqlalchemy import create_engine, select, and_
from sqlalchemy import Integer, String, Date, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app import input_date


class Base(DeclarativeBase):
    pass


class Log(Base):
    __tablename__ = 'Log'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ip: Mapped[str] = mapped_column(String(16), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    time: Mapped[Time] = mapped_column(Time, nullable=False)
    timezone: Mapped[str] = mapped_column(String(20), nullable=False)
    request_method: Mapped[str] = mapped_column(String(20), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    bytes_sent: Mapped[int] = mapped_column(Integer, nullable=False)


def create_rows(new_data, engine):
    with Session(engine) as session:
        for row in new_data:
            session.add(Log(
                ip=row[0],
                date=datetime.strptime(row[1], '%d/%b/%Y').date(),
                time=datetime.strptime(row[2], '%H:%M:%S').time(),
                timezone=row[3],
                request_method=row[4],
                path=row[5],
                status=int(row[6]),
                bytes_sent=int(row[7])
            ))

        session.commit()


def change_db(new_data, config):
    engine = create_engine(
        f"postgresql+psycopg2://{config['username']}:{config['password']}@{config['host_port']}/{config['db']}")
    inspector = inspect(engine)
    if not inspector.has_table('Log'):
        Base.metadata.create_all(bind=engine)
    create_rows(new_data, engine)


def get_data_db(parametr, config):
    engine = create_engine(
        f"postgresql+psycopg2://{config['username']}:{config['password']}@{config['host_port']}/{config['db']}")
    with Session(engine) as session:
        if parametr == '1':
            ip = input('\n\nВведите ip (255.255.255.255)\n>_ ').strip()
            stmt = select(Log).where(Log.ip == ip)
        elif parametr == '2':
            date = input_date()
            stmt = select(Log).where(Log.date == date)
        else:
            start_date = input_date()
            end_date = input_date()
            stmt = select(Log).where(
                and_(Log.date >= start_date, Log.date <= end_date))
        data = [log for log in session.scalars(stmt)]
        return data

