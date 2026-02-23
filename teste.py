from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://postgres:81848938spM!@localhost:5432/db_crud")
connection = engine.connect()
print("Conectou!")
connection.close()