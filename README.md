# python-autodeploy
No Flask local python autodeployer

## Features

Deploys automatically from github every 10min if there is a new commit without using webhooks! 
No stupid flask and ngrok to setup, none of that BULLSHIT. Clean and simple.

## Installation

1. Move into your project directory. <br>
`cd myProject`
2. Download installation file. You will need an internet connection from this point on. <br>
`curl https://raw.githubusercontent.com/FrankWhoee/python-autodeploy/master/install-autodeploy > install-autodeploy`
3. Make the file executable. <br>
`chmod +x install-autodeploy`
4. Install autodeploy <br>
`./install-autodeploy`
5. Create a configuration file<br>
`touch autodeploy.conf`
6. Open your favourite text editor and add the following information to autodeploy.conf:<br>
```
repo: GITHUB_USERNAME/YOUR_PROJECT
run: myProject.py
```
7. Run autodeployment<br>
`./run-autodeploy`

## TODO
- Adding support for other languages!

## Usage

Currently implemented at [Dentaku](https://github.com/vikingsdev/dentaku)
