"""
Utility functions for dealing with arrays
"""

def terms(*items):
    "Provides both a capitalized and uncapitalized version of strings"
    def __():
        for item in items:
            yield item.lower()
            yield item.capitalize()
    return list(__())

def overlaps(l1,l2):
    for v in l2:
        if v in l1:
            return True
    return False

