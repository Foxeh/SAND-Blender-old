from bge import logic

def display():
    
    scene = logic.getCurrentScene()
    writer = scene.objects["Writer"]
    
    # Assigning rank and score temporarily
    # TODO: Get score from game, rank them, and save to disk
    rank = 1
    initials = logic.globalDict["initials"]
    score = 15
    
    
    tup_entry = (rank, initials, score)
    
    writer["Text"] = "{:d}. {:s} - {:d}".format(*tup_entry)
    
    
def setInitials():
    
    scene = logic.getCurrentScene()
    initials = scene.objects["Initials"]
    
    logic.globalDict["initials"] = initials["Text"].strip()
    
