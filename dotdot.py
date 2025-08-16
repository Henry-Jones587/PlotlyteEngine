import random
import time
import getpass
import subprocess
try: from pynput import keyboard
except ImportError: subprocess.run(["pip", "install", "pynput"]); from pynput import keyboard



class DprintTooLong(Exception):
    def __init__(self, message="Text is too long to dprint."):
        self.message = message
        super().__init__(self.message)

class DotDot:
    SyntaxVer = float(1.2)
    styles = {}
    #Thanks to rene-d for all the colour codes!
    colours = {
        "BLACK": "\033[0;30m",
        "RED": "\033[0;31m",
        "GREEN": "\033[0;32m",
        "BROWN": "\033[0;33m",
        "BLUE": "\033[0;34m",
        "PURPLE": "\033[0;35m",
        "CYAN": "\033[0;36m",
        "LIGHT_GRAY": "\033[0;37m",
        "DARK_GRAY": "\033[1;30m",
        "LIGHT_RED": "\033[1;31m",
        "LIGHT_GREEN": "\033[1;32m",
        "YELLOW": "\033[1;33m",
        "LIGHT_BLUE": "\033[1;34m",
        "LIGHT_PURPLE": "\033[1;35m",
        "LIGHT_CYAN": "\033[1;36m",
        "LIGHT_WHITE": "\033[1;37m",
        "BOLD": "\033[1m",
        "FAINT": "\033[2m",
        "ITALIC": "\033[3m",
        "UNDERLINE": "\033[4m",
        "BLINK": "\033[5m",
        "NEGATIVE": "\033[7m",
        "CROSSED": "\033[9m",
        "END": "\033[0m"
    }
    credit = False
    @staticmethod
    def addstyle(name, code):
            DotDot.styles[name] = [code]
            fmt_code = DotDot.colour(name)
            if fmt_code not in DotDot.styles:
                DotDot.styles[name] = fmt_code

    @staticmethod
    def newprint(text, wait=0.05, format=None, end='\n'):
        if not DotDot.credit:
            DotDot.credits()
        try:
            if format is None:
                format = ["END"]
            if DotDot.SyntaxVer < 1.2:
                raise ValueError("Newprint cannot be used with versions before 1.2. Please either run dprint or change your syntax to 1.2 or later.")
            if len(text) > 4000:
                raise DprintTooLong()
            if len(text) < 1:
                return None
            formats = []
            for item in format:
                # Check if they added more than one of the same format
                if item not in DotDot.colours:
                    formatted_text = DotDot.styles.get(item, "")
                else:
                    formatted_text = DotDot.colour(item)
                
                if formatted_text and formatted_text not in formats:
                    formats.append(formatted_text)
                    print(formatted_text, end="", flush=True)
            for char in text:
                print(char, end="", flush=True)
                time.sleep(wait)
            print(DotDot.colour("END"), end=end)
        except DprintTooLong as e:
            return DotDot.newprint(e.message, wait, format)
        except ValueError as e:
            return DotDot.newprint(f"Error: {e}", wait, format)

    @staticmethod
    def dprint(text, wait=0.05, colour=None, bold=False, italic=False, underline=False):
        if not DotDot.credit:
            DotDot.credits()
        try:
            if len(text) > 4000:
                raise DprintTooLong()
            if len(text) < 1:
                return None
            if DotDot.SyntaxVer == 1.0:
                for char in text:
                    if char == ".":
                        time.sleep(wait * 2)
                    print(char, end="", flush=True)
            elif DotDot.SyntaxVer == 1.1:
                if italic:
                    print(DotDot.colour("ITALIC"), end="", flush=True)
                if underline:
                    print(DotDot.colour("UNDERLINE"), end="", flush=True)
                if colour is not None:
                    print(colour, end="", flush=True)
                if bold:
                    print(DotDot.colour("BOLD"), end="", flush=True)
                for char in text:
                    print(char, end="", flush=True)
                    time.sleep(wait)
                if bold or colour is not None or italic:
                    print(DotDot.colour("END"))
            elif DotDot.SyntaxVer == 1.2:
                raise ValueError("Dprint cannot be used with 1.2. Please either run newprint or change your syntax to before 1.2.")
            else:
                raise ValueError("Invalid SyntaxVer. Please use 1.1 or 1.0 for dprint.")
            print()  # New line at the end
        except DprintTooLong as e:
            return DotDot.dprint(e.message, wait)
        except ValueError as e:
            return DotDot.dprint(f"Error: {e}", wait)
    @staticmethod
    def credits(message="", extended=False):
        DotDot.credit = True
        old_syntax = DotDot.SyntaxVer
        DotDot.SyntaxVer = 1.0
        if message != "":
            DotDot.dprint(f"Starting DotDot Utilities for {message}...", 0.05)
        else:
            DotDot.dprint(f"Starting DotDot Utilities...", 0.05)
        if extended and message != "":
            DotDot.dprint(DotDot.colour("RED") + DotDot.colour("BOLD") + f"DotDot x {message}" + DotDot.colour("END"), 0.05)
        DotDot.dprint("By Henry Jones", 0.05)
        DotDot.dprint(f"Version {old_syntax}", 0.05)
        DotDot.SyntaxVer = old_syntax

    @staticmethod
    def colour(colour):
        return DotDot.colours.get(colour, "")

    @staticmethod
    def load(length=[5, 20]):
        wait = random.randint(length[0], length[1])
        for i in range(0, wait):
            print(f"Loading{'.' * (i % 4)}", end='\r')
            print(" " * 20, end='\r')  # Clear the line
            print(f"Loading{'.' * (i % 4)}", end='\r')
            time.sleep(0.1)
        print(" " * 20, end='\r')  # Clear the line

    @staticmethod
    def load_start():
        DotDot.loading = True
        while DotDot.loading:
            for i in range(0,5):
                print(f"Loading{'.' * (i % 4)}", end='\r')
                print(" " * 20, end='\r')  # Clear the line
                print(f"Loading{'.' * (i % 4)}", end='\r')
                print(" " * 20, end='\r')  # Clear the line
                time.sleep(0.1)
            print(" " * 20, end='\r')  # Clear the line
    def stop_loading():
        DotDot.loading = False
        print("Loading complete!")


