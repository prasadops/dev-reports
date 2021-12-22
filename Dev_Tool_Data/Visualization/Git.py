#  Copyright (c)  OpsMx, Purushotham Koduri

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import logging
import pathlib

date = '1st Dec-8thDec'

Analytics = repo_stats=Audit_client=Audit_service=Dashboard=Gate=Sapor=Oestest=UI=Platform=Visibility=pd.DataFrame()

try:
    repo_stats = pd.read_csv(rf'{date}/Git/repostats.csv')
    Analytics = pd.read_csv(rf'{date}\Git\Analytics-linechanges-sorted-merged.csv')
    Audit_client = pd.read_csv(rf'{date}\Git\audit-client-service-linechanges-sorted-merged.csv')
    Audit_service = pd.read_csv(rf'{date}\Git\audit-service-linechanges-sorted-merged.csv')
    Dashboard = pd.read_csv(rf'{date}\Git\dashboard-service-linechanges-sorted-merged.csv')
    Gate = pd.read_csv(rf'C:{date}\Git\gate-linechanges-sorted-merged.csv')
    Sapor = pd.read_csv(rf'{date}\Git\oes-api-linechanges-sorted-merged.csv')
    Oestest = pd.read_csv(rf'{date}\Git\oes-test-linechanges-sorted-merged.csv')
    UI = pd.read_csv(rf'{date}\Git\oes-ui-linechanges-sorted-merged.csv')
    Platform = pd.read_csv(rf'{date}\Git\platform-service-linechanges-sorted-merged.csv')
    Visibility = pd.read_csv(rf'{date}\Git\visibility-service-linechanges-sorted-merged.csv')
except FileNotFoundError:
    logging.error("Files are missing")

repo_stats['repoName'] = repo_stats['repoName'].str.title()
repo_stats['repoName'] = repo_stats['repoName'].str.replace('Oes-', '')
repo_stats['repoName'] = repo_stats['repoName'].str.replace('-Service-', '')

pathlib.Path('Git Plots').mkdir(parents=True, exist_ok=True)

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
    plt.tick_params(axis='both', which='major', labelsize=16)
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


def pie_chart(series, names):
    plt.figure(1, figsize=(10, 10))
    cmap = plt.get_cmap('coolwarm')
    colors = [cmap(i) for i in np.linspace(0, 1, 10)]

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


def subcategorybar(df, title):
    colors = ['#2874A6', '#239B56', '#F1C40F']
    font_color = '#525252'
    ax = df.plot(kind='bar', figsize=(25, 15), width=0.8, color=colors)
    ax.set_xticklabels(list(df.index), rotation=70)
    csfont = {'fontname': 'Georgia'}
    hfont = {'fontname': 'Calibri'}
    plt.tight_layout()
    plt.ylabel('Number of Lines')
    plt.xlabel('Committer')
    ax.tick_params(axis='x', colors='black')
    ax.yaxis.label.set_color('black')
    ax.xaxis.label.set_color('black')
    ax.tick_params(axis='y', colors='black')
    ax.bar_label(ax.containers[0], size=18)
    ax.bar_label(ax.containers[1], size=18)
    ax.bar_label(ax.containers[2], size=18)
    ax.set_title(title, pad=60, fontsize=28, color=font_color, **csfont)
    ax.legend(prop={'size': 19}, bbox_to_anchor=(1.1, 1.05))


def simple_bar_chart(series, labels, title):
    font_color = '#525252'
    csfont = {'fontname': 'Georgia'}
    fig, ax = plt.subplots(figsize=(20, 10))
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['text.color'] = 'black'
    plt.rcParams['font.size'] = 18
    cmap = plt.get_cmap('Blues')
    colors = [cmap(i) for i in np.linspace(0.3, 1.3, 5)]
    ind = np.arange(len(series))
    bars1 = ax.bar(labels, series,
                   color="steelblue", width=0.3)
    ax.bar_label(ax.containers[0])
    ax.set_title(title, pad=60, fontsize=18, color=font_color, **csfont)
    ax.set_ylabel("Total number of files changes(added & deleted)", fontsize=18)
    ax.set_xticks(range(0, len(ind)))
    ax.set_xticklabels(list(labels), rotation=70)
    ax.set_xlabel("Committer", fontsize=18)
    ax.tick_params(axis='x', colors='black')
    ax.yaxis.label.set_color('black')
    ax.xaxis.label.set_color('black')
    ax.tick_params(axis='y', colors='black')
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.set_title(title, pad=60, fontsize=38)


