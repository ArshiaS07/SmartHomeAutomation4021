from flask import Flask , render_template , session , flash
from flask import request , redirect , url_for , jsonify
from flask_mail import Mail , Message
import pandas as pd
import os
from connect import *
import voice_assistant
from playsound import playsound
from IPs import *
import multiprocessing
import time

app = Flask(__name__)
app.secret_key = '1234'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yaghuduk@gmail.com'
app.config['MAIL_PASSWORD'] = 'gnst suft ajuf ital'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def home():
    return redirect("/login")

@app.route("/sign-up" , methods = ["POST" , "GET"])
def register():
    if "username" not in session:
        message = ""
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            t = 0
            file = open("users.txt" , "r+")
            for line in file:
                if username == line.strip().split(" ")[0]:
                    t += 1

            if t == 0:
                file.write(f"{username} {password}" + "\n")
                file.close()

                userInfo = {"username" : [username] ,
                            "password" : [password] ,
                            "profile photo" : ["profile.png"] ,
                            "email" : ["empty"]}
                newUser = open(f"{username}.csv" , "a")
                pd.DataFrame(userInfo).to_csv(newUser)
                newUser.close()

                return "<script>alert('Done! You can login now.');window.location.href = '/login';</script>"
            else:
                #return "<script>alert('Username already taken. Try another.');window.location.href = '/sign-up';</script>"
                message = "Username already taken. Try another."

        return render_template("sign-up.html" , message = message)
    else:
        return redirect("/profile")


@app.route("/login" , methods = ["POST" , "GET"])
def login():
    if "username" in session:
        return redirect("/profile")
    else:
        message = ""
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            file = open("users.txt")
            t = 0
            for line in file:
                if username == line.strip().split(" ")[0]:
                    t += 1
                    if password == line.strip().split(" ")[1]:
                        session["username"] = username
                        return redirect("/profile")
                    else:
                        message = "Invalid password."


            if t == 0:
                message = "You don't have an account. Try to sign up first."
            file.close()

        return render_template("login.html" , message = message)


@app.route("/panel" , methods = ["POST" , "GET"])
def panel():
    if "username" in session:
        result = ""
        lightStatus = 0
        waterStatus = 0
        gasStatus = 0
        if request.method == "GET":
            lightValue = request.args.get("light")
            waterValue = request.args.get("water")
            gasValue = request.args.get("water")
            if lightValue == "on":
                lightStatus = 1
                thread = threading.Thread(target=send_data , args = (lightStatus , IP["light"]))
                thread.start()
                #print(lightStatus , lightValue)
            if lightValue == None:
                lightStatus = 0
                thread = threading.Thread(target=send_data , args = (lightStatus , IP["light"]))
                thread.start()
                #print(lightStatus , lightValue)

            if waterValue == "on":
                waterStatus = 1
                thread = threading.Thread(target=send_data , args = (waterStatus , IP["water"]))
                thread.start()
                #print(waterStatus , request.args.get("water"))
            if waterValue == None:
                waterStatus = 0
                thread = threading.Thread(target=send_data , args = (waterStatus , IP["water"]))
                thread.start()
                #print(waterStatus , request.args.get("water"))

            if gasValue == "on":
                gasStatus = 1
                thread = threading.Thread(target=send_data , args = (gasStatus , IP["water"]))
                thread.start()
                print(gasStatus , request.args.get("gas"))

            if gasValue == None:
                gasStatus = 0
                thread = threading.Thread(target=send_data , args = (gasStatus , IP["water"]))
                thread.start()
                print(gasStatus , request.args.get("gas"))


            if request.args.get("partyDigital") == "on":
                thread = threading.Thread(target=send_data , args = (request.args.get("partyAnolog") , IP["light"]))
                thread.start()
                print(type(request.args.get("partyAnolog")))

            if request.args.get("waterDigital") == "on":
                thread = threading.Thread(target=send_data , args = (request.args.get("waterAnolog") , IP["water"]))
                thread.start()
                print(request.args.get("waterAnolog"))

            if gasValue == "on":
                thread = threading.Thread(target=send_data , args = (request.args.get("gasAnolog") , IP["water"]))
                thread.start()
                print(request.args.get("gasAnolog"))

        return render_template("panel.html" , lightStatus = lightStatus , waterStatus = waterStatus , gasStatus = gasStatus)
    else:
        return redirect("/login")


@app.route("/doorOpen")
def doorOpen():
    if "username" in session:
        thread = threading.Thread(target=send_data , args = (1 , IP["door"]))
        thread.start()
        print("Door is open")
        return redirect("/panel")
    else:
        return redirect("/login")

@app.route("/doorClose")
def doorclose():
    if "username" in session:
        thread = threading.Thread(target=send_data , args = (0 , IP["door"]))
        thread.start()
        print("Door is closed")
        return redirect("/panel")
    else:
        return redirect("/login")


@app.route("/assistant")
def assistant():
    if "username" in session:
        return render_template("assistant.html")
    else:
        return redirect("/login")

