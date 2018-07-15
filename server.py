
from flask import Flask, render_template, request, session, flash, redirect, g, url_for
from twilio.twiml.voice_response import VoiceResponse, Dial, Say
from twilio.rest import Client
import os
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Phonecalls


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.secret_key = os.urandom(24)

connect_to_db(app)
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


####################### LOG IN / REGISTER ###################################

@app.route("/", methods=["GET", "POST"])
def index():
    """shows the homepage, user must sign in(validation) or register"""
    if request.method == "POST":
        print(request.form)
        username = request.form.get('username')
        password = request.form.get('pw')
        user_cred = User.query.filter_by(username=username).first()

        if user_cred is None:
            flash("Username not found! Try again or Register below.")
            print("No user on file")
            return render_template("homepage.html")
        else:
            if user_cred.password == password:
                session['username'] = username
                return render_template('profile.html')
            else:
                flash("Incorrect password, try again")
                return render_template("homepage.html")
    
    return render_template("homepage.html")

@app.route('/profile')
def logged_in():
    if g.user:
        return render_template('/profile')

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


@app.route("/profile", methods=["POST"])
def profile_view():
    """displays user call log/user details."""
    print(request.form)

    # uview = db.session.query(User).get(user_id)
    # user_email = uview.email
    # username = uview.username
    # user_phone = uview.phone_num
    # user_duration_lst = uview.call_duration
    # user_calltime_lst = uview.call_datetime
    # user_recording_lst = uview.recording_url
    # user_sidnum_lst = uview.call_sid

    # return render_template("profile.html", user_email=user_email, username=username,
    #                                        user_phone=user_phone, 
    #                                        user_duration_lst=user_duration_lst, 
    #                                        user_calltime_lst=user_calltime_lst, 
    #                                        user_recording_lst=user_recording_lst,
    #                                        user_sidnum_lst=user_sidnum_lst,
    #                                        user_id=user_id)
    return render_template("profile.html")


@app.route("/register", methods=["GET", "POST"])
def registration():
    """Add new user to database"""
    #print(request.form)
    if request.form.get('pw1') != request.form.get('pw2'):
        flash("Passwords didn't match.")
        return render_template("homepage.html")
    else:
        username = request.form.get('nusername')
        email = request.form.get('email')
        phone_num = request.form.get('telenum')
        password = request.form.get('pw1')

        nope = 

    #if username in db already, enter a different username

    new_user = User(email=email, phone_num=phone_num, password=password, username=username)
    
    print(new_user)
    #db.session.add(new_user)
    #db.session.commit()
    flash("Thanks for registering! Log in to continue")
    return redirect("/")
    


##################### data for database #############################################   
#prototype

@app.route("/call-to-db", methods=['POST'])
def call_to_db():
    """twilio will send info here when call ends."""
    #print(request.get_data())
    #print("And now as json")
    #print(request.get_json(force=True))
    #print(request.form)
    

    #get specific data info from call via request.get_data()
    data = request.form
    call_sid = data["CallSid"]
    timestamp = data["Timestamp"]
    recording = data["RecordingUrl"]+".mp3"
    recording_sid = data["RecordingSid"]
    duration = data["CallDuration"]
    print("##### CALL_SID = {}".format(call_sid))
    print("##### TIMESTAMP = {}".format(timestamp))
    print("##### RECORDING URL = {}".format(recording))
    print("##### RECORDING_SID = {}".format(recording_sid))
    print("##### CALL DURATION = {} seconds".format(duration))
    print("##### CALL TO = {}".format(PHONE_NUMBER))
        
    #fetch a Call resource
    call = client.calls(call_sid).fetch()
    print("fetch of call = {}".format(call))
            
    #DATA TO GO INTO THE DATABASE
    #if session['email'] == email
        #new_call = Phonecalls(call_duration=duration, call_datetime=timestamp, call_sid=call_sid)
        #db.session.add(new_call)
        #db.session.commit()
    #first_number --> call.to
    #other_number --> GLOBAL VARIABLE
    #user_id --> just put 0 for now
    #recording_url --> call.recordings[0].url or something like that
    #bang, send this data into the db. done
    return "ok"
        
    
def get_duration(call_sid):
    pass


def get_start_time(call_sid):
    pass


def get_recording_id(call_sid):
    pass


def get_recording_mp3_url(recording_id):
    pass


 #############################################################################


@app.route("/call")
def make_call():

    return render_template('homepage_logged.html')


@app.route("/answer3", methods=['GET', 'POST'])
def threewaycall():
    """make a three-way call."""
    
    print(request.get_data())
    response = VoiceResponse()
    response.say("Thank you for calling! Please hold while we connect you", 
            voice='alice')
    response.dial(PHONE_NUMBER)
    
    return str(response)


@app.route("/call", methods=["POST"])
def calling():
    """makes a phone call with two numbers user inputs."""

    # in order for second num to be used in "/answer3" function
    global PHONE_NUMBER
    
    phonenum = request.form.get("phonenum")
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

    return render_template('progresscall.html') 


####################### CALL RETURNED ######################################    


@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""

    #start TwiML response
    resp = VoiceResponse()
    #read a message aloud to the caller
    resp.say("The person you are trying to reach is unavailable, please try them on their personal number. Have a splendid day. Goodbye!", 
            voice='alice')
    #recording caller's phone call
    resp.record()
    #end the call when caller hangsup
    resp.hangup
    
    return str(resp)


###########################################################################


if __name__ == "__main__":
    pass
    #app.run(port=5000, host='0.0.0.0', debug=True)


