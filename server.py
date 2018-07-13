
from flask import Flask, render_template, request, session, flash, redirect
from twilio.twiml.voice_response import VoiceResponse, Dial, Say
from twilio.rest import Client
import os
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Phonecalls


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
#app.secret_key = 

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

#call = client.calls('CA97b05c1368e2713740830c63441f075d')


####################### LOG IN / REGISTER ###################################

@app.route("/")
def index():
    """shows the homepage, user must sign in or register"""

    return render_template("homepage.html")


@app.route("/", methods=["POST"])
def login():
    """Validate user log in and redirect to their profile pg."""

    email = request.form.get("email")
    pw = request.form.get("pw")

    user_info = User.query.filter_by(email=email).all()
    print(user_info)
    print(user_info[0])
    
    if user_info[0].password == pw:
        session['email'] = email
        return redirect('/profile/{}'.format(user_info[0].user_id))
    else:
        flash("Incorrect password")
        return redirect('/homepage')

    return render_template("profile.html")


@app.route("/profile/<user_id>")
def profile_view(user_id):
    """displays user call log/user details."""
    
    uview = db.session.query(User).get(user_id)
    user_email = uview.email
    user_phone = uview.phone_num
    user_duration_lst = uview.call_duration
    user_calltime_lst = uview.call_datetime
    user_recording_lst = uview.recording_url
    user_sidnum_lst = uview.call_sid

    return render_template("profile.html", user_email=user_email, user_phone=user_phone, 
                                           user_duration_lst=user_duration_lst, 
                                           user_calltime_lst=user_calltime_lst, 
                                           user_recording_lst=user_recording_lst,
                                           user_sidnum_lst=user_sidnum_lst,
                                           user_id=user_id)


@app.route("/register", methods=["POST"])
def registration():
    # """Add new user to database"""

    # #code to confirm user isn't an existing user(if phone_num in db ALERT)
    # #send a verification code to num to confirm registration
    # new_user = User(email=emailsignup, phone_num=telenum, password=nupw)
    # db.session.add(new_user)
    # db.session.commit()


    # return render_template("profile.html")
    pass


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


