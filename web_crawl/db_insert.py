import pandas as pd
from sqlalchemy import create_engine
contents = pd.read_excel('blog_content.xlsx')

contents = contents.drop(['Unnamed: 0'], axis=1)
# print(contents)

engine = create_engine('mysql+pymysql://root:1234@localhost/o2')

contents.to_sql('contents',con=engine,if_exists='append', chunksize=1000)

