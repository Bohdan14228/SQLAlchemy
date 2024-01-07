from sqlalchemy import create_engine, inspect, select, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship, joinedload

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

session = Session(engine, expire_on_commit=True, autoflush=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]

    addresses: Mapped[list["Address"]] = relationship(back_populates="user", uselist=True, lazy="selectin")
    # addresses: Mapped[list["Address"]] = relationship(back_populates="users", uselist=True, secondary='user_address')

    def __repr__(self) -> str:
        return f"User: {self.id}:{self.name=}:{self.age}"


class Address(Base):
    __tablename__ = 'addresses'
    email: Mapped[str] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="addresses", uselist=False)
    # users: Mapped[list["User"]] = relationship(back_populates="addresses", uselist=True, secondary='user_address')
    user_fk: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"Addresses: {self.email=}:{self.user_fk=}"


# class UserAddress(Base):
#     __tablename__ = 'user_address'
#     user_fk = mapped_column(ForeignKey('users.id'), primary_key=True)
#     address_fk = mapped_column(ForeignKey('addresses.email'), primary_key=True)
#
#     def __repr__(self) -> str:
#         return f"UserAddress: {self.user_fk=}:{self.address_fk=}"


Base.metadata.create_all(engine)


user = User(id=1, name='Test', age=30)
address = Address(email="test@test.com")
address2 = Address(email="test2@test.com")
user.addresses.append(address)
user.addresses.append(address2)
session.add(user)
session.commit()

user = session.scalar(select(User))
print(user)
print(user.addresses)
# users = session.scalars(select(User).options(joinedload(User.addresses))).unique().all()
# user_secondary = session.scalars(select(UserAddress)).all()
# # addresses = session.scalars(select(Address)).all()
#
# print(user)
# # print(addresses)
# print([user.addresses for user in users])
# print(user_secondary)