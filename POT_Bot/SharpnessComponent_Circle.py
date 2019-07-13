import math
from statistics import mean
import os

def BeatInterval(mapID): #Identifies the BPM of any given map.
  BPM = 0
  with open(mapID,'r',encoding='utf-8') as f:
    L = f.read().split('\n')
    TimingPointIndex = L.index('[TimingPoints]') + 1
    BPM = float(L[TimingPointIndex].split(',')[1])
  #60*1000/float(BPM) is the formula for obtaining the true BPM. 
  return 60*1000/BPM

def DectectStream(mapID):
  with open(mapID,'r',encoding='utf-8') as f:
    L = f.read().split("\n")
    ObjectIndex = L.index('[HitObjects]') + 1
    
    
    CircleIndex = list(x for x in L[ObjectIndex::] if len(x.split(',')) < 7)
    
    BPM = BeatInterval(mapID)
    
    StreamList = []
    
    i = 0
  
    while i < len(CircleIndex) -2:
      Circle = CircleIndex[i].split(',')
      CircleTime = Circle[2]
      
      Circle2 = CircleIndex[i+1].split(',')
      CircleTime2 = Circle2[2]
      
      if(float(CircleTime2) - float(CircleTime) <= BPM):
        #That means they are together.
        CurrentStream = []
        CurrentStream.append(CircleIndex[i])
        while(float(CircleTime2) - float(CircleTime) < BPM):
          CurrentStream.append(CircleIndex[i+1])
          i = i+1
          if(i >= len(CircleIndex) - 2):
            break
          Circle = CircleIndex[i].split(',')
          CircleTime = Circle[2]

          Circle2 = CircleIndex[i+1].split(',')
          CircleTime2 = Circle2[2]
      
        #Steam Obtained, Push to SteamList
        StreamList.append(CurrentStream)
      i = i+1
    
    TrueStreamList = list(x for x in StreamList if len(x)>3)

    return TrueStreamList;      


def StreamFollowDifficulty(mapID):
  pass

# for x in os.listdir('test/'):
#   if x.endswith('.osu'):
#     DectectStream('test/'+x)

DectectStream('test/boogie.osu')