
import sys
from typing import Dict
from SmplObject import SmplObjects
import os
from scipy.spatial.transform import Rotation as R
import numpy as np

try:
    from FbxCommon import *
    from fbx import *
except ImportError:
    print("Error: module FbxCommon failed to import.\n")
    print("Copy the files located in the compatible sub-folder lib/python<version> into your python interpreter site-packages folder.")
    import platform
    if platform.system() == 'Windows' or platform.system() == 'Microsoft':
        print('For example: copy ..\\..\\lib\\Python27_x64\\* C:\\Python27\\Lib\\site-packages')
    elif platform.system() == 'Linux':
        print('For example: cp ../../lib/Python27_x64/* /usr/local/lib/python2.7/site-packages')
    elif platform.system() == 'Darwin':
        print('For example: cp ../../lib/Python27_x64/* /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')

class FbxReadWrite(object):
    def __init__(self, fbx_source_path):
        # Prepare the FBX SDK.
        lSdkManager, lScene = InitializeSdkObjects()
        self.lSdkManager = lSdkManager
        self.lScene = lScene

        # Load the scene.
        # The example can take a FBX file as an argument.
        print("\nLoading File: {}".format(fbx_source_path))
        lResult = LoadScene(self.lSdkManager, self.lScene, fbx_source_path)
        if not lResult:
            raise Exception("An error occured while loading the scene :(")

    def _write_curve(self, lCurve:FbxAnimCurve, data:np.ndarray):
        """
        data: np.ndarray of (N, )
        """
        lKeyIndex = 0
        lTime = FbxTime()
        lTime.SetGlobalTimeMode(FbxTime.eFrames60) # Set to fps=60
        data = np.squeeze(data)

        lCurve.KeyModifyBegin()
        for i in range(data.shape[0]):
            lTime.SetFrame(i, FbxTime.eFrames60)
            lKeyIndex = lCurve.KeyAdd(lTime)[0]
            lCurve.KeySetValue(lKeyIndex, data[i])
            lCurve.KeySetInterpolation(lKeyIndex, FbxAnimCurveDef.eInterpolationCubic)
        lCurve.KeyModifyEnd()

    def addAnimation(self, pkl_filename:str, smpl_params:Dict, verbose:bool = False):
        lScene = self.lScene

        # 0. Set fps to 60
        lGlobalSettings = lScene.GetGlobalSettings()
        if verbose==True:
            print ("Before time mode:{}".format(lGlobalSettings.GetTimeMode()))
        lGlobalSettings.SetTimeMode(FbxTime.eFrames60)
        if verbose==True:
            print ("After time mode:{}".format(lScene.GetGlobalSettings().GetTimeMode()))

        self.destroyAllAnimation()

        lAnimStackName = pkl_filename
        lAnimStack = FbxAnimStack.Create(lScene, lAnimStackName)
        lAnimLayer = FbxAnimLayer.Create(lScene, "Base Layer")
        lAnimStack.AddMember(lAnimLayer)
        lRootNode = lScene.GetRootNode()

        names = SmplObjects.joints

        # 1. Write smpl_poses
        smpl_poses = smpl_params["smpl_poses"]
        for idx, name in enumerate(names):
            node = lRootNode.FindChild(name)
            rotvec = smpl_poses[:, idx*3:idx*3+3]
            _euler = []
            for _f in range(rotvec.shape[0]):
                r = R.from_rotvec([rotvec[_f, 0], rotvec[_f, 1], rotvec[_f, 2]])
                euler = r.as_euler('xyz', degrees=True)
                _euler.append([euler[0], euler[1], euler[2]])
            euler = np.vstack(_euler)

            lCurve = node.LclRotation.GetCurve(lAnimLayer, "X", True)
            if lCurve:
                self._write_curve(lCurve, euler[:, 0])
            else:
                print ("Failed to write {}, {}".format(name, "x"))

            lCurve = node.LclRotation.GetCurve(lAnimLayer, "Y", True)
            if lCurve:
                self._write_curve(lCurve, euler[:, 1])
            else:
                print ("Failed to write {}, {}".format(name, "y"))

            lCurve = node.LclRotation.GetCurve(lAnimLayer, "Z", True)
            if lCurve:
                self._write_curve(lCurve, euler[:, 2])
            else:
                print ("Failed to write {}, {}".format(name, "z"))

        # 3. Write smpl_trans to f_avg_root
        smpl_trans = smpl_params["smpl_trans"]
        name = "root"
        node = lRootNode.FindChild(name)
        lCurve = node.LclTranslation.GetCurve(lAnimLayer, "X", True)
        if lCurve:
            self._write_curve(lCurve, smpl_trans[:, 2])
        else:
            print ("Failed to write {}, {}".format(name, "x"))

        lCurve = node.LclTranslation.GetCurve(lAnimLayer, "Y", True) # Translation on the Y axis (in blender, this is not the vertical axis but one of the axis that forms the horizontal plane)
        if lCurve:
            self._write_curve(lCurve, smpl_trans[:, 0])
        else:
            print ("Failed to write {}, {}".format(name, "y"))

        lCurve = node.LclTranslation.GetCurve(lAnimLayer, "Z", True)
        if lCurve:
            self._write_curve(lCurve, smpl_trans[:, 1])
        else:
            print ("Failed to write {}, {}".format(name, "z"))

    def writeFbx(self, write_base:str, filename:str):
        if os.path.isdir(write_base) == False:
            os.makedirs(write_base, exist_ok=True)
        write_path = os.path.join(write_base, filename.replace(".pkl", ""))
        print ("Writing to {}".format(write_path))
        lResult = SaveScene(self.lSdkManager, self.lScene, write_path)

        if lResult == False:
            raise Exception("Failed to write to {}".format(write_path))

    def destroy(self):
        self.lSdkManager.Destroy()

    def destroyAllAnimation(self):
        lScene = self.lScene
        animStackCount = lScene.GetSrcObjectCount(FbxCriteria.ObjectType(FbxAnimStack.ClassId))
        for i in range(animStackCount):
            lAnimStack = lScene.GetSrcObject(FbxCriteria.ObjectType(FbxAnimStack.ClassId), i)
            lAnimStack.Destroy()
