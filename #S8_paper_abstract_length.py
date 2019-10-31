### This file downloads paper extracts from PubMed API


import pandas as pd
import re
import metapub
import numpy as np
import scipy
from NLP_pipeline import nlp_pipeline


publication = pd.read_csv('paper_analysis_new1.csv')

round_number = (len(publication.index) // 80000) + 1
remainder = (len(publication.index) % 80000) - 1
print("Loop begins. There will be " + str(round_number) + " loops and " +
      str(len(publication.index)) + " projects.")

for l in range(0, round_number):
    # Determine the beginning positon and ending position for each loop
    publication = pd.read_csv('paper_analysis_new1.csv')
    start_position = 1 + (l * 80000)
    if l == round_number - 1:
        end_position = start_position + remainder
    else:
        end_position = start_position + 80000
    print("Round " + str(l) + ": from papers #" + str(start_position) + " to #" + str(end_position))

    for i in range(start_position, end_position):
        pmid = publication.loc[i, "PMID"]
        file = open("abstract/" + str(pmid) + ".txt", 'r')
        abstract_text = file.read()
        publication.loc[i, "abstract_length"] = len(abstract_text.split())


    publication.to_csv("paper_analysis_new1.csv", index_label=False, index=False)



