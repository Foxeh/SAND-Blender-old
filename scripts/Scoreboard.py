from bge import logic

scores = []

def display():
    
    scene = logic.getCurrentScene()
    writer = scene.objects["Writer"]
    
    name = logic.globalDict["initials"]
    score = 9
    
    tup_entry = (name, score)
    scores.append(tup_entry)
    scores.sort(key=lambda entry: entry[1])
    scores.reverse()
    
    for entry, i in zip(scores, range(len(scores)):
        new_writer = scene.addObject(writer, writer)
        new_writer["Text"] = "{:d}.  {:s} - {:d}".format(i + 1, entry[0], entry[1])
        
        new_writer.worldPosition.y -= 1.25 * i
        new_writer.localScale = writer.localScale
    
    
def setInitials():
    
    scene = logic.getCurrentScene()
    initials = scene.objects["Initials"]
    
    logic.globalDict["initials"] = initials["Text"].strip() 

