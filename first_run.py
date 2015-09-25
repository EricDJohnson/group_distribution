#!/usr/bin/python
import random

extract_scores = lambda y:y["test_score"]

def score_group(group):
    return sum(map(extract_scores,group))/len(group)

def group_scores(chosen,available,desired_length):
    #terminal case: we have what we need
    if len(chosen) == desired_length: 
        return [{"identifier": chosen, "score": score_group(chosen)}]
    results = []
    for user in available:
        if user in chosen: continue
        results = results + group_scores(chosen + [user], available, desired_length)
    return results


master_users = []
for i in range(1,10):
    master_users.append({ "test_score": random.randint(0,100) })

print group_scores([],master_users,3)
