from yinglong_server import app
from flask_script import Manager, Server

manager = Manager(app)

# Run local server
manager.add_command("runserver", Server("127.0.0.1", port=8000))

if __name__ == '__main__':
    manager.run()
