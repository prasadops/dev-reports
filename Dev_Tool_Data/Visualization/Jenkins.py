#  Copyright (c)  OpsMx, Purushotham Koduri

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import logging

date = '9th-15thDec'
jobs = builds=aona=gitpr=night=pd.DataFrame()

try:
    jobs = pd.read_csv(rf'{date}/Jenkins/job_status_report.csv')
    builds = pd.read_csv(rf'{date}/Jenkins/build_list.csv')
    aona = pd.read_csv(rf'{date}/Jenkins/aona_status_report.csv')
    gitpr = pd.read_csv(rf'{date}/Jenkins/gitpr_status_report.csv')
    night = pd.read_csv(rf'{date}/Jenkins/nightly_status_report.csv')
except FileNotFoundError:
    logging.warning("Files are missing")

pathlib.Path('Jenkins Plots').mkdir(parents=True, exist_ok=True)


def stacked_graph(df, colors, title):
    projects = df.iloc[:, 0]
    indx = np.arange(len(df))
    font_color = '#525252'
    csfont = {'fontname': 'Georgia'}
    hfont = {'fontname': 'Calibri'}
    ax = df.plot.bar(align='center', stacked=True, figsize=(20, 10), color=colors, width=0.35)
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
    plt.show()


def simple_bar_chart(series, labels, title, ylabel, xlabel):
    font_color = '#525252'
    csfont = {'fontname': 'Georgia'}
    fig, ax = plt.subplots(figsize=(30, 20))
    fig.autofmt_xdate()
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['text.color'] = 'black'
    plt.rcParams['font.size'] = 38
    ind = np.arange(len(series))
    bars1 = ax.bar(labels, series,
                   color="steelblue")
    ax.bar_label(ax.containers[0])
    ax.set_title(title, pad=60, fontsize=48, color=font_color, **csfont)

    ax.set_xticks(range(0, len(ind)))
    ax.set_xticklabels(list(labels), rotation=90)
    ax.set_xlabel(xlabel, fontsize=38)
    ax.set_ylabel(ylabel, fontsize=38)
    ax.tick_params(axis='x', colors='black')
    ax.yaxis.label.set_color('black')
    ax.xaxis.label.set_color('black')
    ax.tick_params(axis='y', colors='black')
    ax.tick_params(axis='both', which='major', labelsize=28)
    ax.set_title(title, pad=60, fontsize=38)


