from __future__ import print_function

import collections
#import subprocess
import sys
import re
import os
import time
#import sqlite3
import logging
import pickle


DEBUG = False # the code below will switch this to True automaticaly if this file is __main__

CURRENT_PATH = os.getcwd() + "/"
GCODES_PATHES_FOLDER = CURRENT_PATH
PATH_TO_DB = CURRENT_PATH + "../databasesqlite/db/Prefs.db"
LEVELING_FILE_NAME = "levelling.gcode"
HOMING_FILE_NAME = "homing.gcode"
TOOL_SWITCH_TO_T0_FILE_NAME = "T0code.gcode"
TOOL_SWITCH_TO_T1_FILE_NAME = "T1code.gcode"

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

coords_re = {}
re_template = "COORD([-+]?\d+\.?\d+)"
for coord in ("X", "Y", "Z"):
    coords_re[coord] = re.compile(re_template.replace("COORD", coord))


def load_patch_file(filename):
    with open(filename) as f:
        gcodes = f.read()
    gcodes = gcodes.replace("\r", "").replace("\t", "").split("\n")
    gcodes = [line.split(";")[0].strip() for line in gcodes]
    gcodes = filter(lambda line:line, gcodes)
    return list(gcodes)


def load_homing_gcodes():
    return load_patch_file(GCODES_PATHES_FOLDER + HOMING_FILE_NAME)


def load_switching_to_t0_gcodes():
    return load_patch_file(GCODES_PATHES_FOLDER + TOOL_SWITCH_TO_T0_FILE_NAME)


def load_switching_to_t1_gcodes():
    return load_patch_file(GCODES_PATHES_FOLDER + TOOL_SWITCH_TO_T1_FILE_NAME)


def load_leveling_gcodes(z_offset, parent=None):
    gcodes = load_patch_file(GCODES_PATHES_FOLDER + LEVELING_FILE_NAME)
    t0_switching = load_switching_to_t0_gcodes()
    t0_index = gcodes.index("T0") + 1
    gcodes[t0_index:t0_index] = t0_switching
    print("voy a insertar el levelling")
    gcodes.insert(-1,  "G30 Z-" + z_offset)
    print("lo inserte")
    logger.info("Leveling offset from db:" + z_offset)
    return gcodes


def apply_coord_re_to_line(coord_name, line, parent):
    match = coords_re[coord_name].search(line)
    if match:
        try:
            coord = float(match.group(1))
        except (IndexError, TypeError, ValueError):
            error_message = "Invalid gcode in line: " + str(line)
            logger.info(error_message)
            #if parent:
            #    parent.register_error(987, message, is_blocking = False)
            coord = None
        return coord


#TODO refactor this mess
def patch_and_split_gcodes(gcodes_file, z_offset, parent=None):
    switching_to_t0_gcodes = load_switching_to_t0_gcodes()
    switching_to_t1_gcodes = load_switching_to_t1_gcodes()
    leveling_gcodes = load_leveling_gcodes(z_offset, parent)
    gcodes = collections.deque()
    leveling_was_added = False
    X_coord = None
    Y_coord = None
    Z_coord = None
    switching_gcodes_to_append = None
    after_switching_buffer = []
    while True:
        line = gcodes_file.readline()
        if not line:
            if after_switching_buffer:
                gcodes.extend(switching_gcodes_to_append)
                gcodes.extend(after_switching_buffer)
            break
        line = line.split(";")[0] #strip comments
        line = line.replace("\n", "").replace("\r", "").replace("\t", "").strip()
        if not line:
            continue
        if switching_gcodes_to_append:
            search_result = apply_coord_re_to_line("X", line, parent)
            if search_result is not None:
                X_coord = search_result
            search_result = apply_coord_re_to_line("Y", line, parent)
            if search_result is not None:
                Y_coord = search_result
            if X_coord is not None and Y_coord is not None:
                if DEBUG:
                    gcodes.append(";Tool switching starts")
                gcodes.extend(switching_gcodes_to_append)
                gcodes.append("G1 X%f Y%f" % (X_coord, Y_coord))
                if Z_coord is not None:
                    gcodes.append("G1 Z%f"  % Z_coord)
                gcodes.extend(after_switching_buffer)
                gcodes.append(line)
                if DEBUG:
                    gcodes.append(";Tool switching ends")
                switching_gcodes_to_append = None
                after_switching_buffer = []
                X_coord = None
                Y_coord = None
            else:
                after_switching_buffer.append(line) #TODO remove copy-paste 
                if not leveling_was_added and "G28" in line and not "X" in line and not "Y" in line and not "Z" in line:
                    if DEBUG:
                        after_switching_buffer.append(";Leveling starts")
                    print("meto leveling1")
                    after_switching_buffer.extend(leveling_gcodes)
                    #gcodes.extend(after_switching_buffer)
                    if DEBUG:
                        after_switching_buffer.append(";Leveling ends")
                    leveling_was_added = True
        else:
            gcodes.append(line) #TODO remove copy-paste 
            if not leveling_was_added and "G28" in line and not "X" in line and not "Y" in line and not "Z" in line:
                if DEBUG:
                    gcodes.append(";Leveling starts")
                print("meto leveling2")
                gcodes.extend(leveling_gcodes)
                if DEBUG:
                    gcodes.append(";Leveling ends")
                leveling_was_added = True
            search_result = apply_coord_re_to_line("Z", line, parent)
            if search_result:
                Z_coord = search_result
            if line[0] == "T" and len(line) >= 2:
                if line[1] == "0":
                    switching_gcodes_to_append = switching_to_t0_gcodes
                elif line[1] == "1":
                    switching_gcodes_to_append = switching_to_t1_gcodes
    if not leveling_was_added:
        error_message = "No leveling gcodes were added - probably no G28 line without XYZ"
        logger.info(error_message)
        if DEBUG:
            gcodes.append(";" + error_message)
        if parent:
            parent.register_error(985, error_message, is_blocking = False)
    nasty_thing = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    while nasty_thing in gcodes: gcodes.remove(nasty_thing)
    return gcodes


if __name__ == "__main__":
    DEBUG = True
    print("empece")
    with open("Ext1__PLATough_CableProtector.gcode") as f:
        print("hago mi mierda")
        patch_start = time.time()
        patched = patch_and_split_gcodes(f)
        with open("cosa.gcode", 'wb') as f:
            pickle.dump(patched, f)
        patch_time = time.time() - patch_start
        print("termine: {}".format(patch_time))
        if DEBUG:
            logger.info("\n".join(patched))
            logger.info(";Patching time: %fs" % patch_time)

