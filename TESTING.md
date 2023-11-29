# **Testing**

## **Unit Testing**

I tested the functionality with unit tests with each app, they all pass.

- ![bookclubevents tests](bookclubevents/tests.py)

- ![bookofthemonth tests](bookofthemonth/tests.py)

- ![comments tests](comments/tests.py)

- ![followers tests](followers/tests.py)

- ![likes tests](likes/tests.py)

- ![posts tests](posts/tests.py)

- ![profiles tests](profiles/tests.py)

- ![responses tests](responses/tests.py)

## **Code Validation**

- Using the [CI Python Linter](https://pep8ci.herokuapp.com/) I tested all the relevant .py files and they are all passing without error.

# **Bugs**

# **Fixed and Unfixed Bugs**

- One of the bugs was a missing backslash that was keeping the signin form to render properly. - Fixed
- My bookofthemonth frontend has problems rendering the content from the backend, I suspect it's because of the IsAdminOrReadOnlyOrUserRetrieve instead of just IsAuthenticatedOrReadOnly, but I'm not sure since it worked in the unit tests. - future feature to be fixed
- The book club events in the frontend also don't render properly I couldn't figure out why. There is one place in the BookClubEventsPage where the prop should be ...bookclubevent, because I'm mapping through the props, but then the page doesn't render at all. So I left it as ...BookClubEvents and it renders somewhat - future feature to be fixed.
- The date and time formatting are not corresponding on the Book Club Event - future feature to be fixed

