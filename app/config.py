import os
import urllib.parse

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change_this_secret_for_prod')
    # Priority order:
    # 1. DATABASE_URL (full SQLAlchemy URI, e.g. mysql+pymysql://user:pass@host:3306/dbname)
    # 2. Build from DB_USER/DB_PASS/DB_HOST/DB_PORT/DB_NAME
    # 3. Fallback to local SQLite for easy testing
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        db_user = os.environ.get('DB_USER')
        db_pass = os.environ.get('DB_PASS')
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '3306')
        db_name = os.environ.get('DB_NAME', 'taskdb')
        if db_user and db_pass:
            # quote the password and build a pymysql connection string
            database_url = f"mysql+pymysql://{db_user}:{urllib.parse.quote_plus(db_pass)}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
        else:
            database_url = 'sqlite:///' + os.path.join(basedir, 'taskdb.sqlite3')

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
