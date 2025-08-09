import random
import time


class DprintTooLong(Exception):
    def __init__(self, message="Text is too long to dprint."):
        self.message = message
        super().__init__(self.message)

class DotDot:
    SyntaxVer = float(1.1)
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
            else:
                raise ValueError("Invalid SyntaxVer. Please use 1.1 (recommended) or 1.0")
            print()  # New line at the end
        except DprintTooLong as e:
            return DotDot.dprint(e.message, wait)
        except ValueError as e:
            return DotDot.dprint(f"Error: {e}", wait)
    @staticmethod
    def credits(message="", extended=False):
        DotDot.credit = True
        if message != "":
            DotDot.dprint(f"Starting DotDot Utilities for {message}...", 0.05)
        else:
            DotDot.dprint(f"Starting DotDot Utilities...", 0.05)
        if extended and message != "":
            DotDot.dprint(DotDot.colour("RED") + DotDot.colour("BOLD") + f"DotDot x {message}" + DotDot.colour("END"), 0.05)
        DotDot.dprint("By Henry Jones", 0.05)
        DotDot.dprint("Version 1.1", 0.05)

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



