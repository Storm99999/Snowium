import curses
import random


def rainbow_color_pairs():
    if not curses.has_colors() or curses.COLORS < 8:
        raise ValueError(
            "Terminal doesn't support enough colors for the rainbow effect"
        )

    color_pairs = []
    for i in range(1, 8):  # use colors 1 to 7 
        curses.init_pair(i, i, curses.COLOR_BLACK)
        color_pairs.append(curses.color_pair(i))
    return color_pairs


def create_snowflake():
    return {
        "x": random.randint(1, curses.COLS - 1),
        "y": 0,
        "speed": random.uniform(0.1, 0.5),
    }


def move_snowflake(snowflake):
    snowflake["y"] += snowflake["speed"]


def draw_snowflake(win, snowflake):
    y, x = int(snowflake["y"]), int(snowflake["x"])
    if 0 <= y < curses.LINES and 0 <= x < curses.COLS:
        win.addch(y, x, "❄", curses.color_pair(1))


def draw_christmas_tree(win):
    tree_art = [
        "    _\\/_",
        "     /\\",
        "     /\\",
        "    /  \\",
        "    /~~\\o",
        "   /o   \\",
        "  /~~*~~~\\",
        " o/    o \\",
        " /~~~~~~~~\\~`",
        "/__*_______\\",
        "     ||",
        "   \\====/",
        "    \\__/",
    ]

    tree_height = len(tree_art)
    tree_width = len(tree_art[0])

    start_row = curses.LINES // 2 - tree_height // 2
    start_col = curses.COLS // 2 - tree_width // 2

    for i in range(tree_height):
        color_pair = color_pairs[i % len(color_pairs)]
        win.addstr(start_row + i, start_col, tree_art[i], color_pair)

    return start_row, start_col


def main(stdscr):
    curses.curs_set(0)  # hide cursor
    curses.start_color()

    global color_pairs
    try:
        color_pairs = rainbow_color_pairs()
    except ValueError as e:
        stdscr.addstr(0, 0, str(e), curses.color_pair(1))
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.clear()

    snowflakes = []
    win = curses.newwin(curses.LINES, curses.COLS, 0, 0)

    while True:
        win.clear()

        # generate
        if random.random() < 0.1:
            snowflakes.append(create_snowflake())

        # move func
        for snowflake in snowflakes:
            move_snowflake(snowflake)
            draw_snowflake(win, snowflake)

        # remove
        snowflakes = [flake for flake in snowflakes if flake["y"] < curses.LINES]

        # draw
        start_row, start_col = draw_christmas_tree(win)

        # add text
        tree_top_text = "Merry Christmas from SNOWSEC"
        for i, char in enumerate(tree_top_text):
            color_pair = color_pairs[i % len(color_pairs)]
            win.addstr(start_row - 1, start_col + i, char, color_pair)

        win.refresh()
        curses.delay_output(200)  # delay


if __name__ == "__main__":
    curses.wrapper(main)
