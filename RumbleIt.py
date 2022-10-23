import os
import sys
import ac
import acsys
import sim_info
import math
import socket


l_slip = 0
l_susp = 0
limit = 0.9

# SERVER - CLIENT
host = socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number

client_socket = socket.socket()  # instantiate
try:
    client_socket.connect((host, port))  # connect to the server
except Exception as e:
    print()
    print("ERROR on connecting: ")
    print(str(e))
    ac.log()
    ac.log("ERROR on connecting: ")
    ac.log(str(e))


def sendit(stringer):
    try:
        pass
        client_socket.send(stringer.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
    except Exception as e:
        pass


def acMain(ac_version):
    global l_susp, l_slip, limit, limitSpinner

    appWindow = ac.newApp("RumbleIt")
    ac.setSize(appWindow, 250, 500)
    ac.setBackgroundOpacity(appWindow, 0)
    ac.drawBorder(appWindow, 0)

    l_slip = ac.addLabel(appWindow, "Slip:")
    ac.setPosition(l_slip, 5, 100 + 45)
    ac.setCustomFont(l_slip, "Formula", 0, 0)
    ac.setFontSize(l_slip, 22)
    ac.setFontColor(l_slip, 1, 0, 0, 1)

    l_susp = ac.addLabel(appWindow, "Susp:")
    ac.setPosition(l_susp, 5, 150 + 45)
    ac.setCustomFont(l_susp, "Formula", 0, 0)
    ac.setFontSize(l_susp, 22)
    ac.setFontColor(l_susp, 1, 0, 0, 1)

    limitSpinner = ac.addSpinner(appWindow, 'Limit Spinner')
    ac.setPosition(limitSpinner, 25, 260)
    ac.setSize(limitSpinner, 150, 30)
    ac.setRange(limitSpinner, 0.1, 1.0)
    ac.setValue(limitSpinner, 0.9)
    ac.addOnValueChangeListener(limitSpinner, limit)

    return "RumbleIt"


def acUpdate(deltaT):
    global l_susp, l_slip

    sim_info_obj = sim_info.SimInfo()
    slip_fl, slip_fr, slip_rl, slip_rr = ac.getCarState(0, acsys.CS.TyreSlip)
    if slip_fl == 0.0:
        slip_fl, slip_fr, slip_rl, slip_rr = sim_info_obj.physics.wheelSlip
        slip_fl = max(0.001, slip_fl)
        slip_fr = max(0.001, slip_fr)
        slip_rr = max(0.001, slip_rr)
        slip_rl = max(0.001, slip_rl)
        # multiple all these values by some amount?  1.0 in wheelSlip = ? in TyreSlip?
        mult = 4500.0
        scale = 2.2
        slip_fl = ((math.log(slip_fl) + scale) / scale) * mult
        slip_fr = ((math.log(slip_fr) + scale) / scale) * mult
        slip_rl = ((math.log(slip_rl) + scale) / scale) * mult
        slip_rr = ((math.log(slip_rr) + scale) / scale) * mult

    slip_fl = float(str(slip_fl)[: str(slip_fl).index(".") + 4])
    slip_fr = float(str(slip_fr)[: str(slip_fr).index(".") + 4])
    slip_rl = float(str(slip_rl)[: str(slip_rl).index(".") + 4])
    slip_rr = float(str(slip_rr)[: str(slip_rr).index(".") + 4])

    slip_fl = round(float(slip_fl) / 7500, 2)
    if slip_fl > 1:
        slip_fl = 1
    if slip_fl < 0:
        slip_fl = 0
    slip_fr = round(float(slip_fr) / 7500, 2)
    if slip_fr > 1:
        slip_fr = 1
    if slip_fr < 0:
        slip_fr = 0
    slip_rl = round(float(slip_rl) / 7500, 2)
    if slip_rl > 1:
        slip_rl = 1
    if slip_rl < 0:
        slip_rl = 0
    slip_rr = round(float(slip_rr) / 7500, 2)
    if slip_rr > 1:
        slip_rr = 1
    if slip_rr < 0:
        slip_rr = 0

    slipp = str(slip_fl) + ";" + str(slip_fr) + ";" + str(slip_rl) + ";" + str(slip_rr) + ";"

    suspp = ac.getCarState(0, acsys.CS.SuspensionTravel)

    suspp1 = str(float(str(suspp[0])[:5]) * 10)[:4]
    suspp2 = str(float(str(suspp[1])[:5]) * 10)[:4]
    suspp3 = str(float(str(suspp[2])[:5]) * 10)[:4]
    suspp4 = str(float(str(suspp[3])[:5]) * 10)[:4]

    if float(suspp1) > 1:
        suspp1 = 1
    if float(suspp2) > 1:
        suspp2 = 1
    if float(suspp3) > 1:
        suspp3 = 1
    if float(suspp4) > 1:
        suspp4 = 1

    suspp = str(suspp1) + ";" + str(suspp2) + ";" + str(suspp3) + ";" + str(suspp4)
    ac.setText(l_susp, str(suspp))
    ac.setText(l_slip, str(slipp))

    if float(slip_fl) > limit or float(slip_fr) > limit or float(slip_rl) > limit or float(slip_rr) > limit or float(suspp1) > limit or float(suspp2) > limit or float(suspp3) > limit or float(suspp4) > limit:
        sendit(str(slipp) + str(suspp))
    else:
        sendit("0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0")


def acShutdown():
    ac.log("RumbleIt is closing now...")
    client_socket.close()
    return
