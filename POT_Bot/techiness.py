import sharpness
import SharpnessComponent_Slider as SC_S
import os

def techiness(mapID):
    # Find the overall sharpness of the map:
    s = sharpness.sharpness(mapID)   
    # Find the slider following difficulty into the formula:
    sfd = SC_S.SliderFollowDifficulty(mapID)
    return s*sfd


for file in os.listdir('test'):
    if file.endswith(".osu"):
        print(file + ': ' + str(techiness('test/'+file)))
