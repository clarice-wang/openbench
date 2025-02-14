import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="parses different settings")
    parser.add_argument("--script_path", type=str, default="scripts/job/data_scientist_normal.json")
    return parser.parse_args()