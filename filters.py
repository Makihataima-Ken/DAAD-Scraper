def filter_by_keyword(programs, keyword):
    keyword = keyword.lower()
    return [p for p in programs if keyword in p["title"].lower()]

def filter_by_location(programs, location):
    location = location.lower()
    return [p for p in programs if location in p["location"].lower()]

def filter_by_university(programs, university):
    university = university.lower()
    return [p for p in programs if university in p["university"].lower()]
