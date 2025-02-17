# Mikai Somerville, msom375, 908905231 - AssCool.py

# Import Tkinter for the GUI
from tkinter import *
from tkinter.font import *

# The backend of the application.
class GameBoard:
    # Create the GameBoard object based on it's size. Each object has a size,
    # size number of columns and points for both player and computer.
    def __init__(self, size):
        self.size = size
        self.num_disks = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] * 2

    # Resets the board info to the initial values
    def reset_board(self):
        self.num_disks = [0] * self.size
        self.items = [[0] * self.size for i in range(self.size)]
        self.points = [0] * 2

    # Returns the number of free positions in the given column
    def num_free_positions_in_column(self, column):
        return self.size - self.num_disks[column]

    # Returns whether or not every column is full and the game is over.
    def is_game_over(self):
        for column_index in range(self.size):
            if self.num_disks[column_index] != self.size:
                # If there are less disks in a column than the size of the
                # column, then the game cannot be finished, so return False.
                return False
        # If every column is full, then the game must be over.
        return True

    # # If selected column is not full, add the disk that corresponds to the
    # selected player and update score.
    def add(self, column_index, player):
        if self.num_disks[column_index] == self.size:
            # If the column is full, then disk cannot be added, return false.
            return False
        else:
            # Find the row and set the slot to become the given player, update
            # the points based on this move.
            available_row_index = self.num_disks[column_index]
            self.items[column_index][available_row_index] = player
            self.num_disks[column_index] += 1
            new_points = self.num_new_points(column_index, available_row_index, player)
            self.points[player - 1] += new_points
            return True

    # If the game os not over, use a simple algorithm to determine where the AI
    # should make their move, and then make this move. Returns a boolean
    # representing whether the move able to be taken and the index of the 
    # column where the AI took their move.
    def add_ai(self):
        ai_added = not self.is_game_over()
        if ai_added:
            (best_column, max_points) = self.column_resulting_in_max_points(2)
            if max_points > 0:
                ai_column = best_column
            else:
                # if no move adds new points choose move which minimises points opponent player gets
                (best_column, max_points) = self.column_resulting_in_max_points(1)
                if max_points > 0:
                    ai_column = best_column
                else:
                    # if no opponent move creates new points then choose column as close to middle as possible
                    ai_column = self.free_slots_as_close_to_middle_as_possible()[0]
            self.add(ai_column, 2)
            return ai_added, ai_column
        else:
            return False, self.size + 1

    # Calculate the number of new points that are added when a disk is added to
    # the specified column and row by the given player.
    def num_new_points(self, column_index, row_index, player):
        current_points = 0
        old_points = 0
        # Calculate the number of points in the horizontal direction.
        horizontal_consecutive = 0
        horizontal_consecutive_without = 0
        # Loop through each column at the given row.
        for current_column_index in range(self.size):
            if self.items[current_column_index][row_index] == player:
                # If slot is occupied by player, increment consecutive counts.
                if current_column_index == column_index:
                    # If slot is in the given row, ignore this slot to consider
                    # the points before disk is added in current slot.
                    horizontal_consecutive_without = 0
                else:
                    horizontal_consecutive_without += 1
                horizontal_consecutive += 1
                # If there is four in a row or more add to points.
                if horizontal_consecutive >= 4:
                    current_points += 1
                if horizontal_consecutive_without >= 4:
                    old_points += 1
            else:
                # If slot is not occupied by the player, reset the consecutive
                # counts.
                horizontal_consecutive = 0
                horizontal_consecutive_without = 0
        
        # Calculate number of points in the vertical direction.
        vertical_consecutive = 0
        vertical_consecutive_without = 0
        # Loop through each row in the given column
        for current_row_index in range(self.size):
            if self.items[column_index][current_row_index] == player:
                # If slot is occupied by player, increment consecutive counts.
                if current_row_index == row_index:
                    # If slot is in the given column, ignore this slot to consider
                    # the points before disk is added in current slot.
                    vertical_consecutive_without = 0
                else:
                    vertical_consecutive_without += 1
                vertical_consecutive += 1
                # If there is four in a row or more add to points.
                if vertical_consecutive >= 4:
                    current_points += 1
                if vertical_consecutive_without >= 4:
                    old_points += 1
            else:
                # If slot is not occupied by the player, reset the consecutive
                # counts.
                vertical_consecutive = 0
                vertical_consecutive_without = 0
        
        # Navigate to the bottom left point in the positive diagonal.
        current_column = column_index
        current_row = row_index
        while current_column > 0 and current_row > 0:
            current_column -= 1
            current_row -= 1
        # Calculate number of points in the positive diagonal direction.
        positive_diagonal_consecutive = 0
        positive_diagonal_consecutive_without = 0
        # Loop until the top right of the diagonal is reached.
        while current_column < self.size and current_row < self.size:
            if self.items[current_column][current_row] == player:
                # If slot is occupied by player, increment consecutive counts.
                if current_row == row_index and current_column == column_index:
                    # If slot is the given slot, ignore this slot to consider 
                    # the points before disk is added in current slot.
                    positive_diagonal_consecutive_without = 0
                else:
                    positive_diagonal_consecutive_without += 1
                positive_diagonal_consecutive += 1
                # If there is four in a row or more add to points.
                if positive_diagonal_consecutive >= 4:
                    current_points += 1
                if positive_diagonal_consecutive_without >= 4:
                    old_points += 1
            else:
                # If slot is not occupied by the player, reset the consecutive
                # counts.
                positive_diagonal_consecutive = 0
                positive_diagonal_consecutive_without = 0
            # Move slot up the diagonal towards the top right.
            current_column += 1
            current_row += 1
        
        # Navigate to the bottom right point in the negative diagonal.
        current_column = column_index
        current_row = row_index
        while current_column < self.size - 1 and current_row > 0:
            current_column += 1
            current_row -= 1
        # Calculate number of points in the negative diagonal direction.
        negative_diagonal_consecutive = 0
        negative_diagonal_consecutive_without = 0
        # Loop until the top left of the diagonal is reached.
        while current_column >= 0 and current_row < self.size:
            if self.items[current_column][current_row] == player:
                # If slot is occupied by player, increment consecutive counts.
                if current_row == row_index and current_column == column_index:
                    # If slot is the given slot, ignore this slot to consider 
                    # the points before disk is added in current slot.
                    negative_diagonal_consecutive_without = 0
                else:
                    negative_diagonal_consecutive_without += 1
                negative_diagonal_consecutive += 1
                # If there is four in a row or more add to points.
                if negative_diagonal_consecutive >= 4:
                    current_points += 1
                if negative_diagonal_consecutive_without >= 4:
                    old_points += 1
            else:
                # If slot is not occupied by the player, reset the consecutive
                # counts.
                negative_diagonal_consecutive = 0
                negative_diagonal_consecutive_without = 0
            # Move slot down the diagonal towards the top left.
            current_column -= 1
            current_row += 1
        
        # Find the difference in points between when disk is or isn't added.
        new_points = current_points - old_points
        return new_points

    # Find all of the columns that are not full and order these by distance to
    # the center column, with those equally far from the center ordered left to
    # right.
    def free_slots_as_close_to_middle_as_possible(self):
        # Filter columns to get a list of non-full columns
        available_columns = [column_index for column_index in range(self.size) if self.num_disks[column_index] != self.size]
        middle_column = (self.size - 1) / 2
        # Perform a bubble sort
        for end_index in range(len(available_columns), -1, -1):
            for column_index in range(1, end_index):
                distance_left = abs(available_columns[column_index - 1] - middle_column)
                distance_right = abs(available_columns[column_index] - middle_column)
                if distance_left > distance_right:
                    available_columns[column_index], available_columns[column_index - 1] = available_columns[column_index - 1], available_columns[column_index]
                elif distance_left == distance_right:
                    left_column = available_columns[column_index - 1]
                    right_column = available_columns[column_index]
                    if left_column > right_column:
                        available_columns[column_index], available_columns[column_index - 1] = available_columns[column_index - 1], available_columns[column_index]
        return available_columns

    # Returns a tuple containing the index of the column which gives the
    # specified player a maximum number of points and the number of points this
    # move would earn them.
    def column_resulting_in_max_points(self, player):
        available_columns = self.free_slots_as_close_to_middle_as_possible()
        points_dictionary = {column:0 for column in available_columns}
        # Find the points that would be gained by adding to each column.
        for column in points_dictionary.keys():
            row = self.num_disks[column]
            self.items[column][row] = player
            points_dictionary[column] = self.num_new_points(column, row, player)
            self.items[column][row] = 0
        max_slot_and_points = [available_columns[0], 0]
        # Find the column that results in the largest points gain.
        for column, points in points_dictionary.items():
            if points > max_slot_and_points[1]:
                max_slot_and_points = [column, points]
        return tuple(max_slot_and_points)

    # Returns a boolean representing whether the given column is full
    def column_is_full(self, column_index):
        return self.num_disks[column_index] == self.size

    # Returns the number of points for a given player
    def get_points(self, player):
        return self.points[player]

    # Returns the index of the next row where a move can be taken in a given
    # column.
    def get_available_row(self, column_index):
        return self.num_disks[column_index] - 1


