#  Copyright (c)  OpsMx, Purushotham Koduri
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import logging
import pathlib

date = '9th-15thDec'
Bugs = overview = efforts = stale = epic = tasks = sub_task = stories = test_cases = titles = pd.DataFrame()

try:
    Bugs = pd.read_csv(rf'{date}\Jira\Bug_list.csv')
    overview = pd.read_csv(rf'{date}/Jira/issue_type_state_counter_report.csv')
    efforts = pd.read_csv(rf'{date}\Jira\worklog_report.csv')
    stale = pd.read_csv(rf'{date}\Jira\StaleIssuesInSprint.csv')
    epic = pd.read_csv(rf'{date}\Jira\Epic_list.csv')
    tasks = pd.read_csv(rf'{date}\Jira\Task_list.csv')
    sub_task = pd.read_csv(rf'{date}\Jira\SubTask_list.csv')
    stories = pd.read_csv(rf'{date}\Jira\Story_list.csv')
    test_cases = pd.read_csv(rf'{date}\Jira\TestCase_list.csv')
    titles = pd.read_csv(rf'{date}\Jira\IssueSummary.csv',
                         usecols=[0, 1])

except FileNotFoundError:
    logging.warning("Files are missing")
pd.options.mode.chained_assignment = None
pathlib.Path('Jira Plots').mkdir(parents=True, exist_ok=True)




def stacked_graph(df, colors, title):
    projects = df.iloc[:, 0]
    indx = np.arange(len(df))
    font_color = '#525252'
    csfont = {'fontname': 'Georgia'}
    hfont = {'fontname': 'Calibri'}
    ax = df.plot.barh(align='center', stacked=True, figsize=(20, 10), color=colors, width=0.35)
    plt.tight_layout()
    plt.subplots_adjust(top=0.8, left=0.26)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(15)
    plt.xticks(color=font_color, **hfont)
    plt.yticks(indx, projects, color=font_color, **hfont)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.ylabel('Issue types', fontsize=18)
    plt.xlabel('Number of issues', fontsize=18)
    plt.legend(prop={'size': 19}, bbox_to_anchor=(1.1, 1.05))

    #     for p in ax.patches:
    #         width, height = p.get_width(), p.get_height()
    #         x, y = p.get_xy()
    #         ax.text(x+width/2,
    #                 y+height/2,
    #                 '{:.0f}'.format(width),
    #                 horizontalalignment='center',
    #                 verticalalignment='center',
    #                 color='white',
    #                 fontsize=10,
    #                 **hfont)
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='bottom', bbox=[0, -0.8, 1, 0.6])
    table.set_fontsize(18)
    ax.set_title(title, pad=60, fontsize=38, color=font_color, **csfont)


def pie_chart(series, names, colors):
    plt.figure(1, figsize=(10, 10))
    porcent = 100. * series / series.sum()

    patches, texts = plt.pie(series, colors=colors, startangle=90, radius=1.2)
    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(names, porcent)]

    sort_legend = True
    if sort_legend:
        patches, labels, dummy = zip(*sorted(zip(patches, labels, series),
                                             key=lambda x: x[2],
                                             reverse=True))

    plt.legend(patches, labels, loc='right', bbox_to_anchor=(-0.1, 1.),
               fontsize=19)


def simple_bar_chart(series, labels, title, ylabel, xlabel):
    font_color = '#525252'
    csfont = {'fontname': 'Georgia'}
    fig, ax = plt.subplots(figsize=(20, 10))
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['text.color'] = 'black'
    plt.rcParams['font.size'] = 18
    ind = np.arange(len(series))
    bars1 = ax.bar(labels, series,
                   color="steelblue")
    ax.bar_label(ax.containers[0])
    ax.set_title(title, pad=60, fontsize=18, color=font_color, **csfont)

    ax.set_xticks(range(0, len(ind)))
    ax.set_xticklabels(list(labels), rotation=70)
    ax.set_xlabel(xlabel, fontsize=18)
    ax.set_ylabel(ylabel, fontsize=18)
    ax.tick_params(axis='x', colors='black')
    ax.yaxis.label.set_color('black')
    ax.xaxis.label.set_color('black')
    ax.tick_params(axis='y', colors='black')
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.set_title(title, pad=60, fontsize=38)


