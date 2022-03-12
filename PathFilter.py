import os.path as osp
import glob
from typing import List

"""
AIST-bars naming convention:
    <dance genre>_<dance type>_<camera>_<dancer ID>_<music ID>_<choreography ID>_<bar ID>.pkl
"""

class PathFilter(object):
    dance_genres = ["gBR", "gPO", "gLO", "gMH", "gLH", "gHO", "gWA", "gKR", "gJS", "gJB"]
    dance_types = ["sBM", "sFM"]
    music_IDs = ["0", "1", "2", "3", "4", "5"]

    @staticmethod
    def filter(base_path:str, dance_genres, dance_types, music_IDs):
        if type(dance_genres) != list:
            dance_genres = PathFilter.dance_genres
        if type(dance_types) != list:
            dance_types = PathFilter.dance_types
        if type(music_IDs) != list:
            music_IDs = PathFilter.music_IDs

        print (dance_genres)
        print (dance_types)
        print (music_IDs)

        ret = []
        for path in sorted(glob.glob(osp.join(base_path, "*.pkl"))):
            #filename = path.split("/")[-1].replace(".pkl", "")
            #d_genre, d_type, _, _, m_id, _, _ = filename.split("_")
            #m_id = m_id[-1]
            #if d_genre in dance_genres and d_type in dance_types and m_id in music_IDs:
            #   ret.append(path)
            ret.append(path)
        return ret

if __name__ == "__main__":
    base_path = "./MotionsPerMeasure"

    for dance_type in [["sBM"], ['sFM']]:
        for bpm in [["0"], ["1"], ["2"], ["3"], ["4"], ["5"]]:
            paths = PathFilter.filter(base_path, dance_genres=None,  dance_types=dance_type, music_IDs=bpm)
            print (dance_type, bpm, len(paths), paths[0])
            genres = {}
            for path in paths:
                genre = path.split("/")[-1].split("_")[0]
                if genre not in genres:
                    genres[genre] = 0
                genres[genre] += 1
            print ("\t", genres)
            for path in paths:
                print (path)
            break
        break

    print ("Pass")
