#  MS3 "My home office"

My home office is a comparison/sharing site for visuals of users home office's/workspce to include links to products for purchase

![Am I responsive](https://github.com/David-A-Ray/MS3-My-home-office/blob/master/docs/images/responsive.png)

## UX

### User Stories

As a user I would like to:
* Be able to upload my workspace
* Be able to view others worpspace and details of products
* View the most liked work spaces
* Edit and delete my own workspace
* Be able to easily log in and out of the app

### Strategy

The goal is to build a simple to navigate site with a welcome Modal with options that then guides the user through the site and back to the start when choosing to exit.

### Scope

For users there needs to be an explanation of what the aim of the site is, an easy to navigate menu and simple forms to add/edit or delete the work space.

### Structure

To keep navigation as self explanatory as possible the structure of the site should create a natural flow as follows.
* Home page will display all users workspaces, with a nav bar to allow users to navigate/upload their own space.
* Each users space will have an option to expand and view product details.
* Log in log out features.

### Surface

Quite a clean simple look to allow ease of navigation.

## Technologies

### Languages
* [HTML5](https://en.wikipedia.org/wiki/HTML5) - provides content and structure of the site.
* [CSS3](https://en.wikipedia.org/wiki/CSS) - adds styling.
* [JAVASCRIPT](https://en.wikipedia.org/wiki/JavaScript) - built in bootstrap min js.
* [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) - used for interaction on backend.
* [jinja](https://jinja.palletsprojects.com/en/3.0.x/) - used for shortcuts.


### Frameworks 
* [Bootstrap V4.5.2](https://getbootstrap.com/docs/4.5/getting-started/introduction/) - provides the bulk of responsive layout.
* [jquery](https://jquery.com/) - used on dropdown menu.
* [GitHub](https://github.com/) - GitHub has been used to manage version control and push content to repo.
* [GitPod](https://www.gitpod.io/) - used as the IDE for building the site.
* [mongodb](https://www.mongodb.com/) - functional backend database.
* [heroku](https://en.wikipedia.org/wiki/Heroku) - heroku runs the app.
* [Google FONTS](https://fonts.google.com/) - imported for 2 font varieties.
* [Balsamiq wireframes](https://balsamiq.com/wireframes/?gclid=CjwKCAiA17P9BRB2EiwAMvwNyJFLuwdZxoUMDd-KJV_EtTEdllWFxfMzYAxyyiN7yGBDdFV0IoCHQRoCe0EQAvD_BwE) - used for all wireframes.
* [TinyPNG](https://tinypng.com/) - used to compress initial image files.
* [CSS Autoprefixer](https://autoprefixer.github.io/) - CSS was checked for browser compatibility. 
* [AmIResponsive](http://ami.responsivedesign.is/) - used for initial responsive display and testing.

## Features
* Log in register

* Upload workspace:
    * options to load images and details

* Home Page:
    * display all work spaces with option to view more detail and like

* My workspace:
    * displays users image and details with options to edit and delete.

* Log out

## Features left to implement
* Like feature - I ran out of time, left the like button in place but didn't impliment the JS or backend.
* Search feature for popular products - did split the product uploads into a seperate cluster but struggled to get the forms to work so endedup restructuring back to as is.

## Testing

### Pre-Deployment
Throughout development the site was previewed locally and tested as elements were added. The layout waschecked for responsiveness using developer tools. 

### Post-Deployment
* Deployed site was shared with friends and family.
    * Ran the CSS through Autoprefixer to fix issues.

### Final checks on code
* Code validation
    * W3 HTML validator.
    * W3 CSS validator.

### User stories Testing
* Have the option to signup to app.
    * Complete
* Ability to upload my workpsace
    * Complete
* Ability to edit my workspace
    * Complete
* Ability to delete my workspace.
    * Complete
* Ability to delete my workspace.
    * Complete
* Ability to delete my workspace.
    * Complete
* Option to view other workspaces and details.
    * Complete

All user stories have been fullfilled from original targets. 

## Deployment
### MongoDb

- mongodb was used as the project database.

- I followed the following steps to set it up.
	- signed up to Mongodb and created a shared cluster
	- selected default AWS cloud provider
	- selected Ireland region
	- selected m0 cluster tier
	- chose name for cluster
	- once cluster was created I clicked 'CONNECT' button
	- Selected 'connect your application'
	- selected Python / 3.6 or later as my driver
	- copied the connection string for use in my application
	- set password / cluster name / collection name as enviuronmental variables to connect to my DB within flask
	- used Flask-MongoEngine to interact with my DB within the app

### Git Clone
* To clone my repository follow these steps:
1. Go to my GitHub repository - https://github.com/David-A-Ray/MS2-Whats-your-poison-memory-game
2. Click on the CODE drop down button.
3. With the HTTPS option selected click on the clipboard icon.
4. Open your IDE.
5. Create a directory you want the clone to be named as.
6. Type git clone in your terminal followed by pasting the link you've copied.
7. Hit enter and your local clone will be created.

### Code
Some of the code for the site was taken or influenced by the following sources:
* stackoverflow.com 

### Acknowledgments
I would like to thank my mentor Reuben Ferrante for advice and help with troubleshooting.