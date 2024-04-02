# iGEM IISc 2024 Website
First, I would like to thank you for visiting this repo. This repository contains all the files for the iGEM IISc 2024 website.

## Installation for Development

> [!NOTE]
> If you are using a UNIX based OS (like macOS or linux), use ```python3``` instead of ```python``` in all the commands where you have to write the later.

1. Fork this repository (you need to first make an account on GitHub for this)
2. Go to the forked repository and copy the HTTPS link for cloning this repo (the link is present under the ```Code``` button)
3. ```cd``` into a directory where you'd like to clone this project
> [!NOTE]
> At this stage, you can use a virtual environment if you wish.
4. Run ```git clone https://github.com/USERNAME/igem-2024-website.git``` where ```USERNAME``` is your own GitHub username.
5. Run ```ls``` to check if the cloning is successful or not. You should see the following file structure:

```
├───notebook
│   ├───migrations
│   │   ├───__init__.py
│   ├───static
│   │   ├───notebook
│   │   │   └───base.css
│   ├───templates
│   │   ├───notebook
│   │   │   ├───index.html
│   │   │   └───layout.html
│   ├───__init__.py
│   ├───admin.py
│   ├───apps.py
│   ├───models.py
│   ├───tests.py
│   ├───urls.py
│   └───views.py
├───static
│   ├───common
│   │   └───common.css
│   ├───font
│   │   ├───dmSans.tff
│   │   ├───dmSansIt.tff
│   │   ├───grandstander.tff
│   │   └───grandstanderIt.tff
├───templates
│   ├───common
│   │   └───layout.html
├───wiki
│   ├───__init__.py
│   ├───asgi.py
│   ├───settings.py
│   ├───urls.py
│   └───wsgi.py
├───.gitignore
├───manage.py
├───README.md
└───requirements.py
```

6. If the files you've received match the above structure, then the cloning has been done correctly.
7. Now, you should start a python development environment using ```python -m venv .venv```. You should first run ```pip3 install virtualenv``` to install virtualenv and create virtual environment. Then run ```.venv/Scripts/activate``` to activate the virtual environment. (After you are done, just run ```deactivate``` to exit the virtual environment)

> [!IMPORTANT]
> If you are in Windows and have not used python virtual environment before, chances are you won't be able to run the above command. To fix this, open PowerShell as an administrator and run ```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```. This will allow running of scripts (which has been digitally signed by a trusted publisher) on your computer.

8. Run ```pip3 install -r requirements.txt``` to install all the dependencies required.
9. Once done, run ```python manage.py makemigrations notebook``` followed by ```python manage.py migrate```. This will set up the database for the website.
10. Now run ```python manage.py runserver``` to start the development server if you want to see the website. Then go to ```http://127.0.0.1:8000/notebook``` to visit the notebook page.

If everything works fine, the installation is successful.

## The file structure

- The root directory
    - The ```notebook``` folder contains the files for the notebook app. 
    - The ```static``` folder contains the static files used by all the pages in the website (like fonts, common css, common JS, etc).
    - The ```templates``` folder contains ```.html``` files used by all the sites. It is the basic layout of the website.
    - The ```wiki``` folder contains all the configuration files of the django project.
    - ```.gitignore``` contains names of all the folders that we don't want git to push to the online repo.
    - ```manage.py``` is a utility file for any django project. It contains various housekeeping commands like ```runserver``` as used before.
    - README.md contains the markdown file for this text.
    -  ```requirements.txt``` lists all the dependencies required for this project.

## Contributing

Again, I would thank you for thinking of contributing to the developement of the website. This website would not be a success without your help. Please follow the steps to contribute to this project:

> [!IMPORTANT]
> You are recommened to read the README on the ```dev``` branch to know about the latest files. The ```main``` branch is for the most stable and production ready version of the code.

1. After you ```git clone``` this repository, switch to the ```dev``` branch using ```git checkout dev``` to see the latest updates to the codebase. Then, run ```git checkout -b USERNAME``` to create a new branch, where USERNAME is your GitHub username.

> [!IMPORTANT]
> You must follow step 1.

2. Now, move to that branch using ```git branch USERNAME```.
4. Write and edit the code.
5. After you are done, run ```git add .``` to add any new files that you might have created. You can skip this step if you haven't added anything new.
6. Run ```git commit -am "COMMIT MESSAGE"``` where COMMIT MESSAGE should mention what you modified.
7. Now this step is a bit of a trick. By default, you won't be able to push from this branch directly. But run ```git push```. You should see an error message and that message contains the correct command to use to push to the online repository. Copy, paste and run that command to push your changes.
8. Open the repository from your browser. Chances are, you should see a banner asking you to create a Pull Request. If not, manually create a pull request by navigating to the appropriate tab. Make sure to request merge into the ```dev``` branch and not the ```main``` branch. Fill in the necessary details and create the request. If everything's alright, I will accept the request.
