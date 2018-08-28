import sys
from logging import config, getLogger

from PyQt5.QtWidgets import QApplication
from apscheduler.schedulers.qt import QtScheduler

from settings import HOST, PORT, EMAIL, PASSWORD, ID, AGENT
from src.mainwindow import MainWindow, MainWindowModel, MainWindowPresenter
from src.dialog import UserDialog, UserDialogModel, UserDialogPresenter
from src.dialog import QueryDialog, QueryDialogModel, QueryDialogPresenter
from src.scheduler import TaskScheduler
from src.electronicmail import EmailSender, EmailClient
from src.storage import FileStorage, PickleStorageRetriever, PickleStorageSaver
from src.user import UserValidator
from src.reddit import Reddit, RedditQueryListing

from inputfile import UiFile, StorageFile, ConfigFile

def main():

  app = QApplication(sys.argv)
  config.fileConfig(ConfigFile.LOGGING)

  # Initialize views
  window = MainWindow(UiFile.MAIN_WINDOW)
  user_dialog = UserDialog(UiFile.USER_DIALOG)
  query_dialog = QueryDialog(UiFile.QUERY_DIALOG)

  # Initialize model dependencies
  scheduler = TaskScheduler(QtScheduler(logger=getLogger('scheduler')))
  emailer = EmailSender(EmailClient(HOST, PORT, EMAIL, PASSWORD))
  reddit = Reddit(ID, AGENT)
  user_validator = UserValidator()
  user_retriever = PickleStorageRetriever(StorageFile.USER)
  user_saver = PickleStorageSaver(StorageFile.USER)
  user_storage = FileStorage(user_retriever, user_saver)
  query_retriever = PickleStorageRetriever(StorageFile.QUERYLISTING)
  query_saver = PickleStorageSaver(StorageFile.QUERYLISTING)
  query_storage = FileStorage(query_retriever, query_saver)

  # Initialize model
  window_model = MainWindowModel(scheduler, user_storage, query_storage, emailer)
  user_dialog_model = UserDialogModel(scheduler, user_storage, user_validator)
  query_dialog_model = QueryDialogModel(scheduler, query_storage, reddit)

  # Initialize presenters
  window_presenter = MainWindowPresenter(window, window_model)
  user_dialog_presenter = UserDialogPresenter(user_dialog, user_dialog_model)
  query_dialog_presenter = QueryDialogPresenter(query_dialog, query_dialog_model)

  # Connect signals to slots
  window.user_dialog_clicked.connect(user_dialog.show)
  window.query_dialog_clicked.connect(query_dialog.show)
  user_dialog.confirm_clicked.connect(user_dialog_presenter.validate_user_info)
  query_dialog.confirm_clicked.connect(query_dialog_presenter.validate_subreddit)
  scheduler.user_ready.connect(window_presenter.when_user_ready)
  scheduler.query_ready.connect(window_presenter.when_query_ready)
  scheduler.querylisting_available.connect(window_presenter.with_querylisting)
  scheduler.query_available.connect(window_presenter.with_query)

  window.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
