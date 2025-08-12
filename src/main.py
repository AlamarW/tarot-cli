import src.builders as builds
import src.spreads as spreads
import src.intent as intent
from datetime import datetime as dt
import sys
import optparse
import time

WAIT_TIME = 0.5

def main():
    parser = optparse.OptionParser()
    parser.add_option(
        "-s",
        "--spread",
        help="choose spread between [draw one, past present future, celtic cross]",
    )
    parser.add_option("-p", "--prompt", help="write your prompt for the spread")
    parser.add_option("-n", "--noprompt", action='store_true',
                      help="Won't prompt user for query in interactive mode")

    (options, args) = parser.parse_args()

    deck = builds.build_full_deck()

    if options.spread:
        inp = options.spread.lower()

        if options.prompt:
            user_intent = options.prompt
            intent_seed = intent.read_intent(user_intent)

        else:
            user_intent = dt.now()
            intent_seed = intent.read_intent(user_intent)

            draw_function = spreads.process_draw(inp)
            draw = draw_function(deck, intent=intent_seed)

            for i in range(len(draw["spread"])):
                print(draw["spread"][i] + ":\n")
                print(draw["cards"][i])
                print(draw["messages"][i] + "\n")
    else:
        while True:
            inp = input("Enter spread type (draw one, past present future, celtic cross) or type exit to exit: ").lower()
            if inp == "exit":
                print("Exiting Tarot-cli")
                time.sleep(WAIT_TIME)
                break

            try:
                draw_function = spreads.process_draw(inp)
            except:
                print("Invalid input, please try again")
                time.sleep(WAIT_TIME)
                continue
            if options.noprompt:
                user_intent = dt.now()
            else:
                user_intent = input("What is your query (You can leave this blank if you want)?")

            if user_intent == "exit":
                print("Exiting Tarot-cli")
                time.sleep(WAIT_TIME)
                break

            if user_intent == "":
                user_intent = dt.now()
            intent_seed = intent.read_intent(user_intent)

            draw = draw_function(deck, intent=intent_seed)

            # ANSI escape to move cursor up
            #sys.stdout.write("\x1b[1A")
            # ANSI escape to clear entire line
            #sys.stdout.write("\x1b[2K")

            for i in range(len(draw["spread"])):
                print(draw["spread"][i] + ":\n")
                print(draw["cards"][i])
                print(draw["messages"][i] + "\n")


if __name__ == "__main__":
    main()
