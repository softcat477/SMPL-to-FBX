import numpy as np
import glob
import pickle
import os

from typing import Dict
from typing import Tuple

from PathFilter import PathFilter

class SmplObjects(object):
    joints = ["Pelvis"
    ,"L_Hip"
    ,"R_Hip"
    ,"Spine1"

    ,"L_Knee"
    ,"R_Knee"
    ,"Spine2"

    ,"L_Ankle"
    ,"R_Ankle"
    ,"Spine3"

    ,"L_Foot"
    ,"R_Foot"
    ,"Neck"

    ,"L_Collar"
    ,"R_Collar"

    ,"Head"
    ,"L_Shoulder"
    ,"R_Shoulder"

    ,"L_Elbow"
    ,"R_Elbow"
    ,"L_Wrist"
    ,"R_Wrist"
    ,"L_Hand"
    ,"R_Hand"]
    def __init__(self, read_path):
        self.files = {}

        # For AIST naming convention
        #paths = PathFilter.filter(read_path, dance_genres=["gBR"],  dance_types=["sBM"], music_IDs=["0"])
        paths = PathFilter.filter(read_path, dance_genres=None,  dance_types=None, music_IDs=None)
        for path in paths:
            filename = path.split("/")[-1]
            with open(path, "rb") as fp:
                data = pickle.load(fp)
            self.files[filename] = {"smpl_poses":data["smpl_poses"],
                                    "smpl_trans":data["smpl_trans"] / (data["smpl_scaling"][0]*100)}
        self.keys = [key for key in self.files.keys()]

    def __len__(self):
        return len(self.keys)

    def __getitem__(self, idx:int) -> Tuple[str, Dict]:
        key = self.keys[idx]
        return key, self.files[key]
