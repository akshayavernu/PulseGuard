import time
import requests
from twilio.rest import Client

# -----------------------------
# TWILIO SETTINGS
# -----------------------------
ACCOUNT_SID = "Input_Account_SID"
AUTH_TOKEN = "Input_Auth_Token"

TWILIO_NUMBER = "Input_Twilio_Number"
EMERGENCY_CONTACT = "Input_Emergency_Contact"


# -----------------------------
# AGE GROUP FUNCTION
# -----------------------------
def get_age_group(age):

    if 1 <= age <= 5:
        return "Toddler"

    elif 6 <= age <= 12:
        return "Child"

    elif 13 <= age <= 19:
        return "Teen"

    elif 20 <= age <= 60:
        return "Adult"

    else:
        return "Senior"


# -----------------------------
# HEART RATE LIMITS
# -----------------------------
health_limits = {

    "Toddler": {
        "Resting": {"min": 80, "max": 130},
        "Exercise": {"min": 100, "max": 180}
    },

    "Child": {
        "Resting": {"min": 70, "max": 110},
        "Exercise": {"min": 90, "max": 170}
    },

    "Teen": {
        "Resting": {"min": 50, "max": 100},
        "Exercise": {"min": 100, "max": 170}
    },

    "Adult": {
        "Resting": {"min": 60, "max": 100},
        "Exercise": {"min": 100, "max": 165}
    },

    "Senior": {
        "Resting": {"min": 55, "max": 90},
        "Exercise": {"min": 80, "max": 140}
    }
}


# -----------------------------
# EMERGENCY CALL FUNCTION
# -----------------------------
def emergency_call():

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    call = client.calls.create(

        twiml='''
<Response>
<Say>
Warning. Sustained dangerous heart rate detected.
Emergency assistance may be required.
</Say>
</Response>
''',

        to=EMERGENCY_CONTACT,
        from_=TWILIO_NUMBER
    )

    print("Emergency call initiated.")


# -----------------------------
# LIVE MONITOR STATE
# -----------------------------
high_bpm_start_time = None


# -----------------------------
# HEART RATE CHECKER
# -----------------------------
def check_heart_rate(group, current_bpm, is_exercising):

    global high_bpm_start_time

    activity = "Exercise" if is_exercising else "Resting"

    limits = health_limits[group][activity]

    # TOO LOW
    if current_bpm < limits["min"]:

        print(f"LOW ALERT: {current_bpm} BPM")

        high_bpm_start_time = None

        return

    # NORMAL RANGE
    if current_bpm <= limits["max"]:

        print(f"Normal: {current_bpm} BPM")

        high_bpm_start_time = None

        return

    # HIGH BPM
    print(f"WARNING: High BPM detected ({current_bpm})")

    # START TIMER
    if high_bpm_start_time is None:

        high_bpm_start_time = time.time()

        elapsed = 0

    else:

        elapsed = time.time() - high_bpm_start_time

    print(f"High BPM duration: {int(elapsed)} seconds")

    # EMERGENCY TRIGGER
    if elapsed >= 5:

        print("5 seconds sustained high BPM!")

        emergency_call()

        high_bpm_start_time = None

    # ABOVE SAFE RANGE
    elif current_bpm > limits["max"]:

        print(f"Above safe range for {group}: {current_bpm}")


# -----------------------------
# TESTING SECTION
# -----------------------------

age = int(input("Enter age: "))

group = get_age_group(age)
current_bpm = int(input("Enter BPM:"))
is_exercising = (input("Are you exercising True/False"))

while True:
    check_heart_rate(group, current_bpm, is_exercising)
