from bge import logic
import random
import pickle
from Logging import Logging
import os


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





scores = _loadScoresFromFile("/Users/GRAPHICSDEMO/Desktop/scores.txt")

def display():
    
    # Scene/Object Setup
    scene = logic.getCurrentScene()
    writer = scene.objectsInactive["Writer"]
    
    
    # Set initials and score
    # TODO: Remove random, and get scores from game
    tempInitials = logic.globalDict["initials"]
    initials = tempInitials[:3].upper()
    score = logic.globalDict["score"]

    
    # Save data
    tup_entry = (initials, score)
    scores.append(tup_entry)
    
    
    # Sort scores
    scores.sort(key=lambda entry: entry[1])
    scores.reverse()
    
    
    
    # Display scores
    for entry, i in zip(scores, range(len(scores))):
        new_writer = scene.addObject(writer, writer)
        new_writer["Text"] = "{:d}. {:s} - {:.0f}".format(i + 1, entry[0], entry[1])
        
        new_writer.worldPosition.y -= 1.10 * i
        

    _saveScoresToFile(scores, "/Users/GRAPHICSDEMO/Desktop/scores.txt")
    
    
    
def setInitials():
    
    scene = logic.getCurrentScene()
    initials = scene.objects["Initials"]
    logic.globalDict["initials"] = initials["Text"].strip()
    

def setScore():
    
    cont = logic.getCurrentController()
    score = cont.owner
    scoreValue = score["Text"]
    logic.globalDict["score"] = float(scoreValue[6:])
    
