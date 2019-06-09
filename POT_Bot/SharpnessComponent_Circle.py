import math
from statistics import mean
import os

def BeatInterval(mapID): #Identifies the BPM of any given map.
  BPM = 0
  with open(mapID,'r',encoding='utf-8') as f:
    L = f.read().split('\n')
    J = L.index('[TimingPoints]') + 1
    BPM = L[J].split(',')[1]
  #60*1000/float(BPM) is the formula for obtaining the true BPM. 
  return BPM



for x in os.listdir('test/'):
  if x.endswith('.osu'):
    BeatInterval('test/'+x);