@app.route("/assistant_process")
def assistant_process():
    if "username" in session:
        #voice_assistant.main()
        #music_dir = r"music"
        songs = os.listdir("/")
        while True:
            audio = voice_assistant.capture_voice_input()
            text = voice_assistant.convert_voice_to_text(audio)
            end_program = voice_assistant.process_voice_command(text)
            if end_program is not None:
                break
        if end_program == "l1":
            thread = threading.Thread(target=send_data , args = (1 , IP["light"]))
            thread.start()
        if end_program == "l0":
            thread = threading.Thread(target=send_data , args = (0 , IP["light"]))
            thread.start()

        if end_program == "w1":
            thread = threading.Thread(target=send_data , args = (1 , IP["water"]))
            thread.start()
        if end_program == "w0":
            thread = threading.Thread(target=send_data , args = (0 , IP["water"]))
            thread.start()

        if end_program == "g1":
            thread = threading.Thread(target=send_data , args = (1 , IP["water"]))
            thread.start()
        if end_program == "g0":
            thread = threading.Thread(target=send_data , args = (0 , IP["water"]))
            thread.start()
        if end_program == "d1":
            thread = threading.Thread(target=send_data , args = (1 , IP["door"]))
            thread.start()
        if end_program == "d0":
            thread = threading.Thread(target=send_data , args = (0 , IP["door"]))
            thread.start()
        if end_program == "music":
            playsound("2.mp3")
            time.sleep(1000)
        print(end_program)
        return redirect("/assistant")
    else:
        return redirect("/login")

@app.route("/profile" , methods = ["POST" , "GET"])
def profile():
    if "username" in session:
        df = pd.read_csv(f"{session['username']}.csv")
        profilePhoto = f"static/{df['profile photo'][0]}"
        email = df["email"][0]
        if request.method == "POST":
            if request.files["file"].filename != "":
                f = request.files["file"]
                f.save(f"static/{session['username']}.png")
                df["profile photo"][0] = f"{session['username']}.png"
                df.to_csv(f"{session['username']}.csv")
            if request.form["newpass"] != "" and request.form["newpass"] == request.form["secondnewpass"]:
                df["password"][0] = request.form["newpass"]
                df.to_csv(f"{session['username']}.csv")
                with open("users.txt" , "r") as file:
                    inputFilelines = file.readlines()
                    with open("users.txt" , "w") as file:
                        for line in inputFilelines:
                            if line.strip().split(" ")[0] != session["username"]:
                                file.write(line)
                file.close()
                file = open("users.txt" , "a+")
                file.write(f"{df['username'][0]} {request.form['newpass']}" + "\n")
                file.close()

            if request.form["email"] != "":
                df["email"][0] = request.form["email"]
                df.to_csv(f"{session['username']}.csv")

            if request.form["newpass"] != "" and request.form["newpass"] != request.form["secondnewpass"]:
                return "<script>alert('Your passwords are not the same');window.location.href = '/profile';</script>"

            return redirect("/profile")
        return render_template("profile.html" , profilePhoto = profilePhoto , email = email)
    else:
        return redirect("/logout")

@app.route("/remove-photo")
def removePhoto():
    if "username" in session:
        df = pd.read_csv(f"{session['username']}.csv")
        if df["profile photo"][0] != "profile.png":
            os.remove(f"static/{df['profile photo'][0]}")
            df["profile photo"][0] = "profile.png"
            df.to_csv(f"{session['username']}.csv")
        return redirect("/profile")

    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/delete-account")
def delete():
    if "username" in session:
        df = pd.read_csv(f"{session['username']}.csv")
        if df["profile photo"][0] != "profile.png":
            os.remove(f"static/{session['username']}.png")
        os.remove(f"{session['username']}.csv")
        with open("users.txt" , "r") as file:
            inputFilelines = file.readlines()
            with open("users.txt" , "w") as file:
                for line in inputFilelines:
                    if line.strip().split(" ")[0] != session["username"]:
                        file.write(line)

        session.clear()
        file.close()
        return "<script>alert('Your account has been deleted successfully');window.location.href = '/login';</script>"
    else:
        return redirect(url_for("login"))


@app.route("/recovery" , methods = ["GET" , "POST"])
def recovery():
    if "username" not in session:
        message = ""
        if request.method == "POST":
            email = request.form["email"]
            file = open("users.txt")
            t = 0
            users = []
            for line in file:
                users.append(f"{line.strip().split(' ')[0]}.csv")
                if line.strip().split(" ")[0] == email:
                        t = 1
                        msg = Message('Restore your account', sender = 'yaghuduk@gmail.com', recipients = [email])
                        msg.body = f"Your username is {line.strip().split(' ')[0]} and your password is {line.strip().split(' ')[1]}. Keep them safe."
                        mail.send(msg)
                        return "<script>alert('We sent you an email. Check it and login to your account');window.location.href = '/login';</script>"

                if t == 0:
                    count = 0
                    for user in users:
                        df = pd.read_csv(user)
                        if df["email"][0] == email:
                            count = 1
                            msg = Message('Restore your account', sender = 'yaghuduk@gmail.com', recipients = [email])
                            msg.body = f"Your username is {df['username'][0]} and your password is {df['password'][0]}. Keep them safe."
                            mail.send(msg)
                            break

                    if count == 0:
                        message = "There are no accounts created with this email."

                    else:
                        return "<script>alert('We sent you an email. Check it and login to your account');window.location.href = '/login';</script>"

        return render_template("recovery.html" , message = message)

    else:
        return redirect(url_for("panel"))
