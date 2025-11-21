import datetime
import json
import os
import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds
import random as rand
import argparse
import logging


relative_path = os.getcwd() # takes the current directory path


logger = logging.getLogger(__name__)
FORMAT = "[%(asctime)s][%(module)s][%(created)f] %(msg)s"
logging.basicConfig(level=logging.ERROR, format=FORMAT)


logger.info('Object Creation and Scatter Script')

def take_input():
    value = input("Enter an amount of objects to create | Enter 0 for a random amount of objects between 1-100 \n")

    try:
        value = int(value)
        
                
        if value < 0:
            logger.error('Input cannot be negative')
        elif value == 0:
            create_spheres_and_rename_random()
        else:
            create_spheres_and_rename_set(value)
        
    except ValueError:
        logger.error('Input must be an whole value')
    
def create_file_path(): #chatgpt was used to create to help get the file path here

    if not os.path.exists(os.path.join(relative_path, "workspace.mel")): # os.path.join is from chatgpt, not my own work # checks if the file path exists to a workspace
        cmds.workspace(relative_path, newWorkspace=True) # creates new workspace if one doesn't exist
    cmds.workspace(relative_path, openWorkspace=True)

    file_name = os.path.join(relative_path, "rpy26-ANIM435-2025-WK07.ma") # os.path.join is from chatgpt, not my own work

    cmds.file(rename=file_name)

    take_input()

def create_spheres_and_rename_set(value):
    if value > 100 and value <= 1000:
        logger.warning('Amount of objects is larger than 100, this may take a moment')

    if value > 1000:
        logger.warning('Amount of objects is larger than 1000, this will take a moment')

    spheres_total = []
    for i in range(0, value):
        sphere = cmds.polySphere()[0] # creates spheres
        spheres_total.append(sphere) # addes sphere to list

    
    for i in range(len(spheres_total)): # for loop, for each sphere
        cmds.rename(spheres_total[i], f"scene_object_{i}") # renames spheres

        x = rand.randint(-10,10) # gets random units for scatter
        y = rand.randint(-10,10)
        z = rand.randint(-10,10)
        
        cmds.setAttr(f"scene_object_{i}" +".translateX", x) # sets translation attributes to random numbers
        cmds.setAttr(f"scene_object_{i}" +".translateY", y)
        cmds.setAttr(f"scene_object_{i}" +".translateZ", z)

    cmds.file(save=True, type="mayaAscii")
 

def create_spheres_and_rename_random(): # creates a random amount of spheres, from 5-20, and scatters them into a maya scene
    spheres_total = []
    for i in range(rand.randint(5,20)):
        sphere = cmds.polySphere()[0] # creates spheres
        spheres_total.append(sphere) # addes sphere to list

    for i in range(len(spheres_total)): # for loop, for each sphere
        cmds.rename(spheres_total[i], f"scene_object_{i}") # renames spheres

        x = rand.randint(-10,10) # gets random units for scatter
        y = rand.randint(-10,10)
        z = rand.randint(-10,10)
        
        cmds.setAttr(f"scene_object_{i}" +".translateX", x) # sets translation attributes to random numbers
        cmds.setAttr(f"scene_object_{i}" +".translateY", y)
        cmds.setAttr(f"scene_object_{i}" +".translateZ", z)
    cmds.file(save=True, type="mayaAscii")
    date_time_data(spheres_total)


def date_time_data(spheres_total):
    now = (datetime.datetime.now())
    
    json_write(spheres_total, now)

def json_write(spheres_total):
    scene_data = {
    
        "spheres_total": spheres_total,
        "time": now
    }
    
    f = open('scene_data.json','w')
    file = json.dump(scene_data, f)
    
create_file_path()
maya.standalone.uninitialize() # stops running standalone, read that it was a good practice, let me know if I'm wrong

