import urllib.request
import sys
import os;

#Usual URL https://osu.ppy.sh/beatmapsets/705788#osu/1492654
beatmapsetID = sys.argv[1::]

for i in range(len(beatmapsetID)):
    beatmapset = beatmapsetID[i].split('/')[-1];
    urllib.request.urlretrieve('https://osu.ppy.sh/osu/'+ beatmapset, 'test/'+beatmapset+'.osu')
    rename = ''
    with open('test/'+beatmapset+'.osu','r',encoding='utf-8') as f:
        L = f.read().split('\n')
        Index = L.index('[Metadata]')
        rename = L[Index+1].split(':')[1]
        os.rename('test/'+beatmapset+'.osu','test/'+rename+'.osu')