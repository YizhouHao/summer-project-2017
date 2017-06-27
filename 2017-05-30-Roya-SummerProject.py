
# coding: utf-8

# In[2]:

import urllib.parse
import hmac
import hashlib
import base64
import requests
from datetime import datetime
import sys
sys.path.insert(0, '../../info')
import cred


def getResponse(operation, keyword, index, group,page):
    param={'Service':'AWSECommerceService'}
    param['AWSAccessKeyId']=cred.login['AWSAccessKeyId']
    param['AssociateTag']=cred.login['AssociateTag']
    param['Operation']=operation
    if operation=='ItemSearch':
        param['Keywords']=keyword
        param['SearchIndex']=index
        param['ResponseGroup']=group
        param['ItemPage']=page
    elif operation=='BrowseNodeLookup':
        param['BrowseNodeId']=keyword
        
    param['Version']='2013-08-01'
    param['Timestamp']=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    s=urllib.parse.urlencode(sorted(param.items()))
    s="""GET\nwebservices.amazon.com\n/onca/xml\n"""+s
    s=s.encode('utf-8')
    secret=cred.login['SecretKey'].encode('utf-8')
    code=base64.b64encode(hmac.new(secret, msg=s, digestmod=hashlib.sha256).digest())
    param['Signature']=code
    response=requests.get('http://webservices.amazon.com/onca/xml',param)
    #print(response.url)
    return response.text


# In[26]:

import xml.etree.ElementTree as ET
import csv
import os
import urllib.request
import pandas as pd

def extractData(xmlText, keyword):
    root = ET.fromstring(xmlText)
    prefix=root.tag.split("}")[0][1:]
    ns={'amazon':prefix}
    head=['ASIN','Title','Keyword','ImageURL','Brand','Color','Features','Height','Length','Width','Weight','Price','Similars']
    row={}
    #filename='../data/data-table-'+datetime.utcnow().strftime("%Y-%m-%dT%H:%M")+'.csv'
    #fileExists=os.path.exists(filename)
    totalpages=""
    df=pd.DataFrame()
    imgdir='../Amazon-images/'+keyword
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)
    
    #with open(filename, 'a') as csvfile:
        #writer = csv.DictWriter(csvfile, fieldnames=head)
        #if not fileExists:
         #   writer.writeheader()
        
    for items in root.findall('amazon:Items',ns):
        tp=items.find('amazon:TotalPages',ns)
        if tp is not None:
            totalpages=tp.text  
            #print(totalpages)
        for item in items.findall('amazon:Item',ns):
            #ASIN
            asin=item.find('amazon:ASIN',ns)
            if asin is not None:
                row['ASIN']=asin.text
            #keyword
            row['Keyword']=keyword
        
            #images
        
            imagesets=item.find('amazon:ImageSets',ns)
            if imagesets is not None:
                imageset=imagesets.find('amazon:ImageSet',ns)
                if imageset is not None:
                    largeimage=imageset.find('amazon:LargeImage',ns)
                    if largeimage is not None:
                        imageurl=largeimage.find('amazon:URL',ns)
                        if imageurl is not None:
                            row['ImageURL']=imageurl.text 
                            urllib.request.urlretrieve(imageurl.text, imgdir+'/'+row['ASIN']+'.jpg')
                   
            
                   
                
            
            #attributes
        
            features=""
        
            for attr in item.findall('amazon:ItemAttributes',ns):
                #brand
                brand=attr.find('amazon:Brand',ns)
                if brand is not None:
                    row['Brand']=brand.text
                #color    
                color=attr.find('amazon:Color',ns)
                if color is not None:
                    row['Color']=color.text
                #dimensions    
                dime=attr.find('amazon:ItemDimensions',ns)
                if dime is not None:
                    height=dime.find('amazon:Height',ns)
                    if height is not None:
                        row['Height']=height.text
                    length=dime.find('amazon:Length',ns)
                    if length is not None:
                        row['Length']=length.text
                    width=dime.find('amazon:Width',ns)
                    if width is not None:
                        row['Width']=width.text
                    weight=dime.find('amazon:Weight',ns)
                    if weight is not None:
                        row['Weight']=weight.text
                #features
                row['Features']=', '.join([f.text for f in attr.findall('amazon:Feature',ns)])
                #price
                listprice=attr.find('amazon:ListPrice',ns)
                if listprice is not None:
                    price=listprice.find('amazon:FormattedPrice',ns)
                    if price is not None:
                        row['Price']=price.text
                #title 
                title=attr.find('amazon:Title',ns)
                if title is not None:
                    row['Title']=title.text
            #similars 
            for similars in item.findall('amazon:SimilarProducts',ns):
                simList=similars.findall('amazon:SimilarProduct',ns)
                if simList is not None:
                    row['Similars']=', '.join([s.find('amazon:ASIN',ns).text for s in simList])
                
            #print(row)
            #writer.writerow(row)
            df=df.append(row,ignore_index=True)
    return df


# In[27]:

keywords=['chair','sofa','table']
filename='../data/data-table-'+datetime.utcnow().strftime("%Y-%m-%dT%H:%M")+'.csv'
wholeData=pd.DataFrame()
for keyword in keywords:
    xmlText=getResponse('ItemSearch',keyword,'HomeGarden','Images,ItemAttributes,Similarities',1)
    wholeData=wholeData.append(extractData(xmlText,keyword))
    for p in range(2,15):
        xmlText=getResponse('ItemSearch',keyword,'HomeGarden','Images,ItemAttributes,Similarities',p)
        wholeData=wholeData.append(extractData(xmlText,keyword))
wholeData.to_csv(filename)       


# In[ ]:

getResponse('BrowseNodeLookup',1063278,'','',1)


# In[ ]:



