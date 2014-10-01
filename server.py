from flask import Flask

import subprocess


DATABASE = 'some_database.db'
DEBUG = True
SECRET_KEY = 'development key'


app = Flask(__name__)
app.config.from_object(__name__)



subprocess.Popen(['python','seeder.py'])



if __name__ == '__main__':
    app.run()