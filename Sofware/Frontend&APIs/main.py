from flask import Flask , render_template , session
from flask import request , redirect
import pandas as pd

app = Flask(__name__)
app.secret_key = '1234'

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


@app.route("/profile")
def profile():
    if "username" in session:
        return render_template("profile.html")
    else:
        return redirect("/login")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")