from flask import Flask
import sys
from time import sleep

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
server_name_str=sys.argv[1]

sleep_time = int(sys.argv[2])
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def server_name():
    global server_name_str
    sleep(sleep_time)
    return 'server:{}'.format(server_name_str)
@app.route('/healthcheck')
def healthcheck():
    return str(200)
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host="0.0.0.0",port=5000)