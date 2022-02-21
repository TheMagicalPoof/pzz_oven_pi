#!/bin/env python
from project import create_app, socketio

project = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(project)