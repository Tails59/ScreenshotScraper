# How the URL will be generated
# RAND = random link
# SEQ = sequential, starting from "aa0000" to "zz9999", slow and boring
SEARCH_MODE = "RAND"

# Delay between each request (in milliseconds)
SEARCH_DELAY = 300

# Amount of times to run search requests (0 for infinite)
# This will be the amount of images returned, if invalid or bad links are searched they wont be counted
# ^when i can be bothered adding that, atm its just 10 requests lol
SEARCH_ITERATIONS = 100
