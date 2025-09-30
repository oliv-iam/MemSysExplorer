# <imports / functions>
import os
import argparse
import random
import subprocess
import json

def parse_args():
    parser = argparse.ArgumentParser(
        description="Data For Running MemSysExplorer run.py"
    )

    # Parsing cfg file
    parser.add_argument(
        "--tech_config",
        type=str,
        default=None,
        help="Path to the tech config and if not provided, run.py will find the next best one"
    )
    args = parser.parse_args()

    config = {}
    if args.tech_config is not None:
        with open(args.tech_config, "r") as f:
            config = json.load(f)

    return config

if __name__ == '__main__':
    
    # get apps benchmark, tech config as arguments
    # pull read/write info from apps benchmark
    # run tech side -> read/write latency & power
    # calculations (total time / power)
    # dump apps output, tech output, totals in csv

    # Debug Variables
    PRINT_ON = True
    # Reserves json from parse_args
    config = parse_args()

    # Assume we have pulled the apps here
    apps_data = []

    # Parsing chosen config
    chosen_config_path = None

    if "tech_config" in config:
        tech_config = config["tech_config"]

    # Useful var for processes
    Tech_Dir = os.path.join("tech", "ArrayCharacterization")

    if chosen_config_path is None:
        # Pulling Our Configs
        CONFIG_DIR = os.path.join("tech", "ArrayCharacterization", "sample_configs")
        tech_configs = []
        for root, _, files in os.walk(CONFIG_DIR):
            for f in files:
                if f.endswith(".cfg"):
                    rel_path = os.path.relpath(os.path.join(root, f), start=Tech_Dir)
                    tech_configs.append(rel_path)

        #Statement to test if we pulled the files correctly
        if PRINT_ON:
            for cfg in tech_configs:
                print(cfg)
                print()
        
        # TODO: This should be by best matched 
        chosen_config_path = random.choice(tech_configs)

    # Checking to see if make has been ran in tech/ArrayCharacterization
    NVSim_File_Path = os.path.join(Tech_Dir, "nvsim")
    if not os.path.exists(NVSim_File_Path):
        if PRINT_ON:
            print("NVSim binary not found. Running make in tech/ArrayCharacterization now")
        subprocess.run(["make"], cwd=Tech_Dir)
    
    tech_result = subprocess.run(["./nvsim", chosen_config_path], capture_output=True, text=True, cwd=Tech_Dir)
    print(tech_result.stdout)

