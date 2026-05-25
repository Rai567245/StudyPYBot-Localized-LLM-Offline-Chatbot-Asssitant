import tkinter as tk
from app.controller import ChatController
from gui.main_window import StudyPYGUI

def main():
    # Initialize the controller first (this will load the model)
    # Note: Loading may take 1-2 minutes on your i5 CPU
    controller = ChatController()
    
    root = tk.Tk()
    app = StudyPYGUI(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()