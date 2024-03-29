import os
import sys
from azure.identity import DefaultAzureCredential
import psycopg2

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

# cred = DefaultAzureCredential()
# accessToken = cred.get_token('https://ossrdbms-aad.database.windows.net/.default')
conn_string = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')

# Combine the token with the connection string from the environment variables added by Service Connector to establish the connection.
# conn = psycopg2.connect(conn_string + ' password=' + accessToken.token) 

# For a secret auth, we can just use the provided connection string
conn = psycopg2.connect(conn_string)

app = Flask(__name__)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
   return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():

   version = "unknown"
   with conn.cursor() as curs:
      try:
         # simple single row system query
         curs.execute("SELECT version()")

         # returns a single row as a tuple
         version = curs.fetchone()

      # a more robust way of handling errors
      except (Exception, psycopg2.DatabaseError) as error:
         print(error)

   name = request.form.get('name') + " " + version[0]

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
