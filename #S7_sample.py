import pandas as pd

project = pd.read_csv("project.csv")
abstract = pd.read_csv("abstract.csv")

project_sample = pd.read_csv("proj_sample.csv")
paper_sample = pd.read_csv("paper_sample.csv")

project_sample_summary = pd.DataFrame()
paper_sample_summary = pd.DataFrame()

id_list = list(set(project_sample['id']))

for i in range(len(id_list)):
    id = id_list[i]
    app = project.loc[project['CORE_PROJECT_NUM'] == id, 'APPLICATION_ID'].item()
    title = project.loc[project['CORE_PROJECT_NUM'] == id, 'PROJECT_TITLE'].item()
    abstract_txt = abstract.loc[abstract['APPLICATION_ID'] == app, 'ABSTRACT_TEXT'].item()
    project_sample_summary = project_sample_summary.append({
        "id":id, 'title':title, 'abstract':abstract_txt
    }, ignore_index=True)

project_sample_summary.to_csv("project_sample_summary.csv", index = False)
