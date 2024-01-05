from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)  # url по которому мы подключимся к нашей БД

with engine.connect() as connection:  # установка соединения
    result = connection.execute(text("select 'hello world'"))
    print(result.scalar_one_or_none())
