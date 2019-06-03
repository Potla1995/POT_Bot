import re

def decryptFromDB(infilename,outfilename):
    with open(infilename,'r',encoding='utf-8') as f:
        f = f.read()
        L = f.split('\"')
        for x in L:
            if x in ['<div class=', ' title=', '><a href=', '><img src=', ' class=', '><span title=', 'Difficulty name', 'row truncate', 'row', '><a class=', 'Source',' alt=']:
               L.remove(x)
    
    with open(outfilename,'w',encoding='utf-8') as f:
        for x in L:
            f.write(x+'\n')

#decryptFromDB('maps_db.l.html')

class map(object):
    """A map object consists of Title, Artist, Mapper, DiffName, Length, Date, SR, AR, OD, BPM, Map Link"""
    def __init__(self,title,artist,mapper,diffname,length,date,sr,ar,od,bpm,mlink):
        self.mlink = mlink
        self.Title = title
        self.Artist = artist
        self.Mapper = mapper
        self.DiffName = diffname
        self.Length = length
        self.Date = date
        self.SR = sr
        self.AR = ar
        self.OD = od
        self.BPM = bpm

    def __str__(self):
        return "Map: %s - %s [%s] (by %s) SR%s AR%s OD%s %sBPM\nLink: %s" %(self.Artist, self.Title, self.DiffName, self.Mapper, self.SR, self.AR, self.OD, self.BPM, self.mlink)


def readIntoList(infilename,outfilename):
    with open(infilename,'r',encoding='utf-8') as f:
        f = f.read()
        L = f.split('\n')
        FinalList = []
        mapIndex = 0
        i = 0
        while i < len(L):
            flag = False
            if L[i][0:4]=='http':
                mlink = L[i]
            elif L[i]=='truncate beatmap-title':
                title = L[i+1]
            elif L[i]=='Artist':
                artist = L[i+1]
            elif L[i]=='Mapper':
                mapper = L[i+1]
            elif L[i]=='Difficulty name':
                diffname = L[i+1]
                diffname = diffname.split('[')[1].split(']')[0]
            elif L[i]=='Playable length':
                length = L[i+1][1:6]
            elif L[i]=='Date approved or last updated':
                date = L[i+1][0:11]
            elif L[i]=='Star difficulty':
                sr = L[i+3][1:5]
                sr = re.sub("<|>|/|d","",sr)
            elif L[i]=='Approach rate':
                ar = L[i+3][1:5]
                ar = re.sub("<|>|/|d","",ar)
            elif L[i]=='Overall difficulty':
                od = L[i+3][1:5]
                od = re.sub("<|>|/|d","",od)
            elif L[i]=='Beats per minute':
                bpm = L[i+3][1:5]
                bpm = re.sub("<|>|/|d","",bpm)
                mapIndex+=1
                flag = True
            i+=1
            if flag:
                FinalList.append(map(title,artist,mapper,diffname,length,date,sr,ar,od,bpm,mlink))
        with open(outfilename,'w',encoding='utf-8') as f:
            for x in FinalList:
                f.write("%s@?@%s@?@%s@?@%s@?@%s@?@%s@?@%s@?@%s@?@%s@?@%s@?@%s\n" %(x.Title,x.Artist,x.Mapper,x.DiffName,x.Length,x.Date,x.SR,x.AR,x.OD,x.BPM,x.mlink))


def readFromTXT(infilename):
    with open(infilename,'r',encoding='utf-8') as f:
        FinalList = []
        f = f.read().split('\n')
        f.pop()
        for x in f:
            L=x.split('@?@')
            #print (L)
            FinalList.append(map(L[0],L[1],L[2],L[3],L[4],L[5],L[6],L[7],L[8],L[9],L[10]))
        return FinalList
