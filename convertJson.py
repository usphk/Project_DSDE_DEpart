import pandas as pd
import json
import os


rows = []
count = 0
directory = '/Project/2018'

for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
                # Load the JSON file
            with open(file_path, 'r') as fd:

                    cat = json.load(fd)
                  
                    item = cat['abstracts-retrieval-response']['item']
                    title = item['bibrecord']['head']['citation-title']
                    # publish = item['bibrecord']['head']['source']['publisher']['publishername']
                    # refcount = item['bibrecord']['tail']['bibliography']['@refcount']
                    citedby_count = cat['abstracts-retrieval-response'].get('coredata', {}).get('citedby-count', None)
                            
                    authors = set()
                    countries = set()
                    departments = set()
                    affiliations = set()
                    keywords = set()  # Get keywords if available
                    subject_areas = set()
                            
                    if item.get('bibrecord') and item['bibrecord'].get('tail') and item['bibrecord']['tail'].get('bibliography'):
                        refcount = item['bibrecord']['tail']['bibliography'].get('@refcount')
                    else:
                        refcount = None  # หรือจัดการกับกรณีนี้ตามที่ต้องการ

                    publish = item.get('bibrecord', {}).get('head', {}).get('source', {}).get('publisher', {}).get('publishername', None)

                     # Collect authors and their affiliations
                    author_groups = item['bibrecord']['head']['author-group']
                    if isinstance(author_groups, dict):
                        author_groups = [author_groups]
                    
                    for author_group in author_groups:
                        affiliation = author_group.get('affiliation', {})
                                    
                        # Add country, department, and other affiliation details
                        if affiliation.get('country'):
                            countries.add(affiliation['country'])
                        organizations = affiliation.get('organization', None)
                        if organizations and isinstance(organizations, list):
                            # เพิ่ม affiliation หากมีข้อมูลในตำแหน่งที่ 2
                            if len(organizations) > 2 and organizations[2] is not None:
                                affiliations.add(organizations[2].get('$', 'Unknown'))
                            
                            # Extract subject areas
                        for subject in cat['abstracts-retrieval-response']['subject-areas']['subject-area']:
                            subject_areas.add(subject['$'])
                        if (cat['abstracts-retrieval-response']['authkeywords'] is None):
                            keywords.add(None)
                        else:
                            tmp = cat['abstracts-retrieval-response']['authkeywords']['author-keyword']
                            if isinstance(tmp, dict):
                                tmp = [tmp]
                            for keyword in tmp:
                                keywords.add(keyword.get('$', None))
                    # Compile data into a single row
                    row = {
                        'title': title,
                        'countries': list(countries) if countries else None,
                        'affiliations': list(affiliations) if affiliations else None,
                        'Publisher' : publish,
                        'Ref_count' : refcount,
                        'Cited_count' : citedby_count,
                        'keywords': list(keywords) if keywords else None,
                        'subject_areas': list(subject_areas) if subject_areas else None
                    }
                    rows.append(row)
                    # print(title)
                    
                  
          
# df = pd.json_normalize(rows)
df = pd.DataFrame(rows)

df.to_csv('/project.csv', index=False)