class InputPro:
    response = ""  # make this a class variable so keybrd can access it
    
    def __init__(self, Text, Time=0.05, Style=None):
        if DotDot.SyntaxVer < 1.2:
            raise ValueError("InputPro requires DotDot syntaxver to be 1.2.")
        self.text = Text
        self.time = Time
        self.style = Style

    def Input(self):
        DotDot.newprint(self.text, self.time, self.style, '')
        self.response = input("")
        return self.response

    def Hide(self):
        DotDot.newprint(self.text, self.time, self.style, '')
        self.response = getpass.getpass("")
        return self.response

    def Mask(self):
        InputPro.response = ""  # reset before each run
        DotDot.newprint(self.text, self.time, self.style, '')

        with keyboard.Listener(
            on_press=keybrd.on_press,
            on_release=keybrd.on_release
        ) as listener:
            listener.join()
        print("")
        return InputPro.response


class keybrd:
    @staticmethod
    def on_press(key):
        try:
            if key == keyboard.Key.backspace:
                print('\b \b', end='', flush=True)
                InputPro.response = InputPro.response[:-1]
            elif key not in (keyboard.Key.esc, keyboard.Key.enter):
                # Only append printable chars
                if hasattr(key, 'char') and key.char is not None:
                    InputPro.response += key.char
                    print('*', end='', flush=True)
        except Exception:
            pass

    @staticmethod
    def on_release(key):
        if key in (keyboard.Key.esc, keyboard.Key.enter):
            return False





if __name__ == "__main__":
    LoremIpsum = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc finibus a ligula ut pulvinar. Curabitur mollis tincidunt tortor, eget pulvinar mi tincidunt ut. Vivamus et blandit leo. Curabitur vehicula sodales est eu cursus. Vivamus ac maximus diam. Vestibulum tempus ipsum viverra, placerat risus ut, tempor mi. Morbi at interdum lorem. Quisque ut fringilla neque. Vestibulum lectus orci, porttitor at posuere vel, suscipit nec neque. Pellentesque sit amet ullamcorper lacus. Quisque vel leo porta, scelerisque metus at, pulvinar nisl. Vivamus ornare diam malesuada est feugiat sollicitudin. Sed quam nisi, tristique non arcu ut, fermentum tempus ex. Aenean vel iaculis purus, a porttitor leo.

    Curabitur varius ante enim, ut maximus nulla lobortis et. Phasellus semper vel felis at consequat. In sed odio ultrices, vulputate ligula et, sagittis nibh. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Mauris purus augue, porta ac orci id, mattis viverra augue. Maecenas nec nisi feugiat, dictum leo nec, egestas mi. Donec ut mollis sem. Proin porttitor velit dui. In id nisl volutpat, elementum velit non, ultricies felis. Sed nec finibus ipsum. Aliquam ut feugiat dolor. Suspendisse ultrices mollis turpis, quis imperdiet sem pellentesque eu. Suspendisse potenti. Nam feugiat magna quis iaculis blandit.

    Etiam eu justo a massa dignissim semper vel sit amet enim. Phasellus pretium elit vitae dui convallis sodales. Cras vel hendrerit sem, ac dictum orci. Integer ut enim in nisl auctor semper sed id massa. Cras urna nibh, egestas nec molestie vitae, porta et purus. Nunc at mollis nisi. Sed interdum lorem vel aliquam interdum. Etiam justo nibh, porttitor at gravida ac, eleifend id ipsum. Suspendisse eleifend faucibus lorem, sed gravida nulla tempus id. Sed fringilla ipsum nunc, vitae accumsan tortor commodo ut. Integer quis lacus id felis molestie rutrum. Vestibulum nec dolor vehicula, viverra magna a, volutpat quam. In id pellentesque risus.

    Nunc sodales scelerisque lobortis. Nullam aliquet diam enim, ut lobortis nisl pharetra id. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Phasellus commodo dui sed lacus volutpat, id fermentum neque sodales. Cras nunc felis, consequat ac rhoncus eu, mattis a dui. Donec augue libero, cursus vel ante et, rutrum dapibus nunc. Aenean malesuada varius suscipit. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam bibendum tempus diam, quis cursus est porta eget. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In vel orci ut dui suscipit hendrerit. Quisque non semper nisl, non vulputate lectus. Nullam id consectetur odio. Mauris tristique condimentum libero at iaculis. Phasellus accumsan mauris sed fermentum rhoncus. Vivamus magna enim, placerat ac nisi ut, fringilla tincidunt turpis.

    Sed sit amet magna pharetra, rhoncus ligula lobortis, malesuada diam. Vestibulum accumsan nulla id viverra feugiat. Aenean vitae lectus tempor, rutrum diam eget, interdum leo. Duis consectetur odio nec porttitor imperdiet. Sed massa elit, ultricies at tincidunt nec, fringilla id mi. Proin facilisis nunc dictum, pretium quam in, porta est. Nulla rhoncus nulla eu sem porttitor laoreet.
    """
    DotDot.credits()

    DotDot.dprint(LoremIpsum, 0.01)



