import streamlit as st
import os
import sys
import time
import subprocess


"""
# Welcome to SimpleStepper.

Time to login, sit back, and relax!

"""


# Load saved login information

if os.path.exists("login.txt"):
    with open("login.txt", "r") as f:
        lines = f.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
else:
    username = ""
    password = ""

a = st.sidebar.text('Made by DarkFerret')
Email = st.text_input("Email", value=username)
Password = st.text_input("Password", value=password, type='password')
Time = st.slider("How many hours would you like to run the bot? I recommend sessions no longer than 1-2 hours with a 30 minute break")
Agree = st.checkbox('Understand that ANY cheating tool/bot is risky and that we are NOT responsible for any bans.')
Clear = st.button('Clear login info')



if Email and Password and Agree and Time:
    st.write(':fire:'*5)
    st.write(f'Logging you in as {Email} for {Time} hours')
    st.balloons()


Run = st.button("Run Bot")

def start_subprocess():
    proc = subprocess.Popen(["python", "simple2.py"])
    return proc





if Run:
    st.write('Welcome to SimpleStepper')
    st.success('Successfully started bot!')
    with open("login.txt", "w") as f:
        f.write(f"{Email}\n{Password}\n{Time}")
    proc = start_subprocess()

Stop = st.button('Stop Server')
st.write('Bot will still run if you stop the server, but no data will be shown on the panel. Check console for data.')
if Stop:
    st.stop()

# ItemData = st.button('Check total items found')
# StepData = st.button('Check total steps this session')
def print_text():
    print('C')


# if ItemData:
#   with open("ItemsFound.txt", "r") as f:
#    lines = f.readlines()
#    items = lines[0].strip()
#    st.write(f"{items}")

# if StepData:
#    with open("steps.txt", "r") as f:
#    lines = f.readlines()
#     steps = lines[0].strip()
#     st.write(f"{steps}")



Solve = st.write('When verification is detected, go to the console and type "c"')


if Solve:
    os.system('echo "c" | python')



stepstaken = st.empty()
itemsfound = st.empty()
while True:
    with open("steps.txt", "r") as f:
        steps = f.read()
        stepstaken.text(steps)
        time.sleep(1)
    with open("ItemsFound.txt", "r") as f:
        items = f.read()
        itemsfound.text(items)
        time.sleep(1)
