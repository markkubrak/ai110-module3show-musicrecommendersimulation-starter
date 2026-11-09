"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs

# High-Energy Pop (default): upbeat pop listener
POP_HAPPY = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.80,            # 0.0-1.0, scored by closeness
    "target_acousticness": 0.20,      # prefers produced/electronic texture
    "target_valence": 0.80,           # bright and positive
    "target_instrumentalness": 0.05,  # wants vocals
    "discovery": 0.5,                 # 0 = favor hits, 1 = favor hidden gems
}

# Chill Lofi: study listener
LOFI_CHILL = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "target_acousticness": 0.80,
    "target_valence": 0.60,
    "target_instrumentalness": 0.80,
    "discovery": 0.5,
}

# Deep Intense Rock: loud, dark, guitar-driven
ROCK_INTENSE = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.92,
    "target_acousticness": 0.10,
    "target_valence": 0.35,
    "target_instrumentalness": 0.15,
    "discovery": 0.5,
}

# --- Adversarial / edge-case profiles ---

# Conflicting: very high energy but a sad mood (sad songs in the catalog are low energy)
SAD_BUT_HYPED = {
    "favorite_genre": "blues",
    "favorite_mood": "sad",
    "target_energy": 0.90,
    "target_acousticness": 0.20,
    "target_valence": 0.20,
    "target_instrumentalness": 0.20,
    "discovery": 0.5,
}

# Genre and mood that do not exist in the catalog: only numeric features can score
GENRE_GHOST = {
    "favorite_genre": "k-pop",
    "favorite_mood": "dreamy",
    "target_energy": 0.65,
    "target_acousticness": 0.30,
    "target_valence": 0.70,
    "target_instrumentalness": 0.10,
    "discovery": 0.5,
}

# Contradictory texture: wants EDM but fully acoustic and instrumental
ACOUSTIC_RAVER = {
    "favorite_genre": "edm",
    "favorite_mood": "euphoric",
    "target_energy": 0.95,
    "target_acousticness": 0.95,
    "target_valence": 0.75,
    "target_instrumentalness": 0.90,
    "discovery": 0.5,
}

# Middle-of-the-road taste, maximum discovery: does popularity decide everything?
HIDDEN_GEM_HUNTER = {
    "favorite_genre": "",
    "favorite_mood": "",
    "target_energy": 0.50,
    "target_acousticness": 0.50,
    "target_valence": 0.50,
    "target_instrumentalness": 0.50,
    "discovery": 1.0,
}

PROFILES = {
    "High-Energy Pop (default)": POP_HAPPY,
    "Chill Lofi": LOFI_CHILL,
    "Deep Intense Rock": ROCK_INTENSE,
    "Edge case: Sad but Hyped": SAD_BUT_HYPED,
    "Edge case: Genre Ghost": GENRE_GHOST,
    "Edge case: Acoustic Raver": ACOUSTIC_RAVER,
    "Edge case: Hidden Gem Hunter": HIDDEN_GEM_HUNTER,
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

    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
