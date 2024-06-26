# iGEM IISc 2024 Website
First, I would like to thank you for visiting this repo. This repository contains all the files for the iGEM IISc 2024 website.

## Installation for Development

> [!NOTE]
> If you are using a UNIX based OS (like macOS or linux), use ```python3``` instead of ```python``` in all the commands where you have to write the later.

1. ```cd``` into a directory where you'd like to clone this project

> [!NOTE]
> At this stage, you can use a virtual environment if you wish.

2. Run ```git clone https://github.com/nathaishik/igem-2024-website.git``` to clone the repository.
3. Run ```ls``` to check if the cloning is successful or not. You should see the following file structure:

```
.
├── docs
│   ├── note
│   │   ├── 2ad698b6-0fb8-4280-aa04-5797c13df514.html
│   │   └── 408194b4-102a-4453-98f0-59fc6b3dc6f3.html
│   ├── notebook
│   │   ├── HDLEAF.html
│   │   ├── HDMIST.html
│   │   └── HDSAND.html
│   ├── static
│   │   ├── common
│   │   │   ├── codemirror
│   │   │   │   ├── active-line.js
│   │   │   │   ├── ayu-mirage.css
│   │   │   │   ├── closebrackets.js
│   │   │   │   ├── codemirror.css
│   │   │   │   ├── codemirror.js
│   │   │   │   ├── duotone-light.css
│   │   │   │   ├── markdown.js
│   │   │   │   ├── matchbrackets.js
│   │   │   │   └── mathematica.js
│   │   │   ├── common.css
│   │   │   ├── deletion_warning.js
│   │   │   ├── mathjax.js
│   │   │   ├── pri-nav-toggle.js
│   │   │   ├── sec-nav.js
│   │   │   └── tex-svg.js
│   │   ├── font
│   │   │   ├── ibm_plex_sans
│   │   │   │   ├── IBMPlexSans-Italic.ttf
│   │   │   │   ├── IBMPlexSans-Light.ttf
│   │   │   │   ├── IBMPlexSans-LightItalic.ttf
│   │   │   │   ├── IBMPlexSans-Medium.ttf
│   │   │   │   ├── IBMPlexSans-MediumItalic.ttf
│   │   │   │   ├── IBMPlexSans-Regular.ttf
│   │   │   │   ├── IBMPlexSans-SemiBold.ttf
│   │   │   │   └── IBMPlexSans-SemiBoldItalic.ttf
│   │   │   ├── Bespoke.ttf
│   │   │   ├── BespokeItalic.ttf
│   │   │   ├── JetBrainsMono-Italic.ttf
│   │   │   └── JetBrainsMono.ttf
│   │   ├── notebook
│   │   │   ├── account.css
│   │   │   ├── admin.css
│   │   │   ├── base.css
│   │   │   ├── code-highlight.css
│   │   │   ├── manage_note.css
│   │   │   ├── markdown.css
│   │   │   ├── markdown.js
│   │   │   ├── note.css
│   │   │   ├── note_form.js
│   │   │   ├── sec-nav-toggle.js
│   │   │   └── session.css
│   │   ├── MaterialSymbolsRounded.ttf
│   │   └── MaterialSymbolsRounded.woff2
│   └── index.html
├── notebook
│   ├── static
│   │   └── notebook
│   │       ├── account.css
│   │       ├── admin.css
│   │       ├── base.css
│   │       ├── code-highlight.css
│   │       ├── manage_note.css
│   │       ├── markdown.css
│   │       ├── markdown.js
│   │       ├── note.css
│   │       ├── note_form.js
│   │       ├── sec-nav-toggle.js
│   │       └── session.css
│   ├── templates
│   │   └── notebook
│   │       ├── account.html
│   │       ├── admin.html
│   │       ├── dash_notes.html
│   │       ├── dashboard.html
│   │       ├── docs.html
│   │       ├── index.html
│   │       ├── layout.html
│   │       ├── login.html
│   │       ├── manage_note.html
│   │       ├── note.html
│   │       ├── note_form.html
│   │       ├── notebook.html
│   │       ├── notelist.html
│   │       ├── register.html
│   │       ├── team.html
│   │       └── teams.html
│   ├── test_files
│   │   ├── test.txt
│   │   └── test1.txt
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── urls.py
│   ├── urls_static.py
│   └── views.py
├── static
│   ├── common
│   │   ├── codemirror
│   │   │   ├── active-line.js
│   │   │   ├── ayu-mirage.css
│   │   │   ├── closebrackets.js
│   │   │   ├── codemirror.css
│   │   │   ├── codemirror.js
│   │   │   ├── duotone-light.css
│   │   │   ├── markdown.js
│   │   │   ├── matchbrackets.js
│   │   │   └── mathematica.js
│   │   ├── common.css
│   │   ├── deletion_warning.js
│   │   ├── errors.css
│   │   ├── mathjax.js
│   │   ├── pri-nav-toggle.js
│   │   ├── sec-nav.js
│   │   └── tex-svg.js
│   ├── font
│   │   ├── ibm_plex_sans
│   │   │   ├── IBMPlexSans-Italic.ttf
│   │   │   ├── IBMPlexSans-Light.ttf
│   │   │   ├── IBMPlexSans-LightItalic.ttf
│   │   │   ├── IBMPlexSans-Medium.ttf
│   │   │   ├── IBMPlexSans-MediumItalic.ttf
│   │   │   ├── IBMPlexSans-Regular.ttf
│   │   │   ├── IBMPlexSans-SemiBold.ttf
│   │   │   └── IBMPlexSans-SemiBoldItalic.ttf
│   │   ├── Bespoke.ttf
│   │   ├── BespokeItalic.ttf
│   │   ├── JetBrainsMono-Italic.ttf
│   │   └── JetBrainsMono.ttf
│   ├── MaterialSymbolsRounded.ttf
│   └── MaterialSymbolsRounded.woff2
├── staticfiles
│   ├── common
│   │   ├── codemirror
│   │   │   ├── active-line.js
│   │   │   ├── ayu-mirage.css
│   │   │   ├── closebrackets.js
│   │   │   ├── codemirror.css
│   │   │   ├── codemirror.js
│   │   │   ├── duotone-light.css
│   │   │   ├── markdown.js
│   │   │   ├── matchbrackets.js
│   │   │   └── mathematica.js
│   │   ├── common.css
│   │   ├── deletion_warning.js
│   │   ├── errors.css
│   │   ├── mathjax.js
│   │   ├── pri-nav-toggle.js
│   │   ├── sec-nav.js
│   │   └── tex-svg.js
│   ├── font
│   │   ├── ibm_plex_sans
│   │   │   ├── IBMPlexSans-Italic.ttf
│   │   │   ├── IBMPlexSans-Light.ttf
│   │   │   ├── IBMPlexSans-LightItalic.ttf
│   │   │   ├── IBMPlexSans-Medium.ttf
│   │   │   ├── IBMPlexSans-MediumItalic.ttf
│   │   │   ├── IBMPlexSans-Regular.ttf
│   │   │   ├── IBMPlexSans-SemiBold.ttf
│   │   │   └── IBMPlexSans-SemiBoldItalic.ttf
│   │   ├── Bespoke.ttf
│   │   ├── BespokeItalic.ttf
│   │   ├── JetBrainsMono-Italic.ttf
│   │   └── JetBrainsMono.ttf
│   ├── notebook
│   │   ├── account.css
│   │   ├── admin.css
│   │   ├── base.css
│   │   ├── code-highlight.css
│   │   ├── manage_note.css
│   │   ├── markdown.css
│   │   ├── markdown.js
│   │   ├── note.css
│   │   ├── note_form.js
│   │   ├── sec-nav-toggle.js
│   │   └── session.css
│   ├── MaterialSymbolsRounded.ttf
│   └── MaterialSymbolsRounded.woff2
├── templates
│   └── common
│       └── layout.html
├── wiki
│   ├── asgi.py
│   ├── settings.py
│   ├── settings_prod.py
│   ├── settings_static.py
│   ├── urls.py
│   ├── urls_prod.py
│   ├── urls_static.py
│   ├── wsgi.py
│   └── wsgi_prod.py
├── Dockerfile
├── README.md
├── __init__.py
├── docker-compose.yml
├── export_static.ps1
├── export_static.sh
├── manage.py
└── requirements.txt
```

