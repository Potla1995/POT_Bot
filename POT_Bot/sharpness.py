import math
from statistics import mean
import os

def distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def cosangleovertwo(x1,y1,x2,y2,x3,y3):
    
    AB = distance(x1,y1,x2,y2)
    BC = distance(x2,y2,x3,y3)
    CA = distance(x1,y1,x3,y3)
    cosalpha = AB**2 + BC**2 - CA**2
    try:
        cosalpha /= (2*AB*BC)
    except ZeroDivisionError:
        return 0
    
    return math.sqrt((1+round(cosalpha,5))/2)
    
def sharpness(mapID):
    '''Calculates the sharpness of a map. Provide the .osu file in the link'''
    with open(mapID,'r',encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')
        j = L.index('[HitObjects]')
        L = L[j+1:len(L)-1]

        # calculate the values ab * sin(abc/2) for every a,b,c.
        val = []
        for i in range(len(L)-2):
            Lisplit = L[i].split(',')
            Lipsplit = L[i+1].split(',')
            Lippsplit = L[i+2].split(',')
            xi = Lisplit[0]
            yi = Lisplit[1]
            xip = Lipsplit[0]
            yip = Lipsplit[1]
            xipp = Lippsplit[0]
            yipp = Lippsplit[1]

            # if first object is a slider, pick its end.
            if len(Lisplit)>7:
                c = Lisplit[5].split('|')[-1]
                xi = c.split(':')[0]
                yi = c.split(':')[1]

            # if second object is a slider, (xip,yip) = 2nd point, and 3rd point = next slider point.
            if len(Lipsplit)>7:
                #print(i+j+1)
                c = Lipsplit[5].split('|')[1]
                xipp = c.split(':')[0]
                yipp = c.split(':')[1]

            # typecast string -> float
            xi = float(xi)
            yi = float(yi)
            xip = float(xip)
            yip = float(yip)
            xipp = float(xipp)
            yipp = float(yipp)

            # now calculate distance snap of AB:
            ti = float(Lisplit[2])
            tip = float(Lipsplit[2])
            ds = distance(xi,yi,xip,yip)/(tip-ti)

            # now calculate sine of angle (ABC)/2:
            a = cosangleovertwo(xi,yi,xip,yip,xipp,yipp)

            # if objects are not stacked, add ds * a into the array.
            if ds != 0:
                val.append(ds * a)

        print(mapID + ': ' + str(mean(val)) + ' inverse: ' + str((mean(val)**-1)))
        
        '''
        with open(mapID+'.hist.txt', 'w') as g:
            i = 0
            for x in val:
                g.write(str(i)+' '+str(x)+'\n')
                i += 1
        '''

for file in os.listdir('test'):
    if file.endswith(".osu"):
        sharpness('test/'+file)

