# Tarot CLI

## Description

Tarot CLI lets you use the wisdom of the tarot from your command-line.
When called without options, Taort-CLI will go into an interactive mode. Type
`exit` to exit in interactive mode.

## Options

Tarot CLI currently supports the following options:
-`-s`: spread, defines what spread to use for your reading (Draw one,
        past present future, and Celtic cross)
-`-p`: prompt, use a specific question to guide your tarot reading
        (implementation details below)
-`-n`: noprompt, disables repetitive asking for prompt in interactive mode if
        it is not desired

## Spreads

Current Spread Commands:

1. draw one: draws a single card
2. draw three: generic three card pull
3. past present future: past present future pull
4. celtic cross: ... for the celtic cross (10 cards)a

I can make more spreads on request
