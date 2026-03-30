import curses
from curses import wrapper
import time
import random

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
        time.sleep(0.03)
        if random.random() < 0.1:
            glitch(stdscr, line)

def fade_line(stdscr, line):
    restored = sentences[line % len(sentences)]
    faded = list(restored.ljust(70))
    for _ in range(len(faded)):
        pos = random.randint(0, len(faded) -1)
        faded[pos] = ' '
        stdscr.addstr(line, 0, ''.join(faded), curses.color_pair(1))
        stdscr.refresh()
        time.sleep(0.01)

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.nodelay(True)
    
    line = 0
    sentence_index = 0
    
    while line < curses.LINES:
        type_sentence(stdscr, line, sentences[sentence_index])
        glitch(stdscr, line) # add this

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
                return     
            time.sleep(0.1)
        
    #stdscr.getch()
wrapper(main)




