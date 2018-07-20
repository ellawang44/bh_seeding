import os

def xcmd(cmd):
    print(cmd)
    status = os.system(cmd)

'''
xcmd("python main.py --darkmatter 10.853871964321762 --data 'bh' --stats --bin 75")
xcmd("python main.py --darkmatter 10.154901959985743 --data 'bh' --stats --bin 75")
'''
xcmd("python main.py --blackhole 5.154901959985743 --data 'dm' --stats --bin 75")
'''
xcmd("python main.py --darkmatter 10.154901959985743 --data 'z' --bin 75")
xcmd("python main.py --blackhole 5.154901959985743 --data 'z' --bin 75")
xcmd("python main.py --darkmatter 10.154901959985743 --xaxis 'z' --yaxis 'gas' --stats --bin 35")
xcmd("python main.py --darkmatter 10.154901959985743 --xaxis 'z' --yaxis 'bh' --stats --bin 35")
xcmd("python main.py --blackhole 5.154901959985743 --xaxis 'z' --yaxis 'dm' --stats --bin 35")
xcmd("python main.py --darkmatter 10.154901959985743 --data 'bh' --s5")
xcmd("python main.py --blackhole 5.154901959985743 --data 'dm' --s5")
xcmd("python main.py --darkmatter 10.154901959985743 --data 'bh' --stats --bin 75 --file '_M200__test25240'")
'''
xcmd("python main.py --blackhole 5.154901959985743 --data 'dm' --stats --bin 75 --file '_M200__test25240'")
'''
xcmd("python main.py --blackhole 5.154901959985743 --data 'acc' --stats --bin 75 --file '_M200_FOFseeding25240'")
xcmd("python main.py --darkmatter 10.154901959985743 --data 'acc' --stats --bin 75 --file '_M200_FOFseeding25240'")
'''
#xcmd("cd ../report")
#xcmd("./fix_bounding_box *.eps")
