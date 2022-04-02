from gui import *
from controller import Controller
from repository import Repository
from ui import UI

if __name__ == "__main__":
    repository = Repository()
    controller = Controller(repository)
    ui = UI(controller)
    ui.start()
