from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
session = Session(engine, expire_on_commit=True, autoflush=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]


Base.metadata.create_all(engine)

user = User(id=1, name="Test", age=30)
# user2 = User(id=1, name="Test", age=30)
# insp = inspect(user)
session.add(user)
session.flush()


# session.add(user2)
# session.flush()
# print(insp.transient)
# print(insp.pending)
# print(insp.persistent)
# session.delete(user)
# session.flush()
# print(insp.deleted)
# print(session.new)
# session.execute(select(User))
# user.age = 25
# print(user in session.dirty)
# session.flush()

# session_user = session.get(User, 1)
# print(user == session_user)

user_from_db = session.scalar(select(User).where(User.id == 1))
print(user_from_db == user)