#!/usr/bin/python
import random
import itertools 
import scipy.misc
import numpy

extract_scores = lambda y:y.score
class student:
    def __init__(self,id,score,previous_partners{1:2, 2:3,4:5}):
        self.id = id
        self.score = score
        self.previous_partners = previous_partners
    def __str__(self):
        return "%d" % self.score
    def __repr__(self):
        return self.__str__()
    def proximity(self,other):
        if other.id in self.previous_partners:
            return self.previous_partners[other.id]
        return 0
        
history_record = { "1": { "2": 2, "3": 3}}

def history_score_group(group):
    total_recurrences = 0
    for i in range(0, len(group)):
            for j in range(i+1,len(group)):
                total_recurrences += group[i].proximity(group[j])
    return total_recurrences

def test_score_group(group):
    return numpy.std(map(extract_scores,group))
    # return sum(map(extract_scores,group))/len(group)


def findsubsets(S,m):
        return set(itertools.combinations(S, m))

def students_in_groups(groups):
    students_included = 0
    for group in groups:
        students_included += len(group)
    return students_included

def groups_conflict(group_of_groups,new_group):
    for group in group_of_groups:
        for student in group:
            if student in new_group:
                return True
    return False

def all_possible_class_combinations(total_group_choices, total_student_size, chosen_groups=[],start=0):
    if total_student_size == students_in_groups(chosen_groups):
        # print("Found one! %s " % str(chosen_groups))
        return [chosen_groups]

    combinations = []
    for index in range(start,len(total_group_choices)):
        group = total_group_choices[index]
        if group in chosen_groups: continue
        if groups_conflict(chosen_groups, group): continue
        combinations += all_possible_class_combinations(total_group_choices, total_student_size, chosen_groups + [group],index)
    return combinations

total_class_size = 10
students_per_group = 4

master_class_list = []
for i in range(0,total_class_size):
    master_class_list.append(student(random.randint(0,100)))

total_group_choices = [] 
for number in range(students_per_group-1, students_per_group+1):
    print("Generating all possible combinations of size %d" % number)
    total_group_choices += findsubsets(master_class_list,number)
    print("After that the list is %d long" % len(total_group_choices))

print("Generated a list of %d group combinations\n" % len(total_group_choices))

print("Generating list of total class combinations")
all_possible = all_possible_class_combinations(total_group_choices,len(master_class_list))
for class_possibility in all_possible: 
    print("this is totally a possibility: %s \n\n" % str(class_possibility))

print("There were a total of %d possibilities given a class size of %d and group size around %d" % (len(all_possible), len(master_class_list), students_per_group))

class_summaries = {} 

for class_index in range(0,len(all_possible)):
    class_possibility = all_possible[class_index]
    total_of_std = 0
    for group in class_possibility:
        total_of_std += test_score_group(group)
        # total_of_history += history_score_group(group)
    std_average = total_of_std / float(len(class_possibility))
    class_summaries[class_index] = { "std_average": std_average}

print(class_summaries)
sorted_deviations = sorted(map(lambda k: class_summaries[k]['std_average'], class_summaries))
print("Least diverse: %f" % sorted_deviations[0])
print("Most diverse: %f" % sorted_deviations[-1])
chosen_one = dict(("class",all_possible[key]) for key, value in class_summaries.iteritems() if value["std_average"] == sorted_deviations[-1])
print("This is the best class for you: %s" % str(chosen_one))
