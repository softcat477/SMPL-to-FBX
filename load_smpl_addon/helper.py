import sys
import subprocess
import logging
from typing import Dict

import numpy as np

SMPL_JOINT_NAMES = {
    0:  'Pelvis',
    1:  'L_Hip',        4:  'L_Knee',            7:  'L_Ankle',           10: 'L_Foot',
    2:  'R_Hip',        5:  'R_Knee',            8:  'R_Ankle',           11: 'R_Foot',
    3:  'Spine1',       6:  'Spine2',            9:  'Spine3',            12: 'Neck',            15: 'Head',
    13: 'L_Collar',     16: 'L_Shoulder',       18: 'L_Elbow',            20: 'L_Wrist',         22: 'L_Hand',
    14: 'R_Collar',     17: 'R_Shoulder',       19: 'R_Elbow',            21: 'R_Wrist',         23: 'R_Hand',
}
smpl_joints = len(SMPL_JOINT_NAMES) 

# Install dependencies
def InstallScipy():
    try:
        from scipy.spatial.transform import Rotation as R
    except ModuleNotFoundError as e:
        python_exe = sys.executable
        subprocess.call([python_exe, "-m", "ensurepip"])
        ret = subprocess.run([python_exe, "-m", "pip", "install", "scipy"])
        if ret.returncode != 0:
            logging.error(f"Failed to install scipy")
        else:
            logging.info(f"Install scipy!")
    except Exception as e:
        raise e

InstallScipy()
from scipy.spatial.transform import Rotation as R

def UninstallScipy():
    python_exe = sys.executable
    subprocess.call([python_exe, "-m", "ensurepip"])
    ret = subprocess.run([python_exe, "-m", "pip", "uninstall", "-y", "scipy"])
    if ret.returncode != 0:
        logging.error(f"Failed to uninstall scipy")
    else:
        logging.info(f"Uninstall scipy!")

def GetAnimation(smpl_params:Dict):
    names = [SMPL_JOINT_NAMES[k] for k in sorted(SMPL_JOINT_NAMES.keys())]

    # 1. Write smpl_poses
    rotation_euler_xyz = {}
    smpl_poses = smpl_params["smpl_poses"]
    for idx, name in enumerate(names):
        rotvec = smpl_poses[:, idx*3:idx*3+3]
        _euler = []
        for _f in range(rotvec.shape[0]):
            r = R.from_rotvec([rotvec[_f, 0], rotvec[_f, 1], rotvec[_f, 2]])
            euler = r.as_euler('xyz', degrees=False)
            _euler.append([euler[0], euler[1], euler[2]])
        euler = np.vstack(_euler)
        rotation_euler_xyz[name] = euler

    translation_front_up_right = smpl_params["smpl_trans"]

    return rotation_euler_xyz, translation_front_up_right