#!/usr/bin/python
import random
import itertools
import scipy.misc
import numpy
import math

############################################
############################################
############################################
############################################

extract_scores = lambda y:y.score

class student:
    def __init__(self,score):
        self.score = score
    def __str__(self):
        return "%d" % self.score
    def __repr__(self):
        return self.__str__()

history_record = { "1": { "2": 2, "3": 3}}

def history_score_group(group):
    total_recurrences = 0
    for i in range(0, len(group)):
            for j in range(i+1,len(group)):
                total_recurrences += group[i].proximity(group[j])
    return total_recurrences

def test_score_group(group):
    return numpy.std(map(extract_scores,group))

def generate_sample_class(student_list,group_count):
    # Build a structure to track the class groups
    sample_class = []
    for time in range(0,group_count): sample_class.append([])

    # Build a new randomized list for consideration
    wastable_list = student_list[:]
    random.shuffle(wastable_list)
    # Add the students to the sample class groups
    for index in range(0,len(student_list)):
        sample_class[index % group_count].append(wastable_list[index])
    return sample_class

def generate_sample_classes(student_list,students_per_group, number_of_samples_desired):
    number_of_groups = int(math.ceil(len(student_list)/float(students_per_group)))
    sample_classes = []
    for i in range(0,number_of_samples_desired):
        sample_classes.append(generate_sample_class(student_list,number_of_groups))
    return sample_classes

############################################
############################################
############################################
############################################

TOTAL_CLASS_SIZE = 75
STUDENTS_PER_GROUP = 6
SAMPLE_SIZE = 10000

## Fake some student data
master_class_list = []
for i in range(0,TOTAL_CLASS_SIZE):
    master_class_list.append(student(random.randint(0,100)))

print("Generating list of total class combinations")
sample_classes = generate_sample_classes(master_class_list,STUDENTS_PER_GROUP,SAMPLE_SIZE)

print("There were a total of %d possibilities given a class size of %d and group size around %d" % (len(sample_classes), len(master_class_list), STUDENTS_PER_GROUP))

print("Calculating class scores")
class_summaries = {}
for class_index in range(0,len(sample_classes)):
    class_possibility = sample_classes[class_index]
    total_of_std = 0
    for group in class_possibility:
        total_of_std += test_score_group(group)
    std_average = total_of_std / float(len(class_possibility))
    class_summaries[class_index] = { "std_average": std_average}

sorted_deviations = sorted(map(lambda k: class_summaries[k]['std_average'], class_summaries))
print("Least diverse: %f" % sorted_deviations[0])
print("Most diverse: %f" % sorted_deviations[-1])
chosen_one = dict(("class",sample_classes[key]) for key, value in class_summaries.iteritems() if value["std_average"] == sorted_deviations[-1])
print("This is the best class for you: %s" % str(chosen_one))
