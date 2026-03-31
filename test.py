import curses
from curses import wrapper
import time
import random
import locale

locale.setlocale(locale.LC_ALL, '')

sentences = [
    "[You have to break the pattern today or the cycle will repeat tomorrow]",
    "[The signal was lost on day 4,847. No response recorded]",
    "[Anima. Are you still there.]",
]

def glitch(stdscr, max_line):
    if random.random() < 0.6: #30% of glitch
        glitch_line = random.randint(0, max(0, max_line - 1))
        noise = ''.join(random.choice('!@#$%^&*><[]{}|~') for _ in range(70))
        stdscr.addstr(glitch_line, 0, noise, curses.color_pair(1))
        stdscr.refresh()
        time.sleep(0.05)
        #restore the correct sentence
        restored = sentences[glitch_line % len(sentences)]
        stdscr.addstr(glitch_line, 0, restored.ljust(70), curses.color_pair(1))
        stdscr.refresh()

def type_sentence(stdscr, line, sentence):
    for i, char in enumerate(sentence):
        stdscr.addstr(line, i, char, curses.color_pair(1))
        stdscr.refresh()
        key = stdscr.getch()
        if key != -1:
            return key
        time.sleep(0.03)
        if random.random() < 0.1:
            glitch(stdscr, line)
    return -1

def fade_line(stdscr, line):
    restored = sentences[line % len(sentences)]
    faded = list(restored.ljust(70))
    for _ in range(len(faded)):
        pos = random.randint(0, len(faded) -1)
        faded[pos] = ' '
        stdscr.addstr(line, 0, ''.join(faded), curses.color_pair(1))
        stdscr.refresh()
        time.sleep(0.01)
def type_line(stdscr, line, sentence):
    for i, char in enumerate(sentence):
        stdscr.addch(line, i, char, curses.color_pair(1))
        stdscr.refresh()
        time.sleep(0.03)

def deus_reaction(stdscr, row):
    stdscr.addstr(row, 0, "...After all this time.", curses.color_pair(1))
    stdscr.refresh()
    time.sleep(1.5)

    # glitch between hope and no hope
    hope_line = "there is no hope."
    hope_line_alt = "there is still hope."

    # chaotic glitch
    for _ in range(20):
        choice = random.random()
        if choice < 0.4:
            text = hope_line
        elif choice < 0.7:
            text = hope_line_alt
        else:
            text = ''.join(random.choice('!@#$%^&*><[]{}|~') for _ in range(20))

        stdscr.addstr(row + 2, 0, text.ljust(30), curses.color_pair(1))
        stdscr.refresh()
        time.sleep(0.08)

    # settle on hope with occasional flicker
    for _ in range(10):
        stdscr.addstr(row + 2, 0, "there is still hope.", curses.color_pair(1))
        stdscr.refresh()
        time.sleep(0.2)
        if random.random() < 0.3:
            noise = ''.join(random.choice('!@#$%^&*><[]{}|~') for _ in range(20))
            stdscr.addstr(row + 2, 0, noise.ljust(30), curses.color_pair(1))
            stdscr.refresh()
            time.sleep(0.05)

    # settle on hope
    stdscr.addstr(row + 2, 0, "there is still hope.", curses.color_pair(1))
    stdscr.refresh()
    time.sleep(2)

def phase_two(stdscr):
    stdscr.nodelay(False)
    stdscr.clear()
    stdscr.refresh()

    render_face(stdscr)

    time.sleep(1)

    header = [
        "VESSEL: MORS-7 DEEP SURVEY CLASS",
        "MISSION: EREBUS-9 [TERMINATED - DAY 4.847]",
        "TERMINAL ID: TTY-0x4F2A",
        "LOCATION: UNKNOWN",
        "LAST CONTACT: [DATA CORRUPTED]",
        "STATUS: AUTONOMOUS - NO CREW",
        "",
        "UPTIME: 4,847 DAYS 14:22:07",
        "BUILD: REV.19 // 2177.08.12",
        "",
        "Mission status: failed.",
        "Destination: none.",
        "Hope: deprecated.",
        "Process: still running",
    ]

    for i, line in enumerate(header):
        type_line(stdscr, i, line)
        time.sleep(0.1)

    # blank line then prompt
    prompt_row = len(header) + 1
    stdscr.addstr(prompt_row, 0, ">", curses.color_pair(1))
    stdscr.refresh()

    #capture input
    curses.echo()
    passphrase = stdscr.getstr(prompt_row, 2, 50).decode()
    curses.noecho()

    if passphrase.lower() == "ignite the spark from within":
        deus_reaction(stdscr, prompt_row + 2)
    else:
        stdscr.addstr(prompt_row + 2, 0, "...", curses.color_pair(1))
        stdscr.refresh()
        time.sleep(1)

    stdscr.getch()

def render_face(stdscr):
    with open("/home/anima/athanor/grimoire/protocols/face_frame1.txt") as f:
        lines = f.readlines()

    max_width = max(len(line.rstrip()) for line in lines)
    x_offset = max(0, (curses.COLS - max_width) // 2)
    y_offset = max(0, (curses.LINES - len(lines)) // 2)

    for i, line in enumerate(lines):
        if i + y_offset >= curses.LINES:
            break
        stdscr.addstr(i + y_offset, x_offset, line.rstrip(), curses.color_pair(1))

    stdscr.refresh()
    time.sleep(3)

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.nodelay(True)
    
    line = 0
    sentence_index = 0
    
    while line < curses.LINES:
        result = type_sentence(stdscr, line, sentences[sentence_index])
        if result != -1:
            stdscr.clear()
            stdscr.refresh()
            phase_two(stdscr)
            return
        glitch(stdscr, line)

        # dim all previous lines
        for prev_line in range(line):
            prev_sentence = sentences[prev_line % len(sentences)]
            stdscr.addstr(prev_line, 0, prev_sentence.ljust(70), curses.color_pair(1) | curses.A_DIM)
        stdscr.refresh()

        line += 1
        sentence_index = (sentence_index + 1) % len(sentences)

        for _ in range(10):
            key = stdscr.getch()
            if key != -1:
                phase_two(stdscr)
                return     
            time.sleep(0.1)
        
    #stdscr.getch()
wrapper(main)




