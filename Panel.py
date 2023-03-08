import streamlit as st
import os
import sys
import time
import subprocess
import shutil


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

if os.path.exists("webhook.txt"):
    with open("webhook.txt", "r") as f:
        lines = f.readlines()
        webhook = lines[0].strip()
else:
    webhook = ""

a = st.sidebar.text('Made by DarkFerret')
Email = st.text_input("Email", value=username)
Password = st.text_input("Password", value=password, type='password')
Webhook = st.text_input("Webhook URL ****(Recommended)****", value=webhook)
Time = st.slider("How many hours would you like to run the bot? I recommend sessions no longer than 1-2 hours with a 30 minute break")
Agree = st.checkbox('Understand that ANY cheating tool/bot is risky and that we are NOT responsible for any bans.')
Clear = st.button('Clear login info')
Delete = st.button('Delete pages/items folder')


if Delete:
    shutil.rmtree("pages/items")
    st.write("pages/items folder has been deleted.")

if Email and Password and Agree and Time:
    st.write(':fire:'*5)
    st.write(f'Logging you in as {Email} for {Time} hours')
    st.balloons()


Run = st.button("Run Bot")
Pause = st.button("Pause Bot")

def start_subprocess():
    proc = subprocess.Popen(["python", "simple2.py"])
    return proc


if Run:
    st.write('Welcome to SimpleStepper')
    st.success('Successfully started bot!')
    with open("login.txt", "w") as f:
        f.write(f"{Email}\n{Password}\n{Time}")
    with open("webhook.txt", "w") as f:
        f.write(f"{Webhook}")
    proc = start_subprocess()

if Pause:
    st.write('Bot Paused')
    with open("status.txt", "w") as f:
        f.write('pause')

Resume = st.button('Resume Bot')

if Resume:
    st.write('Bot Resumed')
    with open("status.txt", "w") as f:
        f.write('resume')



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
