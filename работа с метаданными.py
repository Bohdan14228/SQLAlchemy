from sqlalchemy import create_engine, MetaData, Table, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import registry, declarative_base, as_declarative, declared_attr, mapped_column, Mapped

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
# metadata = MetaData()
#
# user_table = Table(
#     "users",
#     metadata,
#     mapped_column("id", Integer, primary_key=True),
#     mapped_column("user_id", BigInteger, unique=True),
#     mapped_column("fullname", String),
# )
#
#
# address = Table(
#     "addresses",
#     metadata,
#     mapped_column("id", Integer, primary_key=True),
#     mapped_column("user_id", ForeignKey('users.user_id')),
#     mapped_column("email", String, nullable=False),
# )
#
# metadata.create_all(engine)
# metadata.drop_all(engine)


# 2 часть

# mapper_registry = registry()
# Base = declarative_base()


@as_declarative()
class AbstractModel:
    id = mapped_column(Integer, autoincrement=True, primary_key=True)

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class UserModel(AbstractModel):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column()
    fullname: Mapped[str] = mapped_column()


class AddressesModel(AbstractModel):
    __tablename__ = 'addresses'
    email = mapped_column(String, nullable=False)
    user_id = mapped_column(ForeignKey(mapped_column='users.id'))


print(UserModel.__table__.__dict__)
print(AddressesModel.__table__)