> [!NOTE]
> To get the above file tree, use ```tree --dirsfirst -n -I 'node_modules|media|.venv|__pycache__|*.sqlite3|*.json'``` in the bash terminal. If you are in Windows, you can enter bash terminal using the ```bash``` command in PowerShell. You will have to enable virtualisation and WSL for Windows.


6. If the files you've received match the above structure, then the cloning has been done correctly. I am also including the names of the migration files. Make sure you have all of them.
7. Now, you should start a python development environment using ```python -m venv .venv```. You should first run ```pip3 install virtualenv``` to install virtualenv and create virtual environment. Then run ```.venv/Scripts/activate``` to activate the virtual environment. (After you are done editing or testing the code, just run ```deactivate``` to exit the virtual environment)

> [!IMPORTANT]
> If you are in Windows and have not used python virtual environment before, chances are you won't be able to run the above command. To fix this, open PowerShell as an administrator and run ```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```. This will allow running of scripts (which has been digitally signed by a trusted publisher) on your computer.

8. Run ```pip3 install -r requirements.txt``` to install all the dependencies required.
9. Run ```python manage.py makemigrations notebook``` followed by ```python manage.py migrate```. This will set up the database for the website.
10. Now run ```python manage.py runserver``` to start the development server if you want to see the website. Then go to ```http://127.0.0.1:8000``` to visit the notebook page.

