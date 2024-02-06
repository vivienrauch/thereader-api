# Welcome to The Reader!

![amiresponsive](docs/amiresponsive.png)

### **Backend**

Live site: https://the-reader-2a70cde2ef2e.herokuapp.com
Repo: https://github.com/vivienrauch/thereader-api

### **Frontend**
Live site: https://the-reader-react-1715725e4d83.herokuapp.com/
Repo: https://github.com/vivienrauch/thereader

# **Objective**

My objective with this community app was to bring those who have reading as a hobby closer together;
as well as having a functional app that can authenticate, make it possible for users to follow each other, make up their own profile, be able to modify it, have some custom features like the book of the month or the book club events and the event response.
it was important throughout the working process to implement security in the application, making sure that only users that meant to access a certain functionality can do so and they get a clear indication of that.

## **User Stories**

- [Kanban board] (https://github.com/users/vivienrauch/projects/8/views/1)
- [User stories] (https://github.com/vivienrauch/thereader-api/issues)

All features detailed are available [here](https://github.com/vivienrauch/thereader/blob/main/README.md).

Testing is available in [TESTING.md](TESTING.md).

# **Deployment**

- Open your Heroku dashboard.
- Click on "New" and choose "Create new app."
- Provide a meaningful name for your app and select the appropriate region.
- Go to the "Settings" tab.
- Click "Reveal Config Vars" to input key-value pairs from your .env file (excluding DEBUG and DEVELOPMENT).
- Add a buildpack by clicking "Add buildpack" and select "python" from the list. Save your changes.
- Navigate to the "Deploy" tab.
- Choose "GitHub - Connect to GitHub" as the deployment method.
- Click "Connect to GitHub" and search for your repository by name.
- Connect to the relevant repository and either enable automatic deploys or manually deploy by clicking "Deploy Branch."
- Access the deployed site by clicking "View."
- You can also find the live site in the environments section of your GitHub repository.