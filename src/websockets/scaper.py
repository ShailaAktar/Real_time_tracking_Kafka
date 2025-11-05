import snscrape.modules.twitter as sntwitter

query = "#startup since:2025-10-01"
max_results = 20  # keep small for quick test

print(f"Fetching {max_results} tweets for query: {query}\n")

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= max_results:
        break
    print(f"[{i+1}] @{tweet.user.username} — {tweet.date}")
    print(tweet.content)
    print("-" * 80)


'''



'''