If everything works fine, the installation is successful. If you wish to make Notes on the notebook app, you first need to create an user.

11. Shut the server down and run ```python manage.py createsuperuser```. Give a username and a passoword. You may skip the email ID part by pressing ```Enter``` when prompted for the email ID.
12. Once the superuser is created, restart the server and go to ```/admin```. Login using the superuser. Then go to Users. Click on the username of your superuser. Scroll down and enable the verified option. You should also assign a Role to the user. You may complete the rest of your profile if you wish but it is not mandatory (as of now). Then create some Departments and add the user in the member list of a Department.

> [!IMPORTANT]
> The Notes app might be a big buggy right now.

13. Log out and go to ```/login```. Login with the superuser account. Go to ```/new``` and create a note.
14. You can also use another account to create the notes. Go to ```/signup``` and creating an account. Then logout and go to ```/admin``` and signup with the superuser account to verify the new user. Assign them a Department and a position and save. Then login again with the new user and go to ```/new``` to create a note.


## The file structure

- The files inside root directory:
    - The ```notebook``` folder contains the files for the notebook app. 
    - The ```static``` folder contains the static files used by all the pages in the website (like fonts, common css, common JS, etc).
    - The ```templates``` folder contains ```.html``` files used by all the sites. It is the basic layout of the website.
    - The ```wiki``` folder contains all the configuration files of the django project.
    - The ```docs``` folder contains the static site.
    - ```.gitignore``` contains names of all the folders that we don't want git to push to the online repo.
    - ```manage.py``` is a utility file for any django project. It contains various housekeeping commands like ```runserver``` as used before.
    - ```README.md``` contains the markdown file for this text.
    - ```requirements.txt``` lists all the dependencies required for this project.

## Contributing

Please follow the steps to contribute to this project:
1. After you ```git clone``` the forked repository (proper forking described in step 1 of [Installation for Development](https://github.com/nathaishik/igem-2024-website/tree/dev?tab=readme-ov-file#installation-for-development)), switch to the 'dev' branch using ```git checkout dev```. Then, run ```git checkout -b USERNAME``` to create a branch.

> [!IMPORTANT]
> You must follow step 1.

2. Now, move to that branch using ```git checkout USERNAME```.
4. Write and edit the code.
5. Run ```python manage.py test``` to test your code. If you feel the need to introduce any new test for the feature that you've developed, write the test in the appropriate test file. Make sure that your code passes all tests.
6. After you are done, run ```git add .``` to add any new files that you might have created. You can skip this step if you haven't added anything new.
7. Run ```git commit -am "COMMIT MESSAGE"``` where COMMIT MESSAGE should mention what you modified.
8. Now this step is a bit of a trick. By default, you won't be able to push from this branch directly. But run ```git push```. You should see an error message and that message contains the correct command to use to push to the online repository. Copy, paste and run that command to push your changes.
9. Open the repository from your browser. Chances are, you should see a banner asking you to create a Pull Request. If not, manually create a pull request by navigating to the appropriate tab. Fill in the necessary details. Tt is important that you ask for merging in the ```dev``` branch. Then create the request. If everything's alright, I will accept the request.

## Generating Static Site

> [!WARNING]
> The notes you've made will be converted into static file and will be available to everyone once the static site is deployed. So, avoid this unless absolutely necessary.

1. Run ```python manage.py distill-local --settings=wiki.settings_static``` and continue with ```YES``` to generate the static site in the ```docs``` directory.
2. Then run ```python manage.py collectstatic --settings=wiki.settings_static``` to generate the ```static``` folder in the ```docs``` directory.
3. Now move the files/folders inside ```./docs/igem-2024-website``` to ```./docs```.
4. Commit and push your changes.
