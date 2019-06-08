import math
from statistics import mean
import os

def distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def angle(x1,y1,x2,y2,x3,y3):
    
    AB = distance(x1,y1,x2,y2)
    BC = distance(x2,y2,x3,y3)
    CA = distance(x1,y1,x3,y3)
    cosalpha = AB**2 + BC**2 - CA**2
    try:
        cosalpha /= (2*AB*BC)
    except ZeroDivisionError:
        return 0
    
    return math.acos(round(cosalpha,5))

def TimingPoints(mapID):
    TimingPointList = [];
    with open(mapID,'r',encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')
        
        #Get all the timing events;
        TimingPointsStartIndex = L.index('[TimingPoints]');
        TimingPointsEndIndex = L.index('[Colours]');
        
        #Strip timingpoints of empty strings and obtain all timing points.
        TimingPointList = list(x for x in L[TimingPointsStartIndex + 1: TimingPointsEndIndex] if x.strip());

    return TimingPointList;

    
def SliderMultiplier(mapID):
    SliderDifficulty = 1.4
    
    with open(mapID,'r',encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')
        
        
        DifficultyStartIndex = L.index('[Difficulty]')
        DifficultyEndIndex = L.index('[Events]')
        
        Difficulty = list(x for x in L[DifficultyStartIndex+1: DifficultyEndIndex] if x.strip());
        
        SliderDiffIndex = list(i for i, word in enumerate(Difficulty) if word.startswith("SliderMultiplier"))
        
        if len(SliderDiffIndex) > 0:
            SliderDifficulty = float(Difficulty[SliderDiffIndex[0]].split(':')[1]);
        
    return SliderDifficulty

    
def FindTimingpoint(Time, TimingList):
    #To find the timing in the timingList that is the lowest
    PrevTimingPoint = ''
    PrevInheritedTimingPoint = ''
    for timingPoint in TimingList:
        L = timingPoint.split(',')
        LTime = float(L[0])
        Inherited = int(L[6]);
        if LTime < Time:
            if Inherited:
                PrevInheritedTimingPoint = timingpoint
            else: 
                PrevTimingPoint = timingPoint
                break
                
    #Use PrevTimingPoint split to find out Duration of beat.
    print(PrevInheritedTimingPoint)
    print(PrevTimingPoint)
    BeatDuration = float(PrevTimingPoint.split(',')[1])
    
    return BeatDuration;

def SliderDuration(mapID):
    TimingList = TimingPoints(mapID);
    SM = SliderMultiplier(mapID);
    
    with open(mapID,'r',encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')
        j = L.index('[HitObjects]')
        L = L[j+1:len(L)-1]
        
        
        #slider duration = pixelLength / (100.0 * SliderMultiplier) * BeatDuration
        
        
        SliderDurationList = []
        for i in range(len(L)):
            if(len(L[i].split(',')) > 7): #Check for slider 
                slider = L[i].split(',');
                PixelLength = float(slider[7]);
                Time = float(slider[2]);
                BeatDuration = FindTimingpoint(Time, TimingList);
                SliderDurationList.append(PixelLength /(100 * SM) * BeatDuration);

        return SliderDurationList

def sharpness(mapID):
    '''Calculates the sharpness of a map. Provide the .osu file in the link'''
    with open(mapID,'r',encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')
        j = L.index('[HitObjects]')
        L = L[j+1:len(L)-1]

        # calculate the values ab * cos(abc/2) for every a,b,c.
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

            # if second object is a slider, (xip,yip) = 2nd point, and 3rd point = next slider anchor.
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
            ds1 = distance(xi,yi,xip,yip)/(tip-ti)

            # calculate also distance snap of BC:
            tipp = float(Lippsplit[2])
            ds2 = distance(xip,yip,xipp,yipp)/(tipp-tip)

            # now calculate cosine of angle (ABC)/2:
            #a = cosangleovertwo(xi,yi,xip,yip,xipp,yipp)
            a = angle(xi,yi,xip,yip,xipp,yipp)
            a = math.sinh(a)
            #a = math.tan(a/4)


            # if objects are not stacked, append ds * a to the list.
            if ds1 >= 0.5 and ds2 >= 0.5:
                val.append(ds1*ds2*a)
            # if the first object is a double and the second is further away, multiply by 1.5
            elif ds1 <= 0.5 and ds2 >= 0.5:
                val.append((ds1+0.1)*ds2*a*1.5)
            
        print(mapID + ': ' + str(mean(val))) #+ ' inverse: ' + str((mean(val)**-1)))
        return mean(val)

def techiness(mapID):
    s = sharpness(mapID)   
    # Incorporate sliderspeeds into the formula:
    base_sv = SliderMultiplier(mapID)
    SliderDurationList = SliderDuration(mapID)
    slidervar =  []
    j = 0
    with open(mapID,'r',encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')
        j = L.index('[HitObjects]')
        L = L[j+1:len(L)-1]
        for i in range(len(L)):
            Lisplit = L[i].split(',')
            if len(Lisplit) > 7:
                pixelLength = float(Lisplit[-1])
                sliderspeed = pixelLength / SliderDuration[j]
                slidervar.append(sliderspeed)
    print(mapID + ': ' + str(mean(slidervar)) + ', variance: ' + str(var(slidervar)))
techiness('test/technical master.osu')

#print(TimingPoints('test/technical master.osu'))
#print(SliderMultiplier('test/technical master.osu'))
#for file in os.listdir('test'):
#    if file.endswith(".osu"):
#        sharpness('test/'+file)

