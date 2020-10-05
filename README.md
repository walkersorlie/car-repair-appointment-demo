# G5 Car Repair Appointment Demo

### These commands are specified for Ubuntu/Linux Mint/Debian distributions

1. Clone this repository into the directory of your choosing
2. Change into the directory git created for the repository. In this directory (the repository root), create a python virtual environment to manage the python dependencies (requires python 3) using this command: `python3 -m venv VIRTUALENV_NAME` substituting `VIRTUALENV_NAME` with the name of your choosing.
3. To activate the virtual environment, use this command: `. VIRTUALENV_NAME/bin/activate`
4. Once the virtual environment is active (you should see the name of the virtual environment appended at the beginning of your terminal prompt, e.g. `(.venv) walker@walksoley:~/Documents/Projects/G5Demo/car_appointment$`) install the required dependencies listed in `requirements.txt` by using this command: `pip install -r requirements.txt`. If you have errors installing dependencies you may have to run these commands:
  * `pip3 install --upgrade setuptools`
  * `pip3 install wheel`
  * `sudo apt-get install python-dev`
  * `sudo apt-get install python3-dev (or for example: sudo apt-get install python3.7-dev if you used Python3.7 to make the virtual environment)`
  * `sudo apt-get install snapd`

5. Once the dependencies are finished installing, change into the `car_appointment` directory (the Django project directory)
6. Before launching the server we have to apply migrations to the database. Run this command to update the database: `python manage.py migrate` (make sure you are in the directory that contains the `manage.py` file)
7. In the `car_appointment` directory run this command to start the server: `./manage.py runserver` (make sure you are in the directory that contains the `manage.py` file). The server starts up listening on port `8000`. In your browser, navigate to `http://127.0.0.1:8000/` (or `localhost:8000/`) to explore the project
8. Emails are output to the console (command line prompt)
