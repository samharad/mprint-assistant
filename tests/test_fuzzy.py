from fuzzywuzzy import fuzz
import sys

print(fuzz.partial_ratio("library", "shapiro library"))