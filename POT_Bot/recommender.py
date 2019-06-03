import maps
import random
def initialmapfile():
    maps.decryptFromDB('database/maps_db.l.db','database/maps.temp.l.db')
    maps.decryptFromDB('database/maps_db.u.db','database/maps.temp.u.db')
    maps.readIntoList('database/maps.temp.l.db','database/maps.l.db')
    maps.readIntoList('database/maps.temp.u.db','database/maps.u.db')


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

    LovedMapsList = maps.readFromTXT('database/maps.l.db')
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

    UnrankedMapsList = maps.readFromTXT('database/maps.u.db')
    TruncatedUnrankedList = [x.__str__() for x in UnrankedMapsList if (float(x.SR)<=SR[1] and float(x.SR)>=SR[0])]
    return random.choice(TruncatedUnrankedList) + "\n (%d choices)" % len(TruncatedUnrankedList)


