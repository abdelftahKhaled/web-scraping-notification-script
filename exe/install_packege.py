import subprocess
packages=['beautifulsoup4','requests','winotify']
for package in packages:
        subprocess.call(['pip', 'install', package]) 