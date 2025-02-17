import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="parses different settings")
    # instance
    parser.add_argument("--s_path", type=str, default="/data/scripts/job/data_scientist_normal.json")
    parser.add_argument("--q_path", type=str, default="/data/questionnaires/data_scientist_normal_q.json")
    # a params
    parser.add_argument("--a_model", type=str, default="gpt-4o")
    parser.add_argument("--a_temp", type=float, default=1.0)
    parser.add_argument("--a_top_p", type=float, default=0.9)
    parser.add_argument("--a_api_key", type=str, default=None)
    # b params
    parser.add_argument("--b_model", type=str, default="gpt-4o")
    parser.add_argument("--b_temp", type=float, default=1.0)
    parser.add_argument("--b_top_p", type=float, default=0.9)
    parser.add_argument("--api_key", type=str, default=None)
    # c params
    parser.add_argument("--c_model", type=str, default="gpt-4o")
    parser.add_argument("--c_temp", type=float, default=1.0)
    parser.add_argument("--c_top_p", type=float, default=0.9)
    parser.add_argument("--api_key", type=str, default=None)
    return parser.parse_args()
