# python3 main.py 	--instance_dir ./data/scripts/job \
# 						--q_dir ./data/questionnaires \
# 						--itr_num 10 \
# 						--a_model gpt-4o \
# 						--a_temp 1.0 \
# 						--a_top_p 1.0 \

python3 main.py 	--instance_dir ./data/scripts/buyer \
						--q_dir ./data/questionnaires \
						--itr_num 10 \
						--a_model gpt-4o \
						--a_temp 1.0 \
						--a_top_p 1.0 \

python3 main.py 	--instance_dir ./data/scripts/guest \
						--q_dir ./data/questionnaires \
						--itr_num 10 \
						--a_model gpt-4o \
						--a_temp 1.0 \
						--a_top_p 1.0 \
