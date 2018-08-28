#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MainWindowPresenter:

  def __init__(self, main_window_view, main_window_model):
    self.main_window_view = main_window_view
    self.main_window_model = main_window_model

  def user_ready(self):
    if main_window_model.user_exist():
      query_listing = main_window_model.get_query_listing()
      main_window_view.get_query_listing()
      main_window_model.enable_query_dialog_button()

  def with_query_listing(self, query_listing):
    main_window_view.populate_listing(query_listing)
    main_window_view.set_query_count(query_listing.count)
