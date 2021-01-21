# Journey Home: A Gravity Based Game

**Authors: Mitchell Krieger, Evan Ricketts**

## How to Play

You are an astronaut whose drifting ship has run out of fuel. As you inexplicably possess the ability to place heavenly objects, your only hope for survival is using the gravitational pull of space things to affect your trajectory and get you home.

Drag the space items you desire from the items tab of the toolbar into space and press go to see if you get to the next leap point (goal), and eventuall get you home. Keep an eye on your lives and the score, and watch out for enemies, black holes, and other baddies.

Your starting trajectory is towards the upper righthand corner of space. You get one freebie by **right clicking** go to see your trajectory from the gravitational pull of objects already in space. Right clicking planets you've dragged out into space will delete them.

## Demo

View a [demo of the game on youtube](https://www.youtube.com/watch?v=EnXRUZDFae4&feature=emb_logo)

## Download and play locally on your computer

If you have Mac OS X 10.7 (Lion) or higher, you can play the game created for the final project by [downloading it here](https://github.com/mitkrieg/Gravity/downloads)

Once downloaded open up the Zip file, and the application should be there. You may need to also download and install XQuartz (a X server window component for macs). Once you open the application it will ask you if you want to install it, if you don’t have it.

## Online Deployment

Still in progress for deployment on Heroku

## Repository Structure
```
├── assets              <- directory containing images, sprites and other assets for graphics
├── old_stuff           <- directory containing outdated pyscripts
├── .gitignore          <- gitignore file
├── Procfile            <- procfile for future heroku deployment
├── README.md           <- Overview of Game Project
├── bar.py              <- Creates Class for the taskbar 
├── goal.py             <- Creates class for the level goal
├── main.py             <- Runs game and contains Game class
├── obstacles.py        <- creates class for obstacles
├── player.py           <- creates class for player
├── layouts.py          <- Py script creating html layouts of Dashboard
├── README.md           <- README for overview of this project
├── requirements.txt    <- requirements for replicating code & heroku future deployment
├── Procfile            <- Procfile for future deployment to Heroku
├── starfield.py        <- Creates Class for the starfield
├── system.py           <- Script for saving and loading game .txt files
├── transitions.py      <- Animations for transitions between screens
└── user_items.py       <- Creates class for items to curve player trajectory
```
