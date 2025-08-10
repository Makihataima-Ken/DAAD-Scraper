def filter_by_keyword(programs, keyword):
    keyword = keyword.lower()
    return [p for p in programs if keyword in p["title"].lower()]
