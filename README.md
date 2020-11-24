# Amys Bakery Web Service
This is a website for Amy's Bakery

# Things need to download
- install python 3.9.0, here is the link -->  https://www.python.org/downloads/

- Install flask: 
````
sudo python -m pip3 install flask --user
````

### To run the web service:
- First, activate the amysBakeryWeb's environment:
````
source venv/bin/activate
````
- Second, set the environment to be "development":
````
export FLASK_ENV=development
````
- Finally, run the server:
````
flask run
````
You should see the following response if the service is started successfully:
````
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 277-587-088
 ````
