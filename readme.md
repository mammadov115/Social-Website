# Django App Name

## Overview

This Django project includes a feature-rich app that provides various functionalities related to user authentication, social authentication, media file uploads, profile management, many-to-many relationships, asynchronous HTTP requests, activity stream, and more.

## Features

- **User Authentication**
  - Includes login, logout, password change, and password reset views using the Django authentication framework.
  - Customizes templates for login, logout, password change, and password reset views.

- **User Registration**
  - Provides user registration views.
  - Extends the user model with a custom profile model.

- **Media File Uploads**
  - Configures the project to handle media file uploads.
  - Uses the messages framework for user feedback.

- **Custom Authentication Backend**
  - Implements a custom authentication backend for advanced user authentication needs.

- **Email Validation**
  - Prevents users from using an existing email during registration.

- **Social Authentication**
  - Integrates Python Social Auth to enable authentication using Facebook, Twitter, and Google accounts.
  - Creates profiles for users who register with social authentication.

- **Many-to-Many Relationships**
  - Demonstrates many-to-many relationships in Django models.
  - Utilizes an intermediary model for a more complex relationship.

- **Custom Forms**
  - Customizes form behavior to suit specific requirements.

- **JavaScript Integration**
  - Uses JavaScript with Django to create interactive features.
  - Implements a JavaScript bookmarklet.

- **Image Thumbnail Generation**
  - Utilizes easy-thumbnails to generate image thumbnails.

- **Asynchronous HTTP Requests**
  - Implements asynchronous HTTP requests with JavaScript and Django.

- **Infinite Scroll Pagination**
  - Builds an infinite scroll pagination feature for a smoother user experience.

- **Follow System**
  - Implements a follow system to allow users to follow other users.

- **Activity Stream**
  - Creates an activity stream application to display user activities.

- **Generic Relations**
  - Adds generic relations to models for more flexible database design.

- **Optimized QuerySets**
  - Optimizes QuerySets for related objects to improve performance.

- **Denormalization with Signals**
  - Uses Django signals for denormalizing counts in the database.

- **Debugging with Django Debug Toolbar**
  - Integrates Django Debug Toolbar to obtain relevant debug information.

- **Counting Image Views with Redis**
  - Uses Redis to count image views.

- **Ranking Most Viewed Images**
  - Builds a ranking of the most viewed images using Redis.

## Installation and Setup

1. Clone the repository:
```
git clone https://github.com/mammadov115/Social-Website.git
cd Social-Website
```

2. Create and activate a virtual environment:
```
python -m venv venv source venv/bin/activate 
#On Windows: 
venv\Scripts\activate
```

3. Install the required packages:
`pip install -r requirements.txt`


4. Apply database migrations:
`python manage.py migrate`


5. Run the development server:
`python manage.py runserver`


6. Access the app at `http://127.0.0.1:8000/`.

## Support

If you have any questions, issues, or suggestions, please feel free to reach out to [me](https://api.whatsapp.com/send?phone=994506222692).

### Thanks
