#! /usr/bin/env python3
from collections import OrderedDict
import datetime
import sys
import os

from peewee import *


db = SqliteDatabase('diary.db')

class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)

def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
      clear()
      print("Enter 'q' to quit")

      for key, value in menu.items():
        print('{}) {}'.format(key, value.__doc__))

      choice = input("Action > ").lower().strip()

      if choice in menu:
          clear()
          menu[choice]()

def add_entry():
    """Add an entry."""
    print("Enter your entry, press ctrl+d when finished")
    data = sys.stdin.read().strip()

    if data:
      if input('Save entry? [Y/N]').lower() != 'n':
        Entry.create(content=data)
        print('Saved successfully \n')
      else:
        print('Entry was crumpled and thrown away. \n')

def view_entries(search_query=None):
    """View previous entries."""
    # A - weekday, B - Month, d - Day, Y - Year, I - Hour , M - Minutes, p- AM/PM
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
      entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
      timestamp = entry.timestamp.strftime('%A %B %d, %Y %I %M%p')
      clear()
      print(timestamp)
      print('='*len(timestamp))
      print('\n \n' + '='*len(timestamp))
      print(entry.content + '\n')
      print('N) Next Entry')
      print('D) Delete Entry')
      print('q) return to main menu')
      next_action = input('Action > [N/D/q]) ').lower().strip()

      if next_action == 'q':
        print('\n')
        break
      elif next_action == 'd':
        delete_entry(entry)

def search_entries():
  """Searches entries for a string """
  view_entries(input('Search Query > '))

def delete_entry(entry):
  """Delete a diary entry."""
  if input("Are you sure? [Y/N]").lower() == 'y':
    entry.delete_instance()
    print("Entry Deleted. \n")

def clear():
  os.system('cls' if os.name == 'nt' else 'clear')


menu = OrderedDict([
    ('a' , add_entry),
    ('v', view_entries),
    ('s', search_entries)
  ])


if __name__ == '__main__':
    initialize()
    menu_loop()

  
