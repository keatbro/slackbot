import os
import psycopg2
import openai
from dotenv import load_dotenv

load_dotenv()

# Function for executing queries against the db
def get_schema():
  conn = psycopg2.connect(
      user = "querything_root",
      password = os.getenv('QUERYTHING_ROOT_USER_PW'),
      host = os.getenv('QUERYTHING_HOST'),
      port = "5432",
      database = "ecommerce"
  )

  query = '''
  select
  table_name,
  column_name,
  data_type
  from information_schema.columns
  where
  table_schema = 'public'
  order by 1,2
  '''
  cur = conn.cursor()
  cur.execute(query)
  result = cur.fetchall()
  conn.close()
  return result

# Get OpenAI to return the query to answer your question

def answer_question(schema, question):

  prompt = '''
  You will play the role of a Data Analyst. 
  I will give you the schema of a PostgreSQL database, and using that schema, you will return the SQL queries that will be used to answer the questions that you are asked.
  You will reply only with PostgreSQL. There will be no text that isn't SQL in your response.
  I will provide the schema in the form of an array, where there are three elements in each item in the array. These elements correspond to the Table name, the Column name, and the Column data type.
  '''
  
  openai.api_key = os.environ['OPENAI_API_KEY']
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": prompt},
        {"role": "system", "content": f'The schema is {schema}'},
        {"role": "system", "content": question}
    ]
  )

  # get proposed query from GPT
  query = response['choices'][0]['message']['content']

  conn = psycopg2.connect(
        user = "querything_root",
        password = os.getenv('QUERYTHING_ROOT_USER_PW'),
        host = os.getenv('QUERYTHING_HOST'),
        port = "5432",
        database = "ecommerce"
    )
  
  cur = conn.cursor()
  cur.execute(query)
  result = cur.fetchall()
  conn.close()

  data = {'query_used': query, 'data_returned': result[0][0]}

  return(data)