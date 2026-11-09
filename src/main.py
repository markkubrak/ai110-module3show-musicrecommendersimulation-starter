"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs

# Default profile: upbeat pop listener
POP_HAPPY = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.80,            # 0.0-1.0, scored by closeness
    "target_acousticness": 0.20,      # prefers produced/electronic texture
    "target_valence": 0.80,           # bright and positive
    "target_instrumentalness": 0.05,  # wants vocals
    "discovery": 0.5,                 # 0 = favor hits, 1 = favor hidden gems
}

# Contrast profile: chill lofi study listener
LOFI_CHILL = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "target_acousticness": 0.80,
    "target_valence": 0.60,
    "target_instrumentalness": 0.80,
    "discovery": 0.5,
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a ranked, readable list of recommendations with score breakdowns."""
    print("=" * 64)
    print(f"Profile: {name}")
    print("=" * 64)
    for rank, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k), 1):
        print(f"{rank}. {song['title']} by {song['artist']}  [{song['genre']}, {song['mood']}]")
        print(f"   Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    print_recommendations("pop / happy (default)", POP_HAPPY, songs)
    print_recommendations("lofi / chill", LOFI_CHILL, songs)


if __name__ == "__main__":
    main()
