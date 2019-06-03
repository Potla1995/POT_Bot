import maps
import random
def initialmapfile():
    maps.decryptFromDB('maps_db.l.html','maps.temp.l.db')
    maps.decryptFromDB('maps_db.u.html','maps.temp.u.db')
    maps.readIntoList('maps.temp.l.db','maps.l.db')
    maps.readIntoList('maps.temp.u.db','maps.u.db')


def recommendloved(msg):
    try:
        SR = [float(x) for x in msg.split()]
    except ValueError:
        return 'Unsupported format: please give a lower and upper star rating. Example: !!r 4.5 5.2'
    if len(SR)!= 2:
        return 'Unsupported format: please give a lower and upper star rating. Example: !!r 4.5 5.2'
    elif SR[0] > SR[1]:
        temp = SR[0]
        SR[0] = SR[1]
        SR[1] = temp

    LovedMapsList = maps.readFromTXT('maps.l.db')
    TruncatedLovedList = [x.__str__() for x in LovedMapsList if (float(x.SR)<=SR[1] and float(x.SR)>=SR[0])]
    return random.choice(TruncatedLovedList) + "\n (%d choices)" % len(TruncatedLovedList)


def recommendunranked(msg):
    try:
        SR = [float(x) for x in msg.split()]
    except ValueError:
        return 'Unsupported format: please give a lower and upper star rating. Example: !!r 4.5 5.2'
    if len(SR)!= 2:
        return 'Unsupported format: please give a lower and upper star rating. Example: !!r 4.5 5.2'
    elif SR[0] > SR[1]:
        temp = SR[0]
        SR[0] = SR[1]
        SR[1] = temp

    UnrankedMapsList = maps.readFromTXT('maps.u.db')
    TruncatedUnrankedList = [x.__str__() for x in UnrankedMapsList if (float(x.SR)<=SR[1] and float(x.SR)>=SR[0])]
    return random.choice(TruncatedUnrankedList) + "\n (%d choices)" % len(TruncatedUnrankedList)