def progress_chart(edf):
    cmap = plt.get_cmap('autumn')
    colors = [cmap(i) for i in np.linspace(0.1, 1.3, 5)]
    fig, axes = plt.subplots(3, 3, figsize=(30, 30))
    for i, (idx, row) in enumerate(edf.set_index('IssueType').iterrows()):
        ax = axes[i // 3, i % 3]
        row = row[row.gt(row.sum() * .01)]
        ax.pie(row, labels=row.index, normalize=True, colors=['steelblue', '#239B56'], startangle=30, autopct='%1.0f%%',
               textprops={'fontsize': 20}, wedgeprops=dict(width=0.5))
        ax.set_title(idx, fontsize=25)

    axes[2, 2].set_axis_off()
    axes[2, 1].set_axis_off()


df = overview
df['Complete'] = df['Done'] + df['InVerification']
df['Pending'] = df['ToDo'] + df['InProgress'] + df['PRRaised'] + df['Merged']
df = df[['IssueType', 'Pending', 'Complete']]
progress_chart(df)
plt.close()
plt.savefig('Jira Plots\ Overview.png', format='png', dpi=300)
efforts = efforts.sort_values(by=['TimeSpentInSeconds'], ascending=False)
stale = stale.sort_values(by=['HoursSinceLastUpdate'], ascending=False)
df4 = epic[epic['OriginalTimeEstimate'] != 'None']
df4.OriginalTimeEstimate = df4.OriginalTimeEstimate.astype(int)
df4.AggregateTimeSpent = df4.AggregateTimeSpent.astype(int)
epic_estimate = df4[df4['OriginalTimeEstimate'] < df4['AggregateTimeSpent']]
df3 = tasks[tasks['OriginalTimeEstimate'] != 'None']
df3.OriginalTimeEstimate = df3.OriginalTimeEstimate.astype(int)
df3.AggregateTimeSpent = df3.AggregateTimeSpent.astype(int)
task_estimate = df3[df3['OriginalTimeEstimate'] < df3['AggregateTimeSpent']]
df5 = sub_task[sub_task['OriginalTimeEstimate'] != 'None']
df5.OriginalTimeEstimate = df5.OriginalTimeEstimate.astype(int)
df5.AggregateTimeSpent = df5.AggregateTimeSpent.astype(int)
subtask_estimate = df5[df5['OriginalTimeEstimate'] < df5['AggregateTimeSpent']]
df6 = stories[stories['OriginalTimeEstimate'] != 'None']
df6.OriginalTimeEstimate = df6.OriginalTimeEstimate.astype(int)
df6.AggregateTimeSpent = df6.AggregateTimeSpent.astype(int)
story_estimate = df6[df6['OriginalTimeEstimate'] < df6['AggregateTimeSpent']]
df7 = Bugs[Bugs['OriginalTimeEstimate'] != 'None']
df7.OriginalTimeEstimate = df7.OriginalTimeEstimate.astype(int)
df7.AggregateTimeSpent = df7.AggregateTimeSpent.astype(int)
bug_estimate = df7[df7['OriginalTimeEstimate'] < df7['AggregateTimeSpent']]
df8 = test_cases.loc[Bugs['OriginalTimeEstimate'] != 'None']
df8.OriginalTimeEstimate = df7.OriginalTimeEstimate.astype(int)
df8.AggregateTimeSpent = df8.AggregateTimeSpent.astype(int)
test_estimate = df8[df8['OriginalTimeEstimate'] < df8['AggregateTimeSpent']]
simple_bar_chart(overview.iloc[1:]['TotalCount'], overview.iloc[1:].IssueType, f"Overview of issue types",
                 "Number of issues", "Issue types")
plt.savefig('Jira Plots\ issues_Overview.png', format='png', dpi=300)
plt.close()
simple_bar_chart(efforts[0:10]['TimeSpentInSeconds'] // 3600, efforts[0:10].Assignee, f"Top Performers of the Week",
                 "Total hours spent", "Assignee")
plt.savefig('Jira Plots\ Top performers.png', format='png', dpi=300)
df = pd.merge(stale, titles, on='IssueKey', how='outer')
df.dropna(inplace=True)
simple_bar_chart(stale[0:10]['HoursSinceLastUpdate'] // 24, stale[0:10].IssueKey, f"Top 10 Stale issues",
                 "Days since last updated", "Issue Key")
if len(df) > 0:
    table = plt.table(cellText=df[['IssueKey', 'Status', 'Priority', 'Assignee', 'Summary']].values,
                      colLabels=df[['IssueKey', 'Status', 'Priority', 'Assignee', 'Summary']].columns, loc='bottom',
                      bbox=[0, -0.95, 1, 0.6])
    table.set_fontsize(28)
plt.savefig('Jira Plots\ stale issues.png', format='png')
overview = pd.read_csv(rf'{date}/Jira/issue_type_state_counter_report.csv')
cmap = plt.get_cmap('Blues')
colors = [cmap(i) for i in np.linspace(0.2, 1.3, 9)]
my_df = overview.drop("TotalCount", axis=1)
stacked_graph(my_df[1:], colors, "Current status of issues")
plt.savefig('Jira Plots\ current status.png', format='png', dpi=300, bbox_inches='tight')
df1 = epic.sort_values(by=['AggregateTotalTime'], ascending=False)
simple_bar_chart(df1[0:10]['AggregateTotalTime'] // 3600, df1[0:10].IssueKey, f"Top 10 high effort Epics",
                 "Hours spent", "Epic Keys")
plt.savefig('Jira Plots\ epic higheffort.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
cmap = plt.get_cmap('Blues')
colors = [cmap(0.6),
          cmap(1.0),
          cmap(0.4),
          cmap(0.2),
          '#C3A316']
pie_chart(epic.groupby('Priority').count()['IssueType'], epic.groupby('Priority').count().index, colors)
plt.savefig('Jira Plots\ epic priority.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
mylabels = ['Time Spent', 'Total Estimated']
epic_estimate['OriginalTimeEstimate'] = epic_estimate['OriginalTimeEstimate'].astype(int) / 3600
epic_estimate['AggregateTimeSpent'] = epic_estimate['AggregateTimeSpent'].astype(int) / 3600
epic_estimate.plot(x="IssueKey", y=["AggregateTimeSpent", "OriginalTimeEstimate"], figsize=(50, 15), grid=True,
                   color=["darkgreen", "red"])
plt.suptitle('Efforts spent on Epics', fontsize=40)
plt.ylabel("Time in hours", fontsize=50)
plt.xlabel("Epic Keys", fontsize=50)
plt.legend(labels=mylabels, prop={'size': 50})
df = pd.merge(epic_estimate[['IssueKey', 'Status', 'Priority', 'Assignee']], titles, on='IssueKey', how='outer')
df.dropna(inplace=True)
if len(df) > 0:
    table = plt.table(cellText=df[['IssueKey', 'Status', 'Priority', 'Assignee']].values,
                      colLabels=df[['IssueKey', 'Status', 'Priority', 'Assignee']].columns, loc='bottom',
                      bbox=[0, -0.95, 1, 0.8])
    table.auto_set_font_size(False)
    table.set_fontsize(28)
plt.savefig('Jira Plots\ underestimated_epics.png', format='png', bbox_inches='tight')
df2 = tasks.sort_values(by=['AggregateTotalTime'], ascending=False)
simple_bar_chart(df2[0:10]['AggregateTotalTime'] // 3600, df2[0:10].IssueKey, f"Top 10 high effort Tasks",
                 "Hours spent", "Task Keys")
plt.savefig('Jira Plots\ tasks_highefforts.png', format='png', dpi=300, bbox_inches='tight')
cmap = plt.get_cmap('Blues')
colors = [cmap(0.6),
          cmap(1.0),
          cmap(0.4),
          cmap(0.2),
          '#C3A316']
pie_chart(tasks.groupby('Priority').count()['IssueType'], tasks.groupby('Priority').count().index, colors)
plt.savefig('Jira Plots\ tasks_priority.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
cmap = plt.get_cmap('Blues')
colors = [cmap(1.0),
          cmap(0.4),
          cmap(0.6),
          cmap(0.2),
          '#C3A316']
pie_chart(tasks.groupby('Status').count()['IssueType'], tasks.groupby('Status').count().index, colors)
plt.savefig('Jira Plots\ tasks_status.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
mylabels = ['Time Spent', 'Total Estimated']
task_estimate['OriginalTimeEstimate'] = task_estimate['OriginalTimeEstimate'].astype(int) / 3600
task_estimate['AggregateTimeSpent'] = task_estimate['AggregateTimeSpent'].astype(int) / 3600
task_estimate.plot(x="IssueKey", y=["AggregateTimeSpent", "OriginalTimeEstimate"], figsize=(50, 15), grid=True,
                   color=["darkgreen", "red"])
plt.suptitle('Efforts spent on Tasks', fontsize=40)
plt.ylabel("Time in hours", fontsize=50)
plt.xlabel("Task Keys", fontsize=50)
plt.legend(labels=mylabels, prop={'size': 50})
df = pd.merge(task_estimate, titles, on='IssueKey', how='outer')
df.dropna(inplace=True)
if len(df) > 0:
    table = plt.table(cellText=df[['IssueKey', 'Status', 'Priority', 'Assignee']].values,
                      colLabels=df[['IssueKey', 'Status', 'Priority', 'Assignee']].columns, loc='bottom',
                      bbox=[0, -0.95, 1, 0.8])
    table.auto_set_font_size(False)
    table.set_fontsize(28)
plt.savefig('Jira Plots\ underestimated_tasks.png', format='png', bbox_inches='tight')
my_subtask = sub_task.sort_values(by=['AggregateTotalTime'], ascending=False)
simple_bar_chart(my_subtask[0:10]['AggregateTotalTime'] // 3600, my_subtask[0:10].IssueKey,
                 f"Top 10 high effort Sub-tasks", "Hours spent", "Sub Task Keys")
plt.savefig('Jira Plots\ subtasks_higheffort.png', format='png', dpi=300, bbox_inches='tight')
cmap = plt.get_cmap('Blues')
colors = [cmap(0.75),
          cmap(1.0),
          cmap(0.2),
          cmap(0.4),
          '#C3A316']
pie_chart(sub_task.groupby('Priority').count()['IssueType'], sub_task.groupby('Priority').count().index, colors)
plt.savefig('Jira Plots\ subtask_priority.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
cmap = plt.get_cmap('Blues')
colors = [cmap(1.0),
          cmap(0.4),
          cmap(0.6),
          cmap(0.2),
          "#C3A316",
          'grey']
pie_chart(sub_task.groupby('Status').count()['IssueType'], sub_task.groupby('Status').count().index, colors)
plt.savefig('Jira Plots\ subtask_status.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
mylabels = ['Time Spent', 'Total Estimated']
subtask_estimate['OriginalTimeEstimate'] = subtask_estimate['OriginalTimeEstimate'].astype(int) / 3600
subtask_estimate['AggregateTimeSpent'] = subtask_estimate['AggregateTimeSpent'].astype(int) / 3600
subtask_estimate.plot(x="IssueKey", y=["AggregateTimeSpent", "OriginalTimeEstimate"], figsize=(50, 15), grid=True,
                      color=["darkgreen", "red"])
plt.suptitle('Efforts spent on subtasks', fontsize=40)
plt.ylabel("Time in hours", fontsize=50)
plt.xlabel("subtask Keys", fontsize=50)
plt.legend(labels=mylabels, prop={'size': 50})
df = pd.merge(subtask_estimate[['IssueKey', 'Status', 'Priority', 'Assignee']], titles, on='IssueKey', how='outer')
df.dropna(inplace=True)
if len(df) > 0:
    table = plt.table(cellText=df[['IssueKey', 'Status', 'Priority', 'Assignee', 'Summary']].values,
                      colLabels=df[['IssueKey', 'Status', 'Priority', 'Assignee', 'Summary']].columns, loc='bottom',
                      bbox=[0, -0.95, 1, 0.8])
    table.set_fontsize(18)
plt.savefig('Jira Plots\ understimated_subtasks.png', format='png', dpi=300, bbox_inches='tight')
my_story = stories.sort_values(by=['AggregateTotalTime'], ascending=False)
simple_bar_chart(my_story[0:10]['AggregateTotalTime'] // 3600, my_story[0:10].IssueKey, f"Top 10 high effort Stories",
                 "Hours spent", "story Keys")
plt.savefig('Jira Plots\ story_higheffort.png', format='png', dpi=300, bbox_inches='tight')
cmap = plt.get_cmap('Blues')
colors = [cmap(0.75),
          cmap(1.0),
          cmap(0.2),
          cmap(0.4),
          '#C3A316']
pie_chart(stories.groupby('Priority').count()['IssueType'], stories.groupby('Priority').count().index, colors)
plt.savefig('Jira Plots\ story_priority.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
cmap = plt.get_cmap('Blues')
colors = [cmap(1.0),
          cmap(0.4),
          cmap(0.6),
          cmap(0.2),
          "#C3A316",
          'grey']
pie_chart(stories.groupby('Status').count()['IssueType'], stories.groupby('Status').count().index, colors)
plt.savefig('Jira Plots\ story_status.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
mylabels = ['Time Spent', 'Total Estimated']
story_estimate['OriginalTimeEstimate'] = story_estimate['OriginalTimeEstimate'].astype(int) / 3600
story_estimate['AggregateTimeSpent'] = story_estimate['AggregateTimeSpent'].astype(int) / 3600
story_estimate.plot(x="IssueKey", y=["AggregateTimeSpent", "OriginalTimeEstimate"], figsize=(50, 15), grid=True,
                    color=["darkgreen", "red"])
plt.suptitle('Efforts spent on stories', fontsize=40)
plt.ylabel("Time in hours", fontsize=50)
plt.xlabel("Story Keys", fontsize=50)
plt.legend(labels=mylabels, prop={'size': 50})
df = pd.merge(story_estimate[['IssueKey', 'Status', 'Priority', 'Assignee']], titles, on='IssueKey', how='outer')
df.dropna(inplace=True)
if len(df) > 0:
    table = plt.table(cellText=df[['IssueKey', 'Status', 'Priority', 'Assignee']].values,
                      colLabels=df[['IssueKey', 'Status', 'Priority', 'Assignee']].columns, loc='bottom',
                      bbox=[0, -0.95, 1, 0.8])
    table.auto_set_font_size(False)
    table.set_fontsize(28)
plt.savefig('Jira Plots\ underestimated_Story.png', format='png', bbox_inches='tight')
my_bugs = Bugs.sort_values(by=['AggregateTotalTime'], ascending=False)
simple_bar_chart(my_bugs[0:10]['AggregateTotalTime'] // 3600, my_bugs[0:10].IssueKey, f"Top 10 high effort Bugs",
                 "Hours spent", "Bug Keys")
plt.savefig('Jira Plots\ bugs_higheffort.png', format='png', dpi=300, bbox_inches='tight')

cmap = plt.get_cmap('Blues')
colors = [cmap(0.75),
          cmap(1.0),
          cmap(0.2),
          cmap(0.4),
          '#C3A316']
pie_chart(Bugs.groupby('Priority').count()['IssueType'], Bugs.groupby('Priority').count().index, colors)
plt.savefig('Jira Plots\ bugs_priority.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
cmap = plt.get_cmap('Blues')
colors = [cmap(1.0),
          cmap(0.4),
          cmap(0.6),
          cmap(0.2),
          "#C3A316",
          'grey']
pie_chart(Bugs.groupby('Status').count()['IssueType'], Bugs.groupby('Status').count().index, colors)
plt.savefig('Jira Plots\ bugs_status.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
mylabels = ['Time Spent', 'Total Estimated']
bug_estimate['OriginalTimeEstimate'] = bug_estimate['OriginalTimeEstimate'].astype(int) / 3600
bug_estimate['AggregateTimeSpent'] = bug_estimate['AggregateTimeSpent'].astype(int) / 3600
bug_estimate.plot(x="IssueKey", y=["AggregateTimeSpent", "OriginalTimeEstimate"], figsize=(50, 15), grid=True,
                  color=["darkgreen", "red"])
plt.suptitle('Efforts spent on Bugs', fontsize=40)
plt.ylabel("Time in hours", fontsize=50)
plt.xlabel("Bug Keys", fontsize=50)
plt.legend(labels=mylabels, prop={'size': 50})
df = pd.merge(bug_estimate[['IssueKey', 'Status', 'Priority', 'Assignee']], titles, on='IssueKey', how='outer')
df.dropna(inplace=True)
if len(df) > 0:
    table = plt.table(cellText=df[['IssueKey', 'Status', 'Priority', 'Assignee']].values,
                      colLabels=df[['IssueKey', 'Status', 'Priority', 'Assignee']].columns, loc='bottom',
                      bbox=[0, -0.95, 1, 0.8])
    table.auto_set_font_size(False)
    table.set_fontsize(28)
plt.savefig('Jira Plots\ underestimated_bugs.png', format='png', bbox_inches='tight')
plt.close()
my_tests = test_cases.sort_values(by=['AggregateTotalTime'], ascending=False)
simple_bar_chart(my_tests[0:10]['AggregateTotalTime'] // 3600, my_tests[0:10].IssueKey, f"Top 10 high effort Testcases",
                 "Hours spent", "test case Keys")
plt.savefig('Jira Plots\ testcases_higheffort.png', format='png', dpi=300, bbox_inches='tight')

cmap = plt.get_cmap('Blues')
colors = [cmap(0.75),
          cmap(1.0),
          cmap(0.2),
          cmap(0.4),
          '#C3A316']
pie_chart(test_cases.groupby('Priority').count()['IssueType'], test_cases.groupby('Priority').count().index, colors)
plt.savefig('Jira Plots\ testcase_priority.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
cmap = plt.get_cmap('Blues')
colors = [cmap(1.0),
          cmap(0.4),
          cmap(0.6),
          cmap(0.2),
          "#C3A316",
          'grey']
pie_chart(test_cases.groupby('Status').count()['IssueType'], test_cases.groupby('Status').count().index, colors)
plt.savefig('Jira Plots\ testcase_status.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
mylabels = ['Time Spent', 'Total Estimated']
test_estimate['OriginalTimeEstimate'] = test_estimate['OriginalTimeEstimate'].astype(int) / 3600
test_estimate['AggregateTimeSpent'] = test_estimate['AggregateTimeSpent'].astype(int) / 3600
test_estimate.plot(x="IssueKey", y=["AggregateTimeSpent", "OriginalTimeEstimate"], figsize=(50, 15), grid=True,
                   color=["darkgreen", "red"])
plt.suptitle('Efforts spent on Testcases', fontsize=40)
plt.ylabel("Time in hours", fontsize=50)
plt.xlabel("Testcase Keys", fontsize=50)
plt.legend(labels=mylabels, prop={'size': 50})
df = pd.merge(test_estimate[['IssueKey', 'Status', 'Priority', 'Assignee']], titles, on='IssueKey', how='outer')
df.dropna(inplace=True)
if len(df) > 0:
    table = plt.table(cellText=df[['IssueKey', 'Status', 'Priority', 'Assignee']].values,
                      colLabels=df[['IssueKey', 'Status', 'Priority', 'Assignee']].columns, loc='bottom',
                      bbox=[0, -0.95, 1, 0.8])
    table.auto_set_font_size(False)
    table.set_fontsize(28)
plt.savefig('Jira Plots\ underestimated_testcase.png', format='png', dpi=300, bbox_inches='tight')
plt.close()
