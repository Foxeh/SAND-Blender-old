from bge import logic
import random
import pickle



def _saveScoresToFile(list_scores, string_filepath):
    
    # Write scores to file
    file = open(string_filepath, "wb")
    pickle.dump(list_scores, file)
    file.close()



def _loadScoresFromFile(string_filepath):
    
    # Load saved scores (from file)
    try:
        file = open(string_filepath, "rb")
    except IOError:
        # Failed to load
        # TODO: add logging
        return []
        
        
    return pickle.load(file)





scores = _loadScoresFromFile("scores.scr")

def display():
    
    # Scene/Object Setup
    scene = logic.getCurrentScene()
    writer = scene.objectsInactive["Writer"]
    
    
    # Set initials and score
    # TODO: Remove random, and get scores from game
    tempInitials = logic.globalDict["initials"]
    initials = tempInitials[:3].upper()
    score = random.randrange(0, 25)
    
    
    # Save data
    tup_entry = (initials, score)
    scores.append(tup_entry)
    
    
    # Sort scores
    scores.sort(key=lambda entry: entry[1])
    scores.reverse()
    
    
    # Display scores
    for entry, i in zip(scores, range(len(scores))):
        new_writer = scene.addObject(writer, writer)
        new_writer["Text"] = "{:d}. {:s} - {:d}".format(i + 1, entry[0], entry[1])
        
        new_writer.worldPosition.y -= 1.25 * i
        
    _saveScoresToFile(scores, "scores.scr")
    
    
    
def setInitials():
    
    scene = logic.getCurrentScene()
    initials = scene.objects["Initials"]
    logic.globalDict["initials"] = initials["Text"].strip()
    
