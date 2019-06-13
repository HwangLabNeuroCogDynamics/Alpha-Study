circles=[polygon1,polygon2]
squares=....

faces_dict={}
place_dict={}

fills=['empty','full']
colors=['red','blue']
stims=['face','places']


stimList=[]
for f in fills:
    for c in colors:
        for s in stims:
            stimList.append({'shape':f,'color':c,'stim':s})
            

print(stimList)


for thisTrial in trialHandler:
    
    if thisTrial['stim']=='face':
        thisFace=np.random.choice(place_dict.keys(),1)
        thisFace=faces_dict[thisFace]
        thisStim=thisFace
    elif thisTrial['stim']=='place':
         --
        thisStim=thisPlace
    
    if thisTrial['color']=='red':
        thisStim.setColor==red
    elif:
        ....
    
    if thisStim.status != done:
        do whatever  
        
        