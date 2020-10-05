# G5 Car Repair Appointmet Demo

1. Clone this repository into the directory of your choosing
2. In the directory of the repository root, create a python virtual environment to manage the python dependencies (requires python 3): `python3 -m venv VIRTUALENV_NAME`
3. To activate the virtual environment, use this command: `. VIRTUALENV_NAME/bin/activate`
4. Once the virtual environment is active (you should see the name of the virtual environment appended at the beginning of your terminal prompt, e.g. `(.venv) walker@walksoley:~/Documents/Projects/G5Demo/car_appointment$`) install the required dependencies listed in `requirements.txt` by using this command: `pip install -r requirements.txt`
5. Once the dependencies are finished installing, change into the `car_appointment` directory (the Django project directory)
6. In the `car_appointment` directory run this command to start the server: `./manage.py runserver` (make sure you are in the directory that contains the `manage.py` file). The server starts up listening on port `8000`. In your browser, navigate to `http://127.0.0.1:8000/` (or `localhost:8000/`) to explore the project
7. Emails are output to the console (command line prompt)
