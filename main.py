from flask import render_template

from simple_HMS import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)