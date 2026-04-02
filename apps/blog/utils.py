def reading_time(content, words_per_minute=200):
    words = len(content.split())
    minutes = max(1, round(words / words_per_minute))
    return minutes
