import src.builders as builds
import src.draws as draws
import src.intent as intent
from datetime import datetime as dt
import sys
import optparse


def main():
    parser = optparse.OptionParser()
    parser.add_option(
        "-s", "--spread", help="choose spread between [draw one, past present future]"
    )
    parser.add_option("-p", "--prompt", help="write your prompt for the spread")

    (options, args) = parser.parse_args()

    deck = builds.build_full_deck()

    # Get spread type from options or user input
    if options.spread:
        inp = options.spread
    else:
        inp = input("Enter spread type (draw one, past present future): ")

    # Get prompt from options or user input
    if options.prompt:
        user_intent = options.prompt

    else:
        user_intent = dt.now()

    # Convert intent string to seed
    intent_seed = intent.read_intent(user_intent)

    draw_function = draws.process_draw(inp)

    draw = draw_function(deck, intent=intent_seed)

    # Clear previous input lines if interactive
    if not (options.spread and options.prompt):
        # ANSI escape to move cursor up
        sys.stdout.write("\x1b[1A")
        # ANSI escape to clear entire line
        sys.stdout.write("\x1b[2K")

    for i in range(len(draw["spread"])):
        print(draw["spread"][i] + ":\n")
        print(draw["cards"][i])
        print(draw["messages"][i] + "\n")


if __name__ == "__main__":
    main()