# The frontend of the application.
class Frontend:
    # Initialises the frontend, creating the window and a canvas in the window,
    # sets all of the contents of the canvas to None.
    def __init__(self, board, size):
        # The backend of the application.
        self.board = board
        self.size = size
        # Create the window and give it a title, then bring to focus.
        self.window = Tk()
        self.window.title("Four In A Row")
        self.window.focus_force()
        # Set the fonts for the app.
        self.normal_font = Font(family = "Helvetica", size = -24, weight = BOLD)
        self.small_font = Font(family = "Helvetica", size = max(-18, -1 * round(self.size * 3.5)), weight = BOLD)
        # Create and place the canvas.
        self.board_canvas = Canvas(self.window, height = 28 * (self.size + 3.5), width = 14 * ((3 * self.size) + 1), bg = "white")
        self.board_canvas.pack()
        # Create the elements of the frontend but set to None.
        self.grid_columns = [None] * self.size
        self.column_buttons = [[None, None]] * self.size
        self.points_labels = [None, None]
        self.end_menu = [None, None, None, None]
        # Fill out the canvas with the default elements.
        self.reset_display()

    # Start running the window.
    def start(self):
        self.window.mainloop()

    # Reset the display to its initial menu.
    def reset_display(self, board = False):
        # Reset the backend if required.
        if board:
            self.board.reset_board()
        # Clear the canvas.
        self.board_canvas.delete("all")
        # Create a background for each column.
        for column_index in range(self.size):
            left_x = 14 + (column_index * 42)
            right_x = left_x + 28
            self.grid_columns[column_index] = self.board_canvas.create_rectangle(left_x, 40, right_x, 28 * (self.size + 1.5), fill = "white", outline = "")
            self.board_canvas.tag_bind(self.grid_columns[column_index], "<Enter>", lambda event, column = column_index: self.hover_column(column))
            self.board_canvas.tag_bind(self.grid_columns[column_index], "<Button-1>", lambda event, column = column_index: self.on_button_press(column))
            self.board_canvas.tag_bind(self.grid_columns[column_index], "<ButtonRelease-1>", lambda event, column = column_index: self.button_release(column))
            self.board_canvas.tag_bind(self.grid_columns[column_index], "<Leave>", lambda event, column = column_index: self.leave_column(column))
        # Set the column buttons.
        for column_index in range(self.size):
            center_x = 42 * (column_index + 1) - 14
            center_y = 28 * (2.5 + self.size)
            background = self.board_canvas.create_rectangle(center_x - 14, center_y - 14, center_x + 14, center_y + 14, fill = "white", outline = "")
            number = self.board_canvas.create_text(center_x, center_y, text = str(column_index + 1), fill = "black", font = self.normal_font)
            self.column_buttons[column_index] = [background, number]
            self.board_canvas.tag_bind(self.column_buttons[column_index][0], "<Enter>", lambda event, column = column_index: self.hover_column(column))
            self.board_canvas.tag_bind(self.column_buttons[column_index][0], "<Button-1>", lambda event, column = column_index: self.on_button_press(column))
            self.board_canvas.tag_bind(self.column_buttons[column_index][0], "<ButtonRelease-1>", lambda event, column = column_index: self.button_release(column))
            self.board_canvas.tag_bind(self.column_buttons[column_index][0], "<Leave>", lambda event, column = column_index: self.leave_column(column))
            self.board_canvas.tag_bind(self.column_buttons[column_index][1], "<Enter>", lambda event, column = column_index: self.hover_column(column))
            self.board_canvas.tag_bind(self.column_buttons[column_index][1], "<Button-1>", lambda event, column = column_index: self.on_button_press(column))
            self.board_canvas.tag_bind(self.column_buttons[column_index][1], "<ButtonRelease-1>", lambda event, column = column_index: self.button_release(column))
            self.board_canvas.tag_bind(self.column_buttons[column_index][1], "<Leave>", lambda event, column = column_index: self.leave_column(column))
        # Show the points for each player.
        self.points_labels[0] = self.board_canvas.create_text(14, 14, text = "Player: " + str(self.board.get_points(0)), anchor = NW, fill="black", font = self.small_font)
        self.points_labels[1] = self.board_canvas.create_text(14 * (3 * self.size), 14, anchor = NE, text = "Computer: " + str(self.board.get_points(1)), fill="black", justify = RIGHT, font = self.small_font)
        # Set the end menu to None so it is not shown.
        self.end_menu = [None, None, None, None]

    # Display the points for each player.
    def display(self):
        # Delete the old points labels.
        self.board_canvas.delete(self.points_labels[0])
        self.board_canvas.delete(self.points_labels[1])
        # Create the new points labels.
        self.points_labels[0] = self.board_canvas.create_text(14, 14, text = "Player: " + str(self.board.get_points(0)), anchor = NW, fill="black", font = self.small_font)
        self.points_labels[1] = self.board_canvas.create_text(14 * (3 * self.size), 14, anchor = NE, text = "Computer: " + str(self.board.get_points(1)), fill="black", justify = RIGHT, font = self.small_font)

    # Highlight the column when the mouse is over it.
    def hover_column(self, column_index):
        # Change the colour of the column to grey as default.
        colour = "#e1e1e1"
        if self.board.column_is_full(column_index):
            # If the column is full, change the colour to red to warn the user.
            colour = "#ff8383"
        # Change the colour of the column and its button to the new colour.
        self.board_canvas.itemconfigure(self.grid_columns[column_index], fill = colour)
        self.board_canvas.itemconfigure(self.column_buttons[column_index][0], fill = colour)

    # Change the colour of the column back to white when the mouse leaves.
    def leave_column(self, column_index):
        self.board_canvas.itemconfigure(self.grid_columns[column_index], fill = "white")
        self.board_canvas.itemconfigure(self.column_buttons[column_index][0], fill = "white")

    # Change the colour of the column to grey when the mouse is released as
    # mouse will still be hovering.
    def button_release(self, column_index):
        # Change the colour of the column to grey as default.
        colour = "#e1e1e1"
        if self.board.column_is_full(column_index):
            # If the column is full, change the colour to red to warn the user.
            colour = "#ff8383"
        # Change the colour of the column and its button to the new colour.
        self.board_canvas.itemconfigure(self.grid_columns[column_index], fill = colour)
        self.board_canvas.itemconfigure(self.column_buttons[column_index][0], fill = colour)

    # When a button is pressed, add the disk to the column and update display.
    def on_button_press(self, column_index):
        # Change the colour of the column to a darker grey as default.
        colour = "grey"
        if self.board.column_is_full(column_index):
            # If the column is full, change the colour to a darker red to warn
            # the user.
            colour = "red"
        # Change the colour of the column and its button to the new colour.
        self.board_canvas.itemconfigure(self.grid_columns[column_index], fill = colour)
        self.board_canvas.itemconfigure(self.column_buttons[column_index][0], fill = colour)
        # If the column can be added to, add the disk and update the display.
        if self.board.add(column_index, 1):
            # Update display
            self.add_to_display(column_index, 1)
            self.display()
            # If game is over, show the end menu.
            if self.board.is_game_over():
                self.show_end_menu()
                return
            else:
                # If game is not over, take AI's move and update the display.
                ai_added, ai_column = self.board.add_ai()
                if ai_added:
                    # Update display if AI made a move.
                    self.add_to_display(ai_column, 2)
                    self.display()
                # Check if game is now over, if so show the end menu.
                if self.board.is_game_over():
                    self.show_end_menu()

    # Add the disk to the display in the given column for the given player.
    def add_to_display(self, column_index, player):
            available_row = self.board.get_available_row(column_index)
            if player == 1:
                player_text = "O"
            elif player == 2:
                player_text = "X"
            else:
                player_text = " "
            slot_x = 42 * (column_index + 1) - 14
            slot_y = 28 * (2 + (self.size - available_row - 1))
            # Create the disk in the given column and row, assign highlights.
            new_disk = self.board_canvas.create_text(slot_x, slot_y, text = player_text, fill="black", font = self.normal_font)
            self.board_canvas.tag_bind(new_disk, "<Enter>", lambda event, column = column_index: self.hover_column(column))
            self.board_canvas.tag_bind(new_disk, "<Button-1>", lambda event, column = column_index: self.on_button_press(column))
            self.board_canvas.tag_bind(new_disk, "<ButtonRelease-1>", lambda event, column = column_index: self.button_release(column))
            self.board_canvas.tag_bind(new_disk, "<Leave>", lambda event, column = column_index: self.leave_column(column))

    # Show the end menu when the game is over.
    def show_end_menu(self):
        # Create a background for the end menu, covering the whole board.
        self.end_menu[0] = self.board_canvas.create_rectangle(14, 40, 42 * self.size, (self.size + 1.5) * 28, fill = "#e1e1e1", outline = "")
        # Set the final message.
        if self.board.get_points(0) == self.board.get_points(1):
            winner = "It was a Draw"
        elif self.board.get_points(0) < self.board.get_points(1):
            winner = "Winner: Computer"
        else:
            winner = "Winner: Player"
        # Create the end menu with the final message and a restart button.
        self.end_menu[1] = self.board_canvas.create_text(7 * ((3 * self.size) + 1), ((28 * (self.size + 3.5)) / 2) - 35, fill = "black", text = f"Game Over\n{winner}", justify = CENTER, font = self.small_font)
        self.end_menu[2] = self.board_canvas.create_rectangle(((14 * ((3 * self.size) + 1)) / 2) - 49, ((28 * (self.size + 3.5)) / 2) + 7, ((14 * ((3 * self.size) + 1)) / 2) + 49, ((28 * (self.size + 3.5)) / 2) + 35, fill = "grey", outline = "")
        self.board_canvas.tag_bind(self.end_menu[2], "<ButtonRelease-1>", lambda _: self.reset_display(board = True))
        self.board_canvas.tag_bind(self.end_menu[2], "<Button-1>", lambda _: self.restart_click())
        self.board_canvas.tag_bind(self.end_menu[2], "<Enter>", lambda _: self.hover_restart())
        self.board_canvas.tag_bind(self.end_menu[2], "<Leave>", lambda _: self.leave_restart())
        self.end_menu[3] = self.board_canvas.create_text((14 * ((3 * self.size) + 1)) / 2, ((28 * (self.size + 3.5)) / 2) + 21, fill = "white", text = "Restart", justify = CENTER, font = self.small_font)
        self.board_canvas.tag_bind(self.end_menu[3], "<ButtonRelease-1>", lambda _: self.reset_display(board = True))
        self.board_canvas.tag_bind(self.end_menu[3], "<Button-1>", lambda _: self.restart_click())
        self.board_canvas.tag_bind(self.end_menu[3], "<Enter>", lambda _: self.hover_restart())
        self.board_canvas.tag_bind(self.end_menu[3], "<Leave>", lambda _: self.leave_restart())
        # Remove the column buttons backgrounds.
        for index in range(self.size):
            self.board_canvas.delete(self.column_buttons[index][0])

    # Change the colour of the restart button while it is clicked.
    def restart_click(self):
        self.board_canvas.itemconfigure(self.end_menu[2], fill = "blue")

    # Change the colour of the restart button while it is hovered over.
    def hover_restart(self):
        self.board_canvas.itemconfigure(self.end_menu[2], fill = "#2d4fa8")

    # Change the colour of the restart button back to the default colour.
    def leave_restart(self):
        self.board_canvas.itemconfigure(self.end_menu[2], fill = "grey")


# The main class that runs the game and encapsulates frontend and backend.
class FourInARow: 
    # Initialise the game with a given size, creating the backend and frontend.
    def __init__(self, size):
        self.board = GameBoard(size)
        self.gui = Frontend(self.board, size)

    # Start the game.
    def play(self):
        self.gui.start()


game = FourInARow(6)
game.play()