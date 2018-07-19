
from flask import Flask, render_template, request, session, flash, redirect, g, url_for
from twilio.twiml.voice_response import VoiceResponse, Dial, Say
from twilio.rest import Client
import os
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Phonecalls
from authy.api import AuthyApiClient
import datetime



app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.undefined = StrictUndefined
app.secret_key = os.urandom(24)

api = AuthyApiClient(app.config['AUTHY_API_KEY'])

connect_to_db(app)
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)



#Global variable
CALL_SID_TO_USER_ID_MAP = {}
#TODO -- replace with flask.g
#from flask import g
#g.CALL_SID_TO_USER_ID_MAP = {}



################### LOG IN / REGISTER #######################################

@app.route("/")
def index():
    """displays homepage."""
    if 'username' not in session:
        return render_template("homepage.html")

@app.route("/", methods=["POST"])
def login_register():
    """shows the homepage, user must sign in(validation) or register"""
    username = request.form.get('username')
    password = request.form.get('pw')
    user_cred = User.query.filter_by(username=username).first()

    if user_cred is None:
        flash("Username not found! Try again or Register below.")
        return render_template("homepage.html")
        
    if user_cred.password == password:
        session['username'] = username
        if user_cred.phone_num is None:
            flash("Welcome back! Please verify your phone number to complete registration.")
            return render_template("phone_verification.html")
        else:
            return redirect('/profile/{}'.format(session['username']))
    else:
        flash("Incorrect password, try again")
        return render_template("homepage.html")
    
    
@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']


@app.route('/logout')
def logout():
    """removes the user from the session and logs out."""
    session.pop('username', None)
    return redirect('/')


@app.route("/profile/<username>")
def profile_view(username):
    """displays user call log/user details."""
    
    user_detail = User.query.filter_by(username=session['username']).first()
    user_username = user_detail.username
    user_id_num = user_detail.user_id
    user_email = user_detail.email
    user_phone = user_detail.phone_num
    user_calls = user_detail.calls
   
    return render_template("profile.html", user_id=user_id_num, user_email=user_email, 
                                           user_username=user_username, user_phone=user_phone,
                                           user_calls=user_calls)
    
   
@app.route("/register", methods=["GET", "POST"])
def registration():
    """Add new user to database"""
    if request.form.get('pw1') != request.form.get('pw2'):
        flash("Passwords didn't match.")
        return render_template("homepage.html")
    else:
        username = request.form.get('new_username')
        email = request.form.get('email')
        password = request.form.get('pw1')

        if User.query.filter_by(username=username).first() is None:
            new_user = User(email=email, password=password, username=username)
            print(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash("We will now need you to verify your phone number in order to complete registration.")
            return render_template("phone_verification.html")
        else:
            flash("The username '{}' is already taken, please choose another".format(username))
            return redirect("/")
    

@app.route("/phone_verification", methods=["GET", "POST"])
def phone_verification():
    """Verify new user phone."""
    if request.method == "POST":
        country_code = request.form.get("country_code")
        phone_number = request.form.get("phone_number")
        method = request.form.get("method")

        session['country_code'] = country_code
        session['phone_number'] = phone_number

        api.phones.verification_start(phone_number, country_code, via=method)
        return redirect(url_for("verify"))
    else:
        return redirect("/phone_verification")
    
    return render_template("phone_verification.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    """Verify user new phone with code that was sent to the number provided."""
    if request.method == "POST":
        token = request.form.get("token")
        phone_number = session.get("phone_number")
        country_code = session.get("country_code")

        verification = api.phones.verification_check(phone_number, country_code, token)

        
        if verification.ok():
            if 'username' in session:
                username = session['username']
                user = User.query.filter_by(username=username).first()
                user.phone_num = phone_number
                db.session.commit()
                flash("Successful! Thanks for verifying. You added the following mobile " +
                        "number {} to your account.".format(phone_number))
                return redirect('/profile/{}'.format(session['username']))
        else:
            flash("Wrong verification code")
            return redirect(url_for("verify"))        

    return render_template("verify.html")

################## CALL DATA FOR DATABASE ####################################   

@app.route("/call-to-db", methods=['POST'])
def call_to_db():
    """twilio will send info here when call ends."""
    """this route is ONLY called by twilio's api."""
    """sessions no longer exist in this function."""
      
    #get specific data info from call via request.get_data()
    #giving them variable names to store in database
    data = request.form
    call_sid = data["CallSid"]
    timestamp = data["Timestamp"][0:-15]
    recording = data["RecordingUrl"]+".mp3"
    recording_sid = data["RecordingSid"]
    duration1 = int(data["CallDuration"])
    duration = str(datetime.timedelta(seconds=duration1))
    #user_id/username grabbed from global var to add calls according to user in session.
    user_id = CALL_SID_TO_USER_ID_MAP[call_sid]
                   
    #DATA TO GO INTO THE DATABASE
    user = User.query.filter_by(username=user_id).all()
    userid = user[0].user_id
    if userid > 0:
        new_call = Phonecalls(user_id=userid, call_duration=duration, call_datetime=timestamp,
                              call_sid=call_sid, recording_url=recording,
                              recording_sid=recording_sid, number_called=PHONE_NUMBER)
        db.session.add(new_call)
        db.session.commit()
        print(new_call)
      
    return "ok"

#################### MAKE PHONE CALLS #########################################

@app.route("/call")
def make_call():
    """renders page where ONLY signed in users can make a call."""
    if 'username' in session:
        return render_template('make_call.html', user_username=session['username'])
    else:
        return redirect("/")

@app.route("/answer3", methods=['GET', 'POST'])
def threewaycall():
    """make a three-way call."""
    
    print(request.get_data())
    response = VoiceResponse()
    response.say("Please hold while we connect you", voice='alice')
    response.dial(PHONE_NUMBER)
    
    return str(response)


@app.route("/call", methods=["POST"])
def calling():
    """makes a phone call with two numbers user inputs."""
    # in order for second num to be used in "/answer3" function
    global PHONE_NUMBER
    #OPTIONAL: phonenum = request.form.get("phonenum")<-if i want the user to input a dif origin
    #num instead of the one saved inside the db.
    #BELOW: grabs the user's verified num to make the call.
    username = session['username']
    user = User.query.filter_by(username=username).all()
    phonenum = user[0].phone_num
    phonenum2 = request.form.get("phonenum2")
    PHONE_NUMBER = phonenum2

    call = client.calls.create(record=True,
                        method='GET',
                        status_callback='http://juliettedemo.ngrok.io/call-to-db',
                        status_callback_event='completed',
                        status_callback_method='POST',
                        url='http://juliettedemo.ngrok.io/answer3',
                        to=phonenum,
                        from_='+16692717646'
                        )

    #saving user-in-session's info to a global var to use for when twilio sends only call data back. 
    #Twilio won't have client side info. Call data is sent to a function unable to be called by flask
    call_sid = call.sid
    print(session)
    user_name = session["username"]
    CALL_SID_TO_USER_ID_MAP[call_sid] = user_name
    return render_template('progresscall.html', user_username=user_name) 


####################### CALL RETURNED ######################################    

@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""

    #start TwiML response
    resp = VoiceResponse()
    #read a message aloud to the caller if caller calls the twilio num
    resp.say("The person you are trying to reach is unavailable, please try them on " + 
                "their personal number. Goodbye!", voice='alice')
    #recording caller's phone call
    resp.record()
    #end the call when caller hangsup
    resp.hangup()
    
    return str(resp)


###########################################################################


if __name__ == "__main__":
    #pass
    app.run(port=5000, host='0.0.0.0', debug=True)


