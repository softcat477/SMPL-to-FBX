"""
   Copyright (C) 2017 Autodesk, Inc.
   All rights reserved.

   Use of this software is subject to the terms of the Autodesk license agreement
   provided at the time of installation or download, or which otherwise accompanies
   this software in either electronic or hard copy form.
 
"""

from FbxReadWriter import FbxReadWrite
from SmplObject import SmplObjects
import argparse
import tqdm

def getArg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_pkl_base', type=str, required=True)
    parser.add_argument('--fbx_source_path', type=str, required=True)
    parser.add_argument('--output_base', type=str, required=True)

    return parser.parse_args()

if __name__ == "__main__":
    args = getArg()
    input_pkl_base = args.input_pkl_base
    fbx_source_path = args.fbx_source_path
    output_base = args.output_base

    smplObjects = SmplObjects(input_pkl_base)
    for pkl_name, smpl_params in tqdm.tqdm(smplObjects):
        try:
            fbxReadWrite = FbxReadWrite(fbx_source_path)
            fbxReadWrite.addAnimation(pkl_name, smpl_params)
            fbxReadWrite.writeFbx(output_base, pkl_name)
        except Exception as e:
            fbxReadWrite.destroy()
            print ("- - Distroy")
            raise e