pie_chart(repo_stats[' CommitsInMergedPRs'], repo_stats['repoName'])
plt.savefig('Git Plots\ service_breakdown.png', format='png', dpi=300, bbox_inches='tight')

colors = ['#2874A6', '#239B56', '#F1C40F']
df = repo_stats[['repoName', ' OpenPRCount', ' MergedPRCount', ' ForcefullyClosedPR']]
stacked_graph(df, colors, "Repository-wise PR data")
plt.savefig('Git Plots\ PR-wise.png', format='png', dpi=300, bbox_inches='tight')

colors = ['#2874A6', '#239B56', '#F1C40F']
df = repo_stats[['repoName', ' CommitsInOpenPRs', ' CommitsInMergedPRs', ' CommitsInForcefullyClosedPRs']]
stacked_graph(df, colors, "Repository-wise commit data")
plt.savefig('Git Plots\ commit-wise.png', format='png', dpi=300, bbox_inches='tight')

df = Analytics.groupby(' Committer').sum()
if len(df) > 0:
    simple_bar_chart(df[' LinesChanges'], df.index, f"Analytics Contributers")
    plt.ylabel("Total number of lines changes(added & deleted)", fontsize=18)
    plt.savefig('Git Plots\ Analytics_contributers.png', format='png', dpi=300, bbox_inches='tight')
    simple_bar_chart(df[' FilesChanged'], df.index, f"Analytics Files changes made by users")
    plt.savefig('Git Plots\ Analytics_filechanges.png', format='png', dpi=300, bbox_inches='tight')
    subcategorybar(df[[' LinesChanges', ' LinesAdded', ' LinesDeleted']], "Analytics Repository Data")
    plt.tight_layout()
    plt.savefig('Git Plots\ Analytics_lines.png', format='png', dpi=300, bbox_inches='tight')

else:
    logging.warning("No data")

df = Dashboard.groupby(' Committer').sum()
if len(df) > 0:
    simple_bar_chart(df[' LinesChanges'], df.index, f"Dashboard Contributers")
    plt.ylabel("Total number of lines changes(added & deleted)", fontsize=18)
    plt.savefig('Git Plots\ Dashboard_contributers.png', format='png', dpi=300, bbox_inches='tight')
    plt.close()

    simple_bar_chart(df[' FilesChanged'], df.index, f"Dashboard Files changes made by users")
    plt.savefig('Git Plots\ Dashboard_Files.png', format='png', dpi=300, bbox_inches='tight')
    plt.close()

    subcategorybar(df[[' LinesChanges', ' LinesAdded', ' LinesDeleted']], "Dashboard Repository Data")
    plt.savefig('Git Plots\ Dashboard_lines.png', format='png', dpi=300, bbox_inches='tight')
    plt.close()

    plt.tight_layout()
else:
    logging.warning("No data")
