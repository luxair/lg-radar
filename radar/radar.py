import subprocess
import pyModeS as pms

def process_adsb(msg):
    tc = pms.adsb.typecode(msg)

    if tc in [1,2,3,4]:
        print(msg, pms.adsb.icao(msg), pms.adsb.callsign(msg))

    #if tc in [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]:
    #    print(
    #        msg,
    #        pms.adsb.callsign(msg),
    #        pms.adsb.altitude(msg)
    #    )

with subprocess.Popen(["rtl_adsb"], stdout=subprocess.PIPE) as adsb_flow:
    while True:
        msg = adsb_flow.stdout.readline()

        if len(msg) == 0:
            break

        process_adsb(msg.decode('ascii').strip('*;\r\n'))

