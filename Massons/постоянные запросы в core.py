from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, insert, select, or_, and_, \
    desc, update, bindparam, delete
from sqlalchemy.dialects import mysql, oracle, postgresql, sqlite

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("first_name", String(30)),
    Column("second_name", String),
)

addresses_table = Table(
    "addresses",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("email_addresses", String(30)),
    Column("user_id", ForeignKey('users.id')),
)

metadata.create_all(engine)

stmt = insert(user_table).values(name='Test', fullname='Test test')
stmt_w0_values = insert(user_table)
sqlite_stmt = stmt_w0_values.compile(engine, sqlite.dialect())
postgresql_stmt = stmt_w0_values.compile(engine, postgresql.dialect())

with engine.begin() as conn:
    conn.execute(
        insert(user_table),
        [
            {"first_name": "Test1", "second_name": "Test1 Full"},
            {"first_name": "Test2", "second_name": "Test2 Full"},
            {"first_name": "Test3", "second_name": "Test3 Full"},
        ]
    )

    conn.execute(
        insert(addresses_table),
        [
            {"email_addresses": "test1@test.com", "user_id": 1},
            {"email_addresses": "test2@test.com", "user_id": 2},
            {"email_addresses": "test3@test.com", "user_id": 3},
        ]
    )

# with engine.begin() as conn:
#     result = conn.execute(  # .c значит что мы обращаемся к коллекции столбцов колонок
        # select(user_table.c.id, user_table.c.name).where(
        #     or_(user_table.c.name.startswith('Test2'),
        #     user_table.c.fullname.contains("3"))
        # )

        # select(
        #     user_table.c.id,
        #     (user_table.c.first_name + " " + user_table.c.second_name).label("fullname")
        # ).where(
        # user_table.c.id.in_([1, 2])
        # user_table.c.id > 1
        # )

        # select(
        #     addresses_table.c.email_addresses.label("email"),
        #     (user_table.c.first_name + " " + user_table.c.second_name).label("fullname"))
        # ).where(
        #     user_table.c.id > 1
            # ).join_from(user_table, addresses_table, user_table.c.id == addresses_table.c.user_id))
        # .join(addresses_table, isouter=True)
        # .order_by(
            # desc(user_table.c.first_name)
            # user_table.c.first_name.desc()
            # "fullname"  # можно делать сортировку по лейблам
            # "email"
        # ).group_by("email")
    # )
    # print(result.all())
    # print(result.mappings().all())  # получаем те же значения что и в result.all() только в словаре
    # for i in result:
    #     print(i)
    #     print(i.id)
    #     print(i.fullname)

    # print(result.all())


with (engine.begin() as conn):
    # stmt =  update(user_table).where(user_table.c.first_name == bindparam("old_name")
    #                                  ).values(first_name=bindparam("new_name"))
    delete_stmt = (
        delete(user_table).where(user_table.c.id.in_([1, 2, 3]))
        # .where(user_table.c.id == addresses_table.c.user_id)
        # .where(addresses_table.c.email_addresses == "test1@test.com")
        .returning(user_table.c.id)
    )

    # conn.execute(
        # update(user_table).where(user_table.c.id == 1).values(first_name="Updated Test1")
        # stmt,
        # [
        #     {"old_name": "Test1", "new_name": "New Test1"},
        #     {"old_name": "Test2", "new_name": "New Test2"},
        #     {"old_name": "Test3", "new_name": "New Test3"}
        # ]
        # delete(user_table).where(user_table.c.id == 1)
        # delete_stmt
    # )

    # print(conn.execute(select(user_table).where(user_table.c.id == 1)).all())
    # print(conn.execute(select(user_table)).all())
    result = conn.execute(delete_stmt).scalars().all()
    print(result)