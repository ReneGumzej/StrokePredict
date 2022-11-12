import sys

from webapp import app

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--docker":
        app.run(host='0.0.0.0')
    else:
        app.run(debug=True)
