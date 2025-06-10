from sqlalchemy import text
from DB import engine

def instalar_triggers():
    with engine.connect() as conn:
        with open("triggers/triggers.sql", "r") as file:
            trigger_sql = file.read()
            conn.execute(text(trigger_sql))
    print("✅ Triggers instaladas com sucesso.")

if __name__ == "__main__":
    instalar_triggers()
