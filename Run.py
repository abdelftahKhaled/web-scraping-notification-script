# import subprocess
# packages = ['beautifulsoup4', 'requests', 'winotify']
# for package in packages:
#         subprocess.call(['pip', 'install', package])
import subprocess
import sys
import os
import importlib
import time
venv_name = 'venv'
packages=['beautifulsoup4', 'requests', 'winotify']

dir_file=os.getcwd()
path_file=__file__
name_file=os.path.basename(path_file)
path_venv=os.path.join(dir_file,venv_name)
list_file_in_dir=os.listdir(dir_file)
file_python_in_venv=os.path.join(path_venv,'Scripts','python')
file_pip_in_venv=os.path.join(path_venv,'pip')
def create_virtualenv():
    global venv_name
    if not os.path.exists(path_venv):
  
        subprocess.check_call([sys.executable, '-m', 'venv', venv_name])
    else:
        print(f"Virtual environment '{venv_name}' already exists!")



def run_script():
    """
    Function to run your script
    """
    global venv_name
    global path_file
    global list_file_in_dir
    global name_file
    global path_venv
    global  file_python_in_venv
    # for file in list_file_in_dir:
    #         # if file.endswith(('.py','.pyw')) and file !=name_file:
    combined_cmd = f'{file_python_in_venv} {os.path.join(dir_file,'packeges.py')}'
    subprocess.call(combined_cmd, shell=True)

if __name__ == "__main__":
    create_virtualenv()
    run_script()



   


