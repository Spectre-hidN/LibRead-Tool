import sys
import os
import time

def clearScreen():
    """
    Clears the terminal
    """
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

def clearLine():
    """
    Clears the current line
    """
    length = os.get_terminal_size()[0]
    whiteSpace = " "*length
    print(whiteSpace, end="\r")

class Prettify():

    def __init__(self):
        """Return specified color escape c0des if flushCodes flag is False else flush it to the console."""
        
        #For some unknown reason window's command prompt does not recognise any escape code unless it is registered/cache using system calls. The below line will make sure to recognise all escape codes.
        if os.name == 'nt':
            os.system('echo|set /p="\033[38;5;12m\033[0m"')
        
        try:
            if sys.argv[1] == 'dump_cols':
                self.flushCodes = True
            else:
                self.flushCodes = False
        except:
            self.flushCodes = False

        try:
            if sys.argv[1] == 'dump_bgs':
                self.OnlyBG = True
            else:
                self.OnlyBG = False
        except:
            self.OnlyBG = False

    def dump_colors(self, code=None, ForBG=False):
        for i in range(0, 256):
            color_code = str(i)
            if not self.OnlyBG:
                escape_code = u"\u001b[38;5;" + color_code + "m"
            else:
                escape_code = "\033[48;5;" + color_code + "m"
            if code != None:
                if str(code) == color_code:
                    return escape_code
            elif code == None:
            	if self.OnlyBG or self.flushCodes:
            		sys.stdout.write(escape_code + color_code.ljust(4) + " ")

    def progressBar(self, total_size: int, size_done: int, prefix="On the way!", suffix="There", length=None, fill_symbol='█', ToBeFill_symbol=' ', static_color=[]): #type: ignore
        """
        Simple Progress bar that changes colors upon progress!

        PARAMETERS --> length {DEFAULT: os.get_terminal_size()[0] - len(prefix) - len(suffix)- 11}
                        prefix {DEFAULT: "On the way!"}
                        suffix {DEFAULT: "There"}
                        total_size {DATATYPE: int} [REQUIRED]
                        size_done {DATATYPE: int} [REQUIRED]
                        fill_symbol {DEFAULT: '█'}
                        ToBeFill_symbol {DEFAULT: ' '}
                        static_color {DEFAULT: []} (Index: [0 -> fill_symbol, 1 -> ToBeFill_symbol])

        NOTE --> endline (\n) should be provided after the job is completed to bring the cursor to a new line.
                 When Overriding the 'fill_symbol' or 'ToBeFill_symbol' with characters of different length, then specifying the length manually might required.
        """
        decimals = 1
        if length == None:
            length = os.get_terminal_size()[0] - len(prefix) - len(suffix) - 11
            if len(fill_symbol) > 1:
                length = length // len(fill_symbol)
        total = total_size
        ToBeFill_length = len(fill_symbol) // len(ToBeFill_symbol)

        try:
            ToBeFill_symbol = self.dump_colors(code=static_color[1]) + ToBeFill_symbol + self.dump_colors(code=7)
        except (IndexError, TypeError):
            pass

        # Progress Bar Printing Function
        def printProgressBar(iteration):
            if self.flushCodes == True:
                exit(0)
            percent = round(float(("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))) + 0.1, 1)

            if percent > float(100):
                percent = 100.0

            fill_color_applied = False
            try:
                fill = self.dump_colors(code=static_color[0]) + fill_symbol + self.dump_colors(code=7)
                fill_color_applied = True
            except (IndexError, TypeError):
                pass

            if not fill_color_applied:
                if percent >= float(0) and percent <= float(11):
                    fill = self.dump_colors(
                        code=124) + fill_symbol + self.dump_colors(code=7)
                elif percent > float(11) and percent <= float(21):
                    fill = self.dump_colors(
                        code=196) + fill_symbol + self.dump_colors(code=7)
                elif percent > float(21) and percent <= float(31):
                    fill = self.dump_colors(
                        code=202) + fill_symbol + self.dump_colors(code=7)
                elif percent > float(31) and percent <= float(41):
                    fill = self.dump_colors(
                        code=208) + fill_symbol + self.dump_colors(code=7)
                elif percent > float(41) and percent <= float(55):
                    fill = self.dump_colors(
                        code=220) + fill_symbol + self.dump_colors(code=7)
                elif percent > float(55) and percent <= float(71):
                    fill = self.dump_colors(
                        code=190) + fill_symbol + self.dump_colors(code=7)
                elif percent > float(71) and percent <= float(85):
                    fill = self.dump_colors(
                        code=34) + fill_symbol + self.dump_colors(code=7)
                elif percent > float(85):
                    fill = self.dump_colors(
                        code=46) + fill_symbol + self.dump_colors(code=7)

            filledLength = int(length * iteration // total) + 1
            bar = fill * filledLength + (ToBeFill_symbol * ToBeFill_length) * (length - filledLength)
            print(f'\r{prefix} |{bar}| {percent}% {suffix}', end="\r")
        if self.flushCodes or self.OnlyBG:
            exit(0)
        else:
            printProgressBar(size_done)

    def dump_styles(self, styles=None):
        """
        Return esacpe code of specified
        *** Tested on Unix terminal ***
        """

        if styles == 'bold':
            return "\033[1m"
        elif styles == 'faint':
            return '\033[2m'
        elif styles == 'italic':
            return '\033[3m'
        elif styles == 'underline':
            return '\033[4m'
        elif styles == 'blink':
            return '\033[5m'
        elif styles == 'reverse':
            return '\033[7m'
        elif styles == 'conceal':
            return '\033[8m'
        elif styles == 'crossed-out':
            return '\033[9m'
        elif styles == 'double-underline':
            return '\033[21m'
        elif styles == 'bold-off' or styles == 'faint-off':
            return '\033[22m'
        elif styles == 'italic-off':
            return '\033[23m'
        elif styles == 'underline-off':
            return '\033[24m'
        elif styles == 'blink-off':
            return '\033[25m'
        elif styles == 'reverse-off':
        	return '\033[27m'
        elif styles == 'reveal' or styles == 'conceal-off': #type: ignore
            return '\033[28m'
        elif styles == 'crossed-out-off':
            return '\033[29m'
        elif styles == "overlined":
            return '\033[53m'
        elif styles == 'overlined-off':
            return '\033[55m'
        elif styles == 'reset':
            return '\033[0m'
    
    @staticmethod   
    def printErr(msg: str, pauseOnError = True) -> None:
        obj = Prettify()
        print(f"{obj.dump_colors(code=196)}{msg}{obj.dump_styles(styles='reset')}")
        input() if pauseOnError else None

    @staticmethod
    def printSuc(msg: str) -> None:
        obj = Prettify()
        print(f"{obj.dump_colors(code=46)}{msg}{obj.dump_styles(styles='reset')}")

    @staticmethod
    def printWar(msg: str) -> None:
        obj = Prettify()
        print(f"{obj.dump_colors(code=208)}{msg}{obj.dump_styles(styles='reset')}")

    @staticmethod
    def printInf(msg: str) -> None:
        obj = Prettify()
        print(f"{obj.dump_colors(code=198)}{msg}{obj.dump_styles(styles='reset')}")

    @staticmethod   
    def printFeaturedText(msg: str, blinkersColorCode = 196, msgColorCode = 226):
        self = Prettify()
        print(self.dump_styles(styles='blink') + self.dump_colors(code=blinkersColorCode) + '♦ ' + self.dump_styles(styles='blink-off') + self.dump_colors(code=msgColorCode) + msg + self.dump_styles(styles='blink') + self.dump_colors(code=blinkersColorCode) + ' ♦' + self.dump_styles(styles='reset'))

if __name__ == "__main__":
    """For Debugging and Initial testing purposes"""

    cl = Prettify()
    cl.dump_colors()
    dump_styles = False
    try:
        if sys.argv[1] == 'dump_styles':
            dump_styles = True
        else:
            dump_styles = False
    except:
        pass
    if dump_styles:
        #show styles
        print(cl.dump_styles(styles='underline') + 'Styles' + cl.dump_styles(styles='underline-off') + '			' + cl.dump_styles(styles='underline') + 'Codename' + cl.dump_styles(styles='underline-off'))
        print(cl.dump_styles(styles='bold') + "Bold Text" + cl.dump_styles(styles='bold-off') + '		' + 'bold, bold-off')
        print(cl.dump_styles(styles='faint') + "Faint Text" + cl.dump_styles(styles='faint-off') + '	  	' + 'faint, faint-off')
        print(cl.dump_styles(styles='italic') + "Italic Text" + cl.dump_styles(styles='italic-off') + '       	' + 'italic, italic-off')
        print(cl.dump_styles(styles='underline') + "Underlined Text" + cl.dump_styles(styles='underline-off') + '	    	' + 'underline, underline-off')
        print(cl.dump_styles(styles='blink') + "Blinking Text" + cl.dump_styles(styles='blink-off') + '	    	' + 'blink, blink-off')
        print(cl.dump_styles(styles='reverse') + "Inverse FG/BG" + cl.dump_styles(styles='reverse-off') + '	    	' + 'reverse, reverse-off')
        print(cl.dump_styles(styles='conceal') + "Conceal Text" + cl.dump_styles(styles='reveal') + '	    	' + 'conceal, reveal')
        print(cl.dump_styles(styles='overlined') + "Overlined Text" + cl.dump_styles(styles='overlined-off') + '	    	' + 'overlined, overlined-off')
        print(cl.dump_styles(styles='crossed-out') + "Crossed Text" + cl.dump_styles(styles='crossed-out-off') + '	    	' + 'crossed-out, crossed-out-off')
        print(cl.dump_styles(styles='double-underline') + "Double underlined Text" + cl.dump_styles(styles='underline-off') + '	' + 'double-underline, underline-off')
        print()
        print(cl.dump_styles(styles='blink') + cl.dump_colors(code=196) + '♦ ' + cl.dump_styles(styles='blink-off') + cl.dump_colors(code=226) + 'Tested on Unix Terminal. Some styles may not work on other platforms' + cl.dump_styles(styles='blink') + cl.dump_colors(code=196) + ' ♦' + cl.dump_styles(styles='reset'))
    else:
        for i in range(123452):
            time.sleep(0.0001)
            cl.progressBar(total_size=123452, size_done=i, fill_symbol=' ☻ ', ToBeFill_symbol=' ☺ ', length=20)
        print()
