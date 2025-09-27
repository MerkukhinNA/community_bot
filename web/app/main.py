import uvicorn, os
from api.app import app


# Просто начальная настройка БД
# from db.db_manager import db
# db.start_setup()

def main() -> None:
    uvicorn.run(app=app, host=os.environ['APP_HOST'], port=int(os.environ['APP_PORT']))

if __name__ == "__main__":
    main()