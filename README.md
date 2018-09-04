# RedditNotifier

## Built with
Reddit API - **Praw 6.0.0** (https://praw.readthedocs.io/en/v6.0.0)

User interface - **PyQt 5.11** (https://www.riverbankcomputing.com/software/pyqt/download5)

Asynchronous programming & task scheduling - **Apscheduler 3.5.3** (https://apscheduler.readthedocs.io) 

Memory persistence - **Pickle 3.7.0** (https://docs.python.org/3/library/pickle.html)

Model-View-Presenter architecture

## Usage

To run:

1. Edit .env file. 
    - Fill in with Praw id + Praw agent acquired through Reddit API website.  
    - Fill in emailer host and port. For example host and port for GMAIL would be 'smtp.gmail.com' and 587, respectively.
    - Fill in the dummy bot email and password you created.
2. Run setup.py
3. Click the email button and enter an email address to receive notifications.
4. Start creating notifications.
