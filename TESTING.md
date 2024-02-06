# **Testing**

This page includes the backend testing of the Reader application.

## **Unit Testing**

I tested the functionality with unit tests for each app, they all pass.

### **Custom Models**

- [bookclubevents tests](bookclubevents/tests.py)

- [bookofthemonth tests](bookofthemonth/tests.py)

- [responses tests](responses/tests.py)

### **Basic Models**

- [comments tests](comments/tests.py)

- [followers tests](followers/tests.py)

- [likes tests](likes/tests.py)

- [posts tests](posts/tests.py)

- [profiles tests](profiles/tests.py)

### **Frontend**

The frontend testing is available [here](https://github.com/vivienrauch/thereader/blob/main/TESTING.md)

## **Code Validation**

### Python validation using Flake8

- **Book Club Events**

![flake8bce](docs/flake8_booklclubevents.png)

- **Book Of The Month**

![flake8botm](docs/flake8_bookofthemonth.png)

- **Responses**

![flake8responses](docs/flake8_responses.png)

- **Profiles**

![flake8profiles](docs/flake8_profiles.png)

- **Posts**

![flake8posts](docs/flake8_posts.png)

- **Likes**

![flake8likes](docs/flake8_likes.png)

- **Comments**

![flake8comments](docs/flake8_comments.png)

- **Followers**

![flake8followers](docs/flake8_followers.png)

# **Bugs**

- Fixed: One of the bugs was a missing backslash that was keeping the signin form to render properly.