def progress_chart(df):
    cmap = plt.get_cmap('autumn')
    colors = [cmap(i) for i in np.linspace(0.1, 1.3, 5)]
    fig, axes = plt.subplots(3, 3, figsize=(30, 30))
    for i, (idx, row) in enumerate(df.set_index('IssueType').iterrows()):
        ax = axes[i // 3, i % 3]
        row = row[row.gt(row.sum() * .01)]
        ax.pie(row, labels=row.index, normalize=True, colors=['steelblue', '#239B56'], startangle=30, autopct='%1.0f%%',
               textprops={'fontsize': 20}, wedgeprops=dict(width=0.5))
        ax.set_title(idx, fontsize=25)

    axes[2, 2].set_axis_off()
    axes[2, 1].set_axis_off()
    plt.show()


def subcategorybar(df, title):
    colors = ['#239B56', 'red', '#F1C40F']
    font_color = '#525252'
    ax = df.plot(kind='bar', x="JobName", figsize=(35, 30), width=0.6, color=colors, grid=True)

    ax.set_xticklabels(list(df.JobName), rotation=90, fontsize=28)
    csfont = {'fontname': 'Georgia'}
    hfont = {'fontname': 'Calibri'}
    plt.ylabel('Number of Builds', fontsize=45)
    plt.xlabel('Job Names', fontsize=45)
    ax.tick_params(axis='x', colors='black')
    ax.yaxis.label.set_color('black')
    ax.xaxis.label.set_color('black')
    ax.tick_params(axis='y', colors='black', labelsize=18)
    ax.bar_label(ax.containers[0], size=28)
    ax.bar_label(ax.containers[1], size=28)
    ax.bar_label(ax.containers[2], size=28)
    # tables = plt.table(cellText=df.values, colLabels=df.columns, loc='bottom', bbox=[0, -1.2, 1, 0.6])
    # tables.set_fontsize(18)
    # ax.set_title(title, pad=60, fontsize=38, color=font_color, **csfont)
    ax.legend(prop={'size': 19}, bbox_to_anchor=(1.1, 1.05))



simple_bar_chart(builds.groupby('JobName').count()['BuildId'], builds.groupby('JobName').count().index,
                 "Builds per job", "Number of builds", "Job names")
plt.savefig('Jenkins Plots\ builds_per_job.png', format='png',bbox_inches='tight')

df = builds
df.BuildEstimateDuration = df.BuildEstimateDuration.astype(int)
df.BuildDuration = df.BuildDuration.astype(int)
build_estimate = df[df['BuildDuration'] > df['BuildEstimateDuration']]
relevant_jobs = jobs[jobs['NumberOfBuilds'] > 0]
relevant_jobs = relevant_jobs.sort_values(by=['Failed'], ascending=False)
jobs = jobs[jobs['NumberOfBuilds'] > 0]
jobs = jobs[jobs['Failed'] > 0]
subcategorybar(jobs[['JobName', 'Successful', 'Failed', 'Aborted']], "Jobs with failed or aborted builds")
plt.savefig('Jenkins Plots\ Jobs with failed or aborted.png', format='png', bbox_inches='tight')
jobs = aona[aona['NumberOfBuilds'] > 0]
jobs = jobs[['JobName', 'Successful', 'Failure', 'Aborted']]
jobs = jobs[jobs.index != "Total"]
subcategorybar(jobs[['JobName', 'Successful', 'Failure', 'Aborted']], "AonA Jobs")
plt.savefig('Jenkins Plots\ AonA Jobs.png', format='png', bbox_inches='tight')
jobs = night[night['NumberOfBuilds']>0]
jobs=jobs[jobs.index != "Total"]
subcategorybar(jobs[['JobName','Successful','Failure','Aborted']],"Nightly jobs")
plt.savefig('Jenkins Plots\ nightly.png', format='png', bbox_inches='tight')
jobs = gitpr[gitpr['NumberOfBuilds']>0]
jobs=jobs[jobs.index != "Total"]
subcategorybar(jobs[['JobName','Successful','Failure','Aborted']],"Git-PR jobs")

plt.savefig('Jenkins Plots\ gitpr.png', format='png',bbox_inches='tight')
simple_bar_chart(relevant_jobs[0:10]['Failed'],relevant_jobs[0:10].JobName,f"Jobs with most build failures","Number of builds","Job names")
plt.ylim([0, 15])
plt.savefig('Jenkins Plots\ most_buildfails.png', format='png',bbox_inches='tight')
relevant_jobs=relevant_jobs.sort_values(by=['NumberOfBuilds'], ascending=False)
simple_bar_chart(relevant_jobs[0:10]['NumberOfBuilds'],relevant_jobs[0:10].JobName,f"Jobs with most builds","Number of builds","Job names")
plt.savefig('Jenkins Plots\ most_builds.png', format='png',bbox_inches='tight')
relevant_jobs=relevant_jobs.sort_values(by=['Aborted'], ascending=False)
simple_bar_chart(relevant_jobs[0:10]['Aborted'],relevant_jobs[0:10].JobName,f"Jobs with most builds aborted","Number of builds","Job names")
plt.ylim([0, 10])
plt.savefig('Jenkins Plots\ most_builds_aborted.png', format='png',bbox_inches='tight')
relevant_builds=builds.sort_values(by=['BuildDuration'], ascending=False)
simple_bar_chart(relevant_builds[0:10]['BuildDuration']//60000,relevant_builds[0:10].BuildName,f"Top 10 Builds that took most time","builds duration in minutes","Build names")
plt.savefig('Jenkins Plots\ most_duration.png', format='png',bbox_inches='tight')
mylabels = ['Build duration','Time Estimated']
pd.options.mode.chained_assignment = None
build_estimate['BuildDuration']= build_estimate['BuildDuration'].copy()//60000
build_estimate['BuildEstimateDuration']= build_estimate['BuildEstimateDuration'].copy()//60000
build_estimate['BuildTimeStamp'] = pd.to_datetime(build_estimate['BuildTimeStamp'],unit='ms')
build_estimate=build_estimate.sort_values(by=['BuildDuration'], ascending=False)
build_estimate[0:10].plot(x="BuildTimeStamp", y=["BuildDuration", "BuildEstimateDuration"],figsize=(50,15), grid=True,color=["red","darkgreen"])
plt.suptitle('Builds that have crossed the estimated duration time the most', fontsize=40)
plt.ylabel("Time in minutes",fontsize=50)
plt.xlabel("Timestamp",fontsize=50)
plt.legend(labels=mylabels, prop={'size': 50})
table = plt.table(cellText=build_estimate[0:10][['BuildTimeStamp','BuildResult','BuildDuration']].values, colLabels=build_estimate[0:10][['BuildTimeStamp','BuildResult','BuildDuration']].columns,loc='bottom',bbox=[0,-0.95,1,0.6])
table.set_fontsize(38)
plt.savefig('Jenkins Plots\ underestimated.png', format='png',bbox_inches='tight',dpi=300)
