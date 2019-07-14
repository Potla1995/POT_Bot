import math
from statistics import mean
import os


def BeatInterval(mapID):  # Identifies the BPM of any given map.
    BPM = 0
    with open(mapID, "r", encoding="utf-8") as f:
        L = f.read().split("\n")
        TimingPointIndex = L.index("[TimingPoints]") + 1
        BPM = float(L[TimingPointIndex].split(",")[1])
    # 60*1000/float(BPM) is the formula for obtaining the true BPM.
    return 60 * 1000 / BPM


#Obtains all the streams of the map
def DectectStream(mapID):
    with open(mapID, "r", encoding="utf-8") as f:
        L = f.read().split("\n")
        ObjectIndex = L.index("[HitObjects]") + 1

        CircleIndex = list(x for x in L[ObjectIndex::] if len(x.split(",")) < 7)

        BPM = BeatInterval(mapID)

        StreamList = []

        i = 0

        while i < len(CircleIndex) - 2:
            Circle = CircleIndex[i].split(",")
            CircleTime = Circle[2]

            Circle2 = CircleIndex[i + 1].split(",")
            CircleTime2 = Circle2[2]

            if float(CircleTime2) - float(CircleTime) <= BPM:
                # That means they are together.
                CurrentStream = []
                CurrentStream.append(CircleIndex[i])
                while float(CircleTime2) - float(CircleTime) < BPM:
                    CurrentStream.append(CircleIndex[i + 1])
                    i = i + 1
                    if i >= len(CircleIndex) - 2:
                        break
                    Circle = CircleIndex[i].split(",")
                    CircleTime = Circle[2]

                    Circle2 = CircleIndex[i + 1].split(",")
                    CircleTime2 = Circle2[2]

                # Steam Obtained, Push to SteamList
                StreamList.append(CurrentStream)
            i = i + 1

        # Return a list if the list is only above three notes.
        TrueStreamList = list(x for x in StreamList if len(x) > 3)

        return TrueStreamList


def EvalBursts(StreamList):
    # Get bursts -- Shorter than 15 notes.
    BurstList = list(x for x in StreamList if len(x) < 15)
    """
    There are Serveral methods of calculating Difficulty for bursts.
    1. Angle of approach.
    2. Spacing Changes.
    3. Spacing.
    4. Curvature
    5. Rythym changes (eg, 1/4th and 1/6th) <- TODO
    6. Spacing between the bursts.
    7. Direction changes.
    8. Cuts <- Dunno how to handle this one.
    """
    return BurstList

def FlowDifficulty(mapID):
    # Get all Bursts and Streams
    # Get difficulty of Bursts only.
    pass


FlowDifficulty("test/boogie.osu")

