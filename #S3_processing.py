### This file downloads paper extracts from PubMed API


import pandas as pd
import re
import metapub
import numpy as np
import scipy
from NLP_pipeline import nlp_pipeline

fetch = metapub.PubMedFetcher()

publication = pd.read_csv('PAPER_SUM.csv')
publication_list = list(set(publication['PMID']))
print('Step 1: There are ' + str(len(publication_list)) + ' unique papers to be checked.')

# round_number = (len(publication_list) // 100) + 1
# remainder = (len(publication_list) % 100) - 1
# print("Loop begins. There will be " + str(round_number) + " loops and " +
#       str(len(publication_list)) + " projects.")
#
# for l in range(4349, round_number):
#     # Determine the beginning positon and ending position for each loop
#     publication = pd.read_csv('PAPER_SUM.csv')
#     start_position = 1 + (l * 100)
#     if l == round_number - 1:
#         end_position = start_position + remainder
#     else:
#         end_position = start_position + 100
#     print("Round " + str(l) + ": from papers #" + str(start_position) + " to #" + str(end_position))
#
#     for i in range(start_position, end_position):
#         pmid = publication_list[i]
#         if len(fetch._eutils_pmids_for_query(str(pmid))) == 1:
#             abstract_text = fetch.article_by_pmid(str(pmid)).abstract
#
#             if abstract_text != None:
#                 publication.loc[publication['PMID'] == pmid, 'match'] = "T"
#                 file = open("abstract/" + str(pmid) + ".txt", "w")
#                 file.write(abstract_text)
#                 file.close()
#                 print("Write " + str(pmid) + " to file. (" + str(i) + " / " + str(len(publication_list)) + ")")
#             else:
#                 publication.loc[publication['PMID'] == pmid, 'match'] = "F"
#                 print(str(pmid) + " does not have abstract.")
#
#         else:
#             publication.loc[publication['PMID'] == pmid, 'match'] = "F"
#             print(str(pmid) + " does not have abstract.")
#
#     publication.to_csv("PAPER_SUM.csv", index_label=False, index=False)


publication = publication.loc[publication['match'] == "T"]
# 656,931 out of 686,660 papers wee retained from the last step.
publication.to_csv("PAPER_SUM_NEW.csv", index_label=False, index=False)

round_number = (len(publication.index) // 500) + 1
remainder = (len(publication.index) % 500) - 1
print("Loop begins. There will be " + str(round_number) + " loops and " +
      str(len(publication.index)) + " papers.")

#  round_number
for l in range(0, round_number):
    # Determine the beginning positon and ending position for each loop
    publication = pd.read_csv('PAPER_SUM_NEW.csv')
    start_position = 1 + (l * 500)
    if l == round_number - 1:
        end_position = start_position + remainder
    else:
        end_position = start_position + 500
    print("Round " + str(l) + ": from papers #" + str(start_position) + " to #" + str(end_position))

    for i in range(start_position, end_position):
        pmid = publication.loc[i, 'PMID']
        file = open("abstract/" + str(pmid) + ".txt", 'r')
        abstract_text = file.read()
        text_table = nlp_pipeline(str(abstract_text))
        if len(text_table) > 0:
            publication.loc[i, 'TERM'] = ";".join(text_table)
            publication.loc[i, 'TERM_LENGTH'] = len(text_table)
        else:
            publication.loc[i, 'TERM'] = ""
            publication.loc[i, 'TERM_LENGTH'] = 0

    publication.to_csv("PAPER_SUM_NEW.csv", index_label=False, index=False)
