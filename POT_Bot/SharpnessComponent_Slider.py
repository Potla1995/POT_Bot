import math
from statistics import mean
import os


def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)


def angle(x1, y1, x2, y2, x3, y3):

    AB = distance(x1, y1, x2, y2)
    BC = distance(x2, y2, x3, y3)
    CA = distance(x1, y1, x3, y3)
    cosalpha = AB**2 + BC**2 - CA**2
    try:
        cosalpha /= (2*AB*BC)
    except ZeroDivisionError:
        return 0

    return math.acos(round(cosalpha, 5))


def TimingPoints(mapID):
    TimingPointList = []
    with open(mapID, 'r', encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')

        # Get all the timing events;
        TimingPointsStartIndex = L.index('[TimingPoints]')
        TimingPointsEndIndex = L.index('[Colours]')

        # Strip timingpoints of empty strings and obtain all timing points.
        TimingPointList = list(
            x for x in L[TimingPointsStartIndex + 1: TimingPointsEndIndex] if x.strip())

    return TimingPointList


def SliderMultiplier(mapID):
    SliderDifficulty = 1.4

    with open(mapID, 'r', encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')

        DifficultyStartIndex = L.index('[Difficulty]')
        DifficultyEndIndex = L.index('[Events]')

        Difficulty = list(
            x for x in L[DifficultyStartIndex+1: DifficultyEndIndex] if x.strip())

        SliderDiffIndex = list(i for i, word in enumerate(
            Difficulty) if word.startswith("SliderMultiplier"))

        if len(SliderDiffIndex) > 0:
            SliderDifficulty = float(
                Difficulty[SliderDiffIndex[0]].split(':')[1])

    return SliderDifficulty


def CircleSize(mapID):
    CircleSizeNum = 4

    with open(mapID, 'r', encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')

        DifficultyStartIndex = L.index('[Difficulty]')
        DifficultyEndIndex = L.index('[Events]')

        Difficulty = list(
            x for x in L[DifficultyStartIndex+1: DifficultyEndIndex] if x.strip())

        Index = list(i for i, word in enumerate(Difficulty)
                     if word.startswith("CircleSize"))

        CircleSizeNum = float(Difficulty[Index[0]].split(':')[1])

    return CircleSizeNum


def FindTimingpoint(Time, TimingList):
    # To find the timing in the timingList that is the lowest
    NonInheritedTimingPoint = TimingList[0]
    InheritedTimingPoint = TimingList[0]
    for i in range(len(TimingList)):
        L = TimingList[i].split(',')
        LTime = float(L[0])
        Inherited = int(L[6])
        # Time needs to be lower than the slider time point and must not be inherited.
        if(Inherited == 1):
            NonInheritedTimingPoint = TimingList[i]

        if(LTime < Time):
            InheritedTimingPoint = TimingList[i]
        else:
            break
    # Use PrevTimingPoint split to find out Duration of beat.

    NonInheritedBeatDuration = float(NonInheritedTimingPoint.split(',')[1])
    InheritedBeatDuration = float(InheritedTimingPoint.split(',')[1])

    if(InheritedBeatDuration > 0):
        return NonInheritedBeatDuration

    else:
        return NonInheritedBeatDuration * (-InheritedBeatDuration/100)


def SliderDuration(mapID):
    TimingList = TimingPoints(mapID)
    SM = SliderMultiplier(mapID)

    with open(mapID, 'r', encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')
        j = L.index('[HitObjects]')
        L = L[j+1:len(L)-1]

        # slider duration = pixelLength / (100.0 * SliderMultiplier) * BeatDuration

        SliderDurationList = []
        for i in range(len(L)):
            if(len(L[i].split(',')) > 7):  # Check for slider
                slider = L[i].split(',')
                PixelLength = float(slider[7])
                Time = float(slider[2])
                BeatDuration = FindTimingpoint(Time, TimingList)
                SliderDurationList.append(
                    PixelLength / (100 * SM) * BeatDuration)

        return SliderDurationList


def SliderLengths(mapID):
    with open(mapID, 'r', encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')
        j = L.index('[HitObjects]')
        L = L[j+1:len(L)-1]

        SliderLengthList = []
        for i in range(len(L)):
            if(len(L[i].split(',')) > 7):
                slider = L[i].split(',')
                SliderLengthList.append(int(float(slider[7])))

        return SliderLengthList


def SliderAngleDifficulty(mapID):
    with open(mapID, 'r', encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')
        j = L.index('[HitObjects]')
        L = L[j+1:len(L)-1]
        angleValues = []
        for i in range(len(L)):
            if len(L[i].split(',')) > 7:
                slider = L[i].split(',')
                sliderStartPointX = slider[0]
                sliderStartPointY = slider[1]
                sliderPoints = slider[5].split('|')
                sliderAngles = []
                for i in range(2, len(sliderPoints)-2):
                    if sliderPoints[i] == sliderPoints[i+1]:  # if a red anchor exists,
                        x1 = float(sliderPoints[i-1].split(':')[0])
                        y1 = float(sliderPoints[i-1].split(':')[1])
                        x2 = float(sliderPoints[i].split(':')[0])
                        y2 = float(sliderPoints[i].split(':')[1])
                        x3 = float(sliderPoints[i+2].split(':')[0])
                        y3 = float(sliderPoints[i+2].split(':')[1])
                        sliderAngles.append(angle(x1, y1, x2, y2, x3, y3))
                sumAngleDiff = 1
                for sliderAng in sliderAngles:
                    sumAngleDiff += math.exp(-sliderAng)
                angleValues.append(sumAngleDiff)
        return angleValues


def SliderFollowDifficulty(mapID):
    SM = SliderLengths(mapID)
    DL = SliderDuration(mapID)
    SSM = SliderMultiplier(mapID)
    CS = CircleSize(mapID)
    AV = SliderAngleDifficulty(mapID)
    SFD = []
    for i in range(len(SM)):
        x = (SM[i]*CS*AV[i]/DL[i])
        SFD.append(x)
    print("{}:{}".format(mapID, mean(SFD)))


for file in os.listdir('test'):
    if file.endswith(".osu"):
        SliderFollowDifficulty('test/'+file)
