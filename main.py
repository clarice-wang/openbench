import os
import sys
import numpy as np
sys.path.append('./src')
from parse import parse_args
from conversation import make_conversation_dynamic

def find_instances(target_dir):
    instances = []
    for _, _, filenames in os.walk(target_dir):
        for fname in filenames:
            if fname.endswith(".json") and 'sales_manager' not in fname:
                instances.append(fname[:-5])
    return instances

def update_metrics(m, delta):
    for k, v in delta.items():
        if k not in m:
            m[k] = []
        m[k].append(v)

def agg_metrics(m):
    return {k:np.mean(v) for k, v in m.items()}

args = parse_args() # take arguments from the command line

# make backbone_configs
backbone_configs = {
    "a": {
        "model": args.a_model,
        "api_key": args.a_api_key,
        "temp": args.a_temp,
        "top_p": args.a_top_p,
        "end_point": None
    },
    "b": {
        "model": args.b_model,
        "api_key": args.b_api_key,
        "temp": args.b_temp,
        "top_p": args.b_top_p,
        "end_point": None
    },
    "c": {
        "model": args.c_model,
        "api_key": args.c_api_key,
        "temp": args.c_temp,
        "top_p": args.c_top_p,
        "end_point": None
    }
}

# find all instances in the job
instance_dir = args.instance_dir
q_dir = args.q_dir
log_dir = args.log_dir + "/" + args.a_model + "/"
# establish the log directory for the a model if not exists
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
instances = find_instances(instance_dir)
print(f"now start to run following instances: {instances}")
if "job" in instance_dir:
    role_a = "Interviewer"
    role_b = "Interviewee"
    sce = "job interview"
elif "guest" in instance_dir:    
    role_a = "Host"
    role_b = "Guest"
    sce = "podcast interview"
elif "buyer" in instance_dir:
    role_a = "Salesperson"
    role_b = "Buyer"
    sce = "b2b negotiation"
else:
    raise ValueError("instance_dir must contain 'job' or 'guest' or 'buyer'")

all_ins_metrics = {}
for ins in instances:
    print(f'now start to run instance: {ins}')
    ins_script_path = instance_dir + "/" + ins + ".json"
    ins_q_path = q_dir + "/" + ins + "_q.json"
    log_ins_dir = log_dir + "/" + ins + "/"
    # make conversation
    all_metrics_3 = {}
    for t in range(3):
        print(f't={t}')
        conv = make_conversation_dynamic(ins_script_path, ins_q_path, backbone_configs, args.itr_num, role_a, role_b, sce)
        cost_a = conv.run(cal_price=True) # calculate the cost of agent a
        all_metrics = conv.evaluate_performance()
        all_metrics['cost_a'] = cost_a # add the cost of agent a to the metrics
        print(f"metrics: {all_metrics}")
        if not os.path.exists(log_ins_dir):
            os.makedirs(log_ins_dir)
        conv.log_conversation(log_ins_dir)
        update_metrics(all_metrics_3, all_metrics)

    all_ins_metrics[ins] = agg_metrics(all_metrics_3)
print(all_ins_metrics)
