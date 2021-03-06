"""
GameGUI is the all-encompassing object to represent the GUI window instance. A GameGUI may have multiple Layouts, so
there is no need to create new instances of GameGUI when a new screen layout is required (menu screen, main playing
screen, win screen, etc.).
"""


class GameGUI:
    """ GameGUI is the all-encompassing object to represent the GUI window instance. See docs at top of file. """

    ''' ========== Constructor ========== '''

    def __init__(self, layouts=None, active_layout=None):

        if layouts is None:
            layouts = set()

        # List of Layout objects representing win screen, play screen, end screen, etc.
        self.layouts = layouts

        # Whichever screen should be draw()n in the pygame window
        self.active_layout = active_layout

    ''' ========== Static Methods ========== '''

    @staticmethod
    def get_active_screen(game_gui):
        """ :return active layout """
        return game_gui.active_layout

    ''' ========== Instance Methods ========== '''

    def update_active_screen(self, new_layout):
        """ :param new_layout to be made the active layout """
        if new_layout not in self.layouts:
            self.layouts.add(new_layout)

        self.active_layout = new_layout

    def handle_click(self, x_click_loc, y_click_loc):
        """ Handle the click in the context of the active_layout. """
        return self.active_layout.handle_click(x_click_loc, y_click_loc)

    def draw(self, screen):
        """ Draw the active_layout. """
        self.active_layout.draw(screen)
