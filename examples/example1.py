# -*- coding: utf-8 -*-
"""Example of in Visual Studio Code (Python Interactive Window), or ATOM with Hydrogen querying the Cacophony Project Servers via a REST API using a Python Client."""
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
print(os.getcwd())

# %% 

try:
	# os.chdir(os.path.join(os.getcwd(), '..\\..\..\AppData\Local\Temp'))
	os.chdir(os.path.join(os.getcwd(), 'python-api'))
	print(os.getcwd())
except:
	pass
# %%
from IPython import get_ipython

# %% [markdown]
# # TEST NOTEBOOK for Python REST API client  connect to  Cacophony project server
# %% [markdown]
# #### Configuration

# %%
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# %%
import logging, sys, os
logging.basicConfig(format='%(asctime)s : %(module)s :%(levelname)s : %(message)s', level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.info("Logging Started ---------------- LEVEL: {} -------------".format(logging.getLevelName(logger.level)))


# %%
import json
from datetime import datetime
import pandas as pd
import numpy as np

# %%
test= ''
str(test)
# %%
from cacophonyapi.user  import UserAPI
from cacophonyapi.config  import Config


# %%
config=Config().load_config(config_file=os.path.join(os.getcwd(),'.env','defaultconfig.json'))


# %%

cp_client = UserAPI(baseurl=config.api_url,
                            username=config.admin_username,
                            password=config.admin_password)
cp_client.version

# %% [markdown]
# ### SHOW devices and groups

# %%
pd.DataFrame(cp_client.get_devices_as_json())


# %%
pd.DataFrame(cp_client.get_groups_as_json()["groups"])

# %% [markdown]
# 
# ## Define some helper functions
# 
#     strToSqlDateTime : Generates a datatime object from a string
# 
#     recordingSubset : Retrieve a subset of dataframe
# 
#     pandas_df_to_markdown_table : Displays a markdown table from a dataframe
#     
#     pandas_df_to_markdown_table : Generates a string representing the markdown table
# 
# 

# %%
strToSqlDateTime = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

def recordingSubset(dataframe=None,startDateUTC=None,endDateUTC=None,fields=None):
    """Generate a DataFrame from a subset of recording time points of an existing Dataframe.

    Returns a Pandas Dataframe subset of recordingings by date and Time inclusive of the lower and upper limit. NB date ranges must be in GMT

    :param startDateUTC: lower value for recordings to select
    :param endDateUTC: upper value (inclusive) of recordings to select
    :param fields: a list of columns to include in the subset of recordings
    """
    # fields = ["recordingDateTime_DT_local",'recordingURL','comment']
    return dataframe[(df.recordingDateTime >= startDateUTC) & (df.recordingDateTime <= endDateUTC)].loc[:,
        fields]

def pandas_df_to_markdown_table(df,*args,**kwargs):
    """Generate a Markdown Display (IPython) of the Pandas Dataframe.

    Displays in a IPython environment such as Jupyter Notebook

    :param columns: [Optional, default 'list(df.columns)'] A list of columns to display
    """
    df['index'] = df.index
    if 'columns' not in kwargs:
        columns=list(df.columns)
    else:
        columns=['index']+kwargs['columns']

    from IPython.display import Markdown, display


    fmt = ['---' for i in range(len(df.columns))]
    df_fmt = pd.DataFrame([fmt], columns=df.columns)
    df_formatted = pd.concat([df_fmt, df])
    display(Markdown(df_formatted.loc[:,columns].to_csv(sep="|", index=False)))


def pandas_df_to_markdown_table_string(df,*args,**kwargs):
    """Generate a Markdown string representing the Pandas Dataframe.

    Returns a string representing the dataframe in markdown syntax

    :param columns: [Optional, default 'list(df.columns)'] A list of columns to display
    """
    df['index'] = df.index
    if 'columns' not in kwargs:
        columns=df.columns.to_list()
    else:
        columns=['index']+kwargs['columns']
    from IPython.display import Markdown, display
    headers = ['- {} -'.format(col) for i,col in enumerate(df.columns)]
    fmt = ['---' for i in range(len(df.columns))]
    df_headers = pd.DataFrame([headers], columns=df.columns)
    df_fmt = pd.DataFrame([fmt], columns=df.columns)
    df_formatted = pd.concat([df_fmt, df])
    return df_formatted.loc[:,columns].to_csv(sep="|", index=False)

# %% [markdown]
# 
# ## Query for first 300 recordings
# 
# 

# %%
queryResponse=cp_client.query(endDate=strToSqlDateTime("2019-11-06 06:30:00"),startDate=strToSqlDateTime("2019-11-01 19:00:00"),limit=300,offset=0,tagmode="any")
df = pd.DataFrame(queryResponse)


# %%

df.columns


# %%
pd.options.display.html.table_schema = True
pd.options.display.max_rows = None
from IPython.display import HTML

# %% [markdown]
# ### Format the Data

# %%
df['recordingDateTime_DT'] = pd.to_datetime(df['recordingDateTime'])
df['Date']=df['recordingDateTime_DT'].dt.date # TODO: Check where we are using this
df['recordingDateTime_DT_local'] = df['recordingDateTime_DT'].dt.tz_convert('Pacific/Auckland').dt.strftime('%Y/%m/%d %H:%M:%S')
df['recordingURL']=df['id'].apply(lambda id: '<a href="https://browse.cacophony.org.nz/recording/{id}">{id}</a>'.format(id=id))
df['recordingURLmd']=df['id'].apply(lambda id: '[{id}](https://browse.cacophony.org.nz/recording/{id})'.format(id=id))


df['metric_recordingCount']=1
df['metric_gainIssueTrue'] = (df.comment.str.contains('[G|g]ain')==True).apply(lambda x: 1 if x else 0)
df['metric_gainIssueTrue'] = (df.comment.str.contains('(?i)[G|g]ain')==True).apply(lambda x: 1 if x else 0)

df['metric_gainIssueFalse']= ((df.comment.str.contains('[G|g]ain')!=True ) | (df.comment.isnull())).apply(lambda x: 1 if x else 0)
df['metric_otherComment']= ((df.comment.str.contains('[G|g]ain')!=True ) & (~df.comment.isnull())).apply(lambda x: 1 if x else 0)

# %% [markdown]
# # EXAMPLES 
# 
# exaples of various queries
# 

# %%
HTML(recordingSubset(df, '2019-11-04T06:00Z','2019-11-04T21:00Z',["recordingDateTime_DT_local",'recordingURL','comment'] ).to_html(escape=False))


# %%
doi='2019-11-05'
pandas_df_to_markdown_table(recordingSubset(df[df.metric_gainIssueTrue==1],
         '{}T06:00Z'.format(doi),'{}T21:00Z'.format(doi),["recordingDateTime_DT_local",'recordingURLmd','comment']))


# %%
# df.groupby(by=df['recordingDateTime_DT'].dt.date).sum()
dfp=pd.pivot_table(df, index=['Date'],values=['metric_recordingCount','metric_gainIssueTrue','metric_gainIssueFalse','metric_otherComment'],aggfunc=np.sum)
# dfp

dfp['percentGainIssueTrue'] = (dfp.metric_gainIssueTrue/dfp.metric_recordingCount*100.0).map('{0:,.2f}%'.format)
dfp.loc[:,['percentGainIssueTrue','metric_recordingCount','metric_gainIssueTrue','metric_gainIssueFalse','metric_otherComment']]
pandas_df_to_markdown_table(dfp,columns=['percentGainIssueTrue','metric_recordingCount','metric_gainIssueTrue','metric_gainIssueFalse','metric_otherComment'])


# %%
print(pandas_df_to_markdown_table_string(dfp,columns=['percentGainIssueTrue','metric_recordingCount','metric_gainIssueTrue','metric_gainIssueFalse','metric_otherComment']))


# %%


