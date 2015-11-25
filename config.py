import web
db_filename = "config.db"
DB = web.database(dbn='sqlite', db=db_filename)
