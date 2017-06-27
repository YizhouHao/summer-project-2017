
# coding: utf-8

# In[21]:

import pandas as pd
import numpy as np
df = pd.read_csv('../data/data-table-2017-06-22T20:29.csv')
featureList=df['Features'].tolist()


# In[28]:

from textblob import TextBlob
blobList=map(TextBlob, featureList)
tags=[b.tags for b in blobList]
print(tags)


# In[38]:

import pandas as pd
import numpy as np
df = pd.read_csv('../data/data-table-2017-06-23T03-23.csv')
missing= df['Features'].isnull()
modern= df['Features'].str.contains('formal',case=False)
df[~missing & modern]


# In[ ]:



