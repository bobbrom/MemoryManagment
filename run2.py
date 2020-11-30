from flask import Flask, render_template, request, jsonify, render_template
import os
import psutil
import webbrowser
import background
from shutil import copyfile
import threading


app = Flask(__name__)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def getReserved():
    folder = open("data/mainFolder.dat").read()
    files = []
    for f in os.walk(folder):
        files += [os.path.join(f[0], a) for a in f[-1]]

    return sum([os.path.getsize(a) for a in files])

def isRunning():
    f = open("data/pid_background.dat")
    pid = int(f.read())
    f.close()
    running = False
    for p in psutil.process_iter(attrs=["pid"]):
        if p.pid == pid and (p.name() == "python.exe" or p.name() == "pythonw.exe"):
            running = True
    return running


@app.route('/_add_numbers')
def add_numbers():
    f = open("data/wasFree.dat")
    wasFree = int(f.read())
    f.close()

    f = open("data/keepFree.dat")
    keepFree = int(f.read()) * 1024**3
    f.close()

    toDo = wasFree - keepFree

    hdd = psutil.disk_usage("D:\\")
    nowFree = hdd.free

    allToDo = wasFree - keepFree
    done = nowFree - keepFree

    perc = (100/allToDo)*(allToDo - done)

    done /= 1024**3
    return jsonify(result=round(perc,2), eta="Unknown", done=round(done,2))





hdd = psutil.disk_usage("D:\\")
folder = open("data/mainFolder.dat").read()


def getReserved():
    folder = open("data/mainFolder.dat").read()
    files = []
    for f in os.walk(folder):
        files += [os.path.join(f[0], a) for a in f[-1]]

    return sum([os.path.getsize(a) for a in files])


@app.route("/")
def index():
    hdd = psutil.disk_usage("D:\\")

    reserved = getReserved()

    total = hdd.total
    used  = hdd.used - reserved
    free  = hdd.free

    reservedPerc = round((100/total)*reserved,2)
    usedPerc     = round((100/total)*used,2)
    freePerc     = round((100/total)*free,2)



    running_checked = ""
    if(isRunning()):
        running_checked = "checked"

    run_on_startup = ""
    if( os.path.exists(os.path.join(os.getenv('ProgramData'),"Microsoft\\Windows\\Start Menu\\Programs\\StartUp","MemoryManagment.bat")) ):
        run_on_startup = "checked"
    available = round((reserved + free) / 1024**3)
    return render_template( "index.html",
                            running_checked = running_checked,
                            run_on_startup = run_on_startup,
                            total   =round(total    / 1024**3, 2),
                            used    =round(used     / 1024**3, 2),
                            reserved=round(reserved / 1024**3, 2),
                            free    =round(free     / 1024**3   ),
                            usedPerc    =round(usedPerc,    2),
                            freePerc    =round(freePerc,    2),
                            reservedPerc=round(reservedPerc,2),
                            available=available
                          )


@app.route('/runOnStartup', methods=['POST'])
def runOnStartUp():
    file_folder = __file__.split("/")
    file_folder.pop()
    file_folder = os.sep.join(file_folder)

    bat_file = os.path.join(file_folder, "MemoryManagment.bat")
    if not os.path.exists(bat_file):
        cmd = os.path.join(file_folder, "venv", "Scripts", "pythonw.exe")
        background_file = os.path.join(file_folder, "background.py")
        f = open(bat_file, "w+")
        f.write(cmd + " " + background_file)
        f.close()

    if not os.path.exists(os.path.join(os.getenv('ProgramData'),"Microsoft\\Windows\\Start Menu\\Programs\\StartUp","MemoryManagment.bat")):
        dst = os.path.join(os.getenv('ProgramData'), "Microsoft\\Windows\\Start Menu\\Programs\\StartUp", "MemoryManagment.bat")
        copyfile("MemoryManagment.bat", dst)
    return ""

@app.route('/dontRunOnStartup', methods=['POST'])
def dontRunOnStartUp():
    dst = os.path.join(os.getenv('ProgramData'), "Microsoft\\Windows\\Start Menu\\Programs\\StartUp", "MemoryManagment.bat")
    os.remove(dst)
    return ""

@app.route('/runNow', methods=['POST'])
def runNow():
    file_folder = __file__.split("/")
    file_folder.pop()
    file_folder = os.sep.join(file_folder)
    cmd = os.path.join(file_folder, "venv", "Scripts", "pythonw.exe")
    background_file = os.path.join(file_folder, "background.py")
    os.system(cmd+" "+background_file)
    return ""

@app.route('/dontRunNow', methods=['POST'])
def dontRunNow():
    f = open("data/pid_background.dat")
    pid = f.read()
    f.close()

    os.system( "Taskkill /PID "+pid+" /F" )
    return ""




@app.route('/refresh', methods=['POST'])
def refresh():
    return ""


def background():
    file_folder = __file__.split("/")
    file_folder.pop()
    file_folder = os.sep.join(file_folder)
    cmd = os.path.join(file_folder, "venv", "Scripts", "pythonw.exe")
    background_file = os.path.join(file_folder, "background.py")
    os.system(cmd + " " + background_file + " false")


amountToReserve = 1
@app.route('/reserveFreeSpace', methods=['POST'])
def reserveFreeSpace():
    if not isRunning():
        thread = threading.Thread(target=background, name="Background")
        thread.start()
    f = open("data/keepFree.dat","w+")
    f.write(request.form['amountToReserve'])
    f.close()

    return render_template("reserveFreeSpace.html")




if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run()