df=Sapor.groupby(' Committer').sum()
if len(df)>0:
        simple_bar_chart(df[' LinesChanges'],df.index,f"Sapor Contributers")
        plt.ylabel("Total number of lines changes(added & deleted)",fontsize=18)
        plt.savefig('Git Plots\ Sapor_contributers.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        simple_bar_chart(df[' FilesChanged'],df.index,f"Sapor Files changes made by users")
        plt.savefig('Git Plots\ Sapor_files.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        subcategorybar(df[[' LinesChanges',' LinesAdded',' LinesDeleted']],"Sapor Repository Data")
        plt.savefig('Git Plots\ Sapor_files.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        plt.tight_layout()
else:
    logging.warning("No data in sapor")

df=Audit_client.groupby(' Committer').sum()
if len(df)>0:
        simple_bar_chart(df[' LinesChanges'],df.index,f"Analytics Contributers")
        plt.ylabel("Total number of lines changes(added & deleted)",fontsize=18)
        plt.savefig('Git Plots\ Audit_client_contributers.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        simple_bar_chart(df[' FilesChanged'],df.index,f"Analytics Files changes made by users")
        plt.savefig('Git Plots\ Audit_client_files.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        subcategorybar(df[[' LinesChanges',' LinesAdded',' LinesDeleted']],"Analytics Repository Data")
        plt.savefig('Git Plots\ Audit_client_lines.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        plt.tight_layout()

else:
    logging.warning("No data sapor")

df=Audit_service.groupby(' Committer').sum()
if len(df)>0:
        simple_bar_chart(df[' LinesChanges'],df.index,f"Audit_service Contributers")
        plt.ylabel("Total number of lines changes(added & deleted)",fontsize=18)
        plt.savefig('Git Plots\ Audit_service_contributers.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        simple_bar_chart(df[' FilesChanged'],df.index,f"Audit_service Files changes made by users")
        plt.savefig('Git Plots\ Audit_service_files.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        subcategorybar(df[[' LinesChanges',' LinesAdded',' LinesDeleted']],"Audit_service Repository Data")
        plt.savefig('Git Plots\ Audit_service_lines.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        plt.tight_layout()
else:
    logging.warning("No data")

df=Gate.groupby(' Committer').sum()
if len(df)>0:
        simple_bar_chart(df[' LinesChanges'],df.index,f"Gate Contributers")
        plt.ylabel("Total number of lines changes(added & deleted)",fontsize=18)
        plt.savefig('Git Plots\ Gate_contributers.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        simple_bar_chart(df[' FilesChanged'],df.index,f"Gate Files changes made by users")
        plt.savefig('Git Plots\ Gate_files.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        subcategorybar(df[[' LinesChanges',' LinesAdded',' LinesDeleted']],"Gate Repository Data")
        plt.savefig('Git Plots\ Gate_lines.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        plt.tight_layout()
else:
    logging.warning("No data")

df=Oestest.groupby(' Committer').sum()
if len(df)>0:
        simple_bar_chart(df[' LinesChanges'],df.index,f"Oes-test Contributers")
        plt.ylabel("Total number of lines changes(added & deleted)",fontsize=18)
        plt.savefig('Git Plots\ Oestest_contributers.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        simple_bar_chart(df[' FilesChanged'],df.index,f"Oes-test Files changes made by users")
        plt.savefig('Git Plots\ Oestest_files.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        subcategorybar(df[[' LinesChanges',' LinesAdded',' LinesDeleted']],"Oes-test Repository Data")
        plt.savefig('Git Plots\ Oestest_lines.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        plt.tight_layout()
else:
    logging.warning("No data")

UI.columns = ['commitid', ' Committer', ' FilesChanged', ' LinesChanges', ' LinesAdded', ' LinesDeleted']
df=UI.groupby(' Committer').sum()
if len(df)>0:
        simple_bar_chart(df[' LinesChanges'],df.index,f"UI Contributers")
        plt.ylabel("Total number of lines changes(added & deleted)",fontsize=18)
        plt.savefig('Git Plots\ UI_contributers.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        simple_bar_chart(df[' FilesChanged'],df.index,f"UI Files changes made by users")
        plt.savefig('Git Plots\ UI_files.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        subcategorybar(df[[' LinesChanges',' LinesAdded',' LinesDeleted']],"UI Repository Data")
        plt.savefig('Git Plots\ UI_lines.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        plt.tight_layout()
else:
    logging.warning("No data")

Platform.columns = ['commitid', ' Committer', ' FilesChanged', ' LinesChanges', ' LinesAdded', ' LinesDeleted']
df=Platform.groupby(' Committer').sum()
if len(df)>0:
        simple_bar_chart(df[' LinesChanges'],df.index,f"Platform Contributers")
        plt.ylabel("Total number of lines changes(added & deleted)",fontsize=18)
        plt.savefig('Git Plots\ Platform_contributers.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        simple_bar_chart(df[' FilesChanged'],df.index,f"Platform Files changes made by users")
        plt.savefig('Git Plots\ Platform_files.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        subcategorybar(df[[' LinesChanges',' LinesAdded',' LinesDeleted']],"Platform Repository Data")
        plt.savefig('Git Plots\ Platform_lines.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        plt.tight_layout()
else:
    logging.warning("No data")

Visibility.columns = ['commitid', ' Committer', ' FilesChanged', ' LinesChanges', ' LinesAdded', ' LinesDeleted']
df=Visibility.groupby(' Committer').sum()
if len(df)>0:
        simple_bar_chart(df[' LinesChanges'],df.index,f"Visibility Contributers")
        plt.ylabel("Total number of lines changes(added & deleted)",fontsize=18)
        plt.savefig('Git Plots\ Visibility_contributers.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        simple_bar_chart(df[' FilesChanged'],df.index,f"Visibility Files changes made by users")
        plt.savefig('Git Plots\ Visibility_files.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        subcategorybar(df[[' LinesChanges',' LinesAdded',' LinesDeleted']],"Visibility Repository Data")
        plt.savefig('Git Plots\ Visibility_lines.png', format='png', dpi=300, bbox_inches='tight')
        plt.close()

        plt.tight_layout()
else:
    logging.warning("No data")


