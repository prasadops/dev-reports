#  Copyright (c)  OpsMx, Purushotham Koduri

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import logging

date = '1st Dec-8thDec'
issue_report = status_report=severity_report=resolution_report=pd.DataFrame()

try:
    issue_report = pd.read_csv(rf'{date}/Sonarqube/issuetype_report.csv')
    status_report = pd.read_csv(rf'{date}\Sonarqube\status_report.csv')
    severity_report = pd.read_csv(rf'{date}\Sonarqube\severity_report.csv')
    resolution_report = pd.read_csv(rf'{date}\Sonarqube\resolution_report.csv')
except FileNotFoundError:
    logging.warning("Files are missing")

pathlib.Path('Sonarqube Plots').mkdir(parents=True, exist_ok=True)



def stacked_graph(df, colors, title):
    projects = df.iloc[:, 0]
    indx = np.arange(len(df))
    font_color = '#525252'
    csfont = {'fontname': 'Georgia'}
    hfont = {'fontname': 'Calibri'}
    ax = df.plot.barh(align='center', stacked=True, figsize=(20, 10), color=colors, width=0.45)
    plt.tight_layout()
    plt.subplots_adjust(top=0.8, left=0.26)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(15)
    plt.xticks(color=font_color, **hfont)
    plt.yticks(indx, projects, color=font_color, **hfont)
    plt.ylabel('ProjectName', fontsize=18)
    plt.xlabel('Number of issues', fontsize=18)
    plt.legend(prop={'size': 19})
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


def pie_chart(df):
    cmap = plt.get_cmap('autumn')
    font_color = '#525252'
    csfont = {'fontname': 'Georgia'}  # title font
    hfont = {'fontname': 'Calibri'}  # main font
    fig, axes = plt.subplots(3, 3, figsize=(30, 30))
    colours = {'Blocker': cmap(0.1),
               'Critical': cmap(0.4),
               'Major': cmap(0.7),
               'Minor': cmap(1.0),
               'Info': '#C3A316'}
    axes[2, 2].set_axis_off()
    axes[2, 1].set_axis_off()

    for i, (idx, row) in enumerate(df.set_index('ProjectName').iterrows()):
        ax = axes[i // 3, i % 3]
        row = row[row.gt(row.sum() * .01)]
        ax.pie(row, labels=row.index, normalize=True, startangle=30, autopct='%1.0f%%',
               colors=[colours[key] for key in row.index], textprops={'fontsize': 20})
        ax.set_title(idx, fontsize=25)

    fig.subplots_adjust(wspace=.2)


df = severity_report[severity_report.ProjectName != 'issue-generator']
df = df[df.ProjectName != 'restapp']
df['ProjectName'] = df['ProjectName'].str.title()
df['ProjectName'] = df['ProjectName'].str.replace('Oes-', '')
pie_chart(df)
plt.savefig('Sonarqube Plots\ Overall_sonarqube_issues.png', format='png', dpi=300)
cmap = plt.get_cmap('autumn')
colors = [cmap(i) for i in np.linspace(0.1, 1.3, 5)]
projects = issue_report.iloc[:, 0]
issue_report['ProjectName'] = issue_report['ProjectName'].str.title()
issue_report['ProjectName'] = issue_report['ProjectName'].str.replace('Oes-', '')
df = issue_report[issue_report.ProjectName != 'Issue-Generator']
df = df[df.ProjectName != 'Restapp']
stacked_graph(df, colors, "Issue Type of the Week",)
plt.savefig('Sonarqube Plots\ issuetype.png', format='png', dpi=300,bbox_inches='tight')
# current status
cmap = plt.get_cmap('Blues')
colors = [cmap(i) for i in np.linspace(0.2, 1.3, 7)]
status_report['ProjectName'] = status_report['ProjectName'].str.title()
status_report['ProjectName'] = status_report['ProjectName'].str.replace('Oes-', '')
df = status_report[status_report.ProjectName != 'Issue-Generator']
df = df[df.ProjectName != 'Restapp']
stacked_graph(df, colors, "Current status of issues")
plt.savefig('Sonarqube Plots\ current status.png', format='png', dpi=300,bbox_inches='tight')
cmap = plt.get_cmap('autumn')
colors = {'Blocker': cmap(0.1),
          'Critical': cmap(0.4),
          'Major': cmap(0.7),
          'Minor': cmap(1.0),
          'Info': '#C3A316'}
severity_report['ProjectName'] = severity_report['ProjectName'].str.title()
severity_report['ProjectName'] = severity_report['ProjectName'].str.replace('Oes-', '')
df = severity_report[severity_report.ProjectName != 'Issue-Generator']
df = df[df.ProjectName != 'Restapp']
stacked_graph(df, colors, "Severity of issues")
plt.savefig('Sonarqube Plots\ severity.png', format='png', dpi=300,bbox_inches='tight')

# Resolution status
cmap = plt.get_cmap('Blues')
colors = [cmap(i) for i in np.linspace(0.2, 1.3, 7)]
resolution_report['ProjectName'] = resolution_report['ProjectName'].str.title()
resolution_report['ProjectName'] = resolution_report['ProjectName'].str.replace('Oes-', '')
df = resolution_report[resolution_report.ProjectName != 'Issue-Generator']
df = df[df.ProjectName != 'Restapp']
stacked_graph(df, colors, "Resolution status")
plt.savefig('Sonarqube Plots\ resolution.png', format='png', dpi=300,bbox_inches='tight')
