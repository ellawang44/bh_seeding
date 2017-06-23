import read
from init import M_bh

#some allowed range around the given mass:
r = 100

if M_bh == None:
    data = None
else:
    bhs = []
    for key, value in read.halo_data.items():
        current_redshift = key[0]
        counts = 0
        for i in value:
            if M_bh - r < i[5] < M_bh + r:
                counts += 1
            else:
                pass
        if counts != 0:
            bhs.append((current_redshift, counts))
        else:
            pass
    if bhs != []:
        redshift = []
        num = []
        for i in sorted(bhs):
            redshift.append(i[0])
            num.append(i[1])
        data = (redshift, num)
    else:
        print("error: no black holes found within mass range " + str(M_bh - r) + " to " + str(M_bh + r))
        quit()
