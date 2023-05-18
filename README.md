# PYFM - Henry Boisdequin
Music recommendation system built in Python, using the [last.fm](https://last.fm) api.

### Planning

Algorithm: Content-Based Filtering
1. 2 options for input:
>> * User information (username | uses favorite artists, genres, tags to offer genre/artist/track recommendations)
>> * Artist information (artist name | uses given artist to offer similar artist recommendations)
2. Calculate Item Similarity:
>> * Use Jaccard similarity & Cosine similarity to compute similarity between artist/genres/tracks
3. Build User Profile:
>> * Get weighted preferences for different user artist/genres/tracks based on last.fm metadata
4. Generate Recommendations:
>> * Use the similarity between an artist profile to other artist profiles OR user data to artist/genre/track profiles
>> * Rank the recommendations based on their similarity

### Notes
[API Key](https://www.last.fm/api/accounts)
