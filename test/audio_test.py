import subprocess

file="/home/njeffers/heydeer2.wav"

print("Playing audio:",file)

subprocess.run(["aplay","-D","default:CARD=Device",file])

#player= subprocess.Popen(

#)
