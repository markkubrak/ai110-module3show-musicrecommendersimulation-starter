import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    # Discovery features (defaults keep older code/tests working)
    instrumentalness: float = 0.0  # 0.0 = vocal-heavy, 1.0 = no vocals
    popularity: int = 50           # 0-100; low values = hidden gems
    release_year: int = 2020

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # Optional targets (defaults keep older code/tests working)
    target_acousticness: Optional[float] = None    # if None, derived from likes_acoustic
    target_valence: float = 0.6                    # 0.0 = sad/dark, 1.0 = happy/bright
    target_instrumentalness: float = 0.5           # 0.0 = vocals, 1.0 = instrumental
    discovery: float = 0.5                         # 0 = favor hits, 1 = favor hidden gems

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user, best match first."""
        by_id = {song.id: song for song in self.songs}
        ranked = recommend_songs(profile_to_prefs(user), [asdict(s) for s in self.songs], k)
        return [by_id[song["id"]] for song, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable explanation of why this song scored the way it did."""
        score, reasons = score_song(profile_to_prefs(user), asdict(song))
        return f"Score {score:.2f}: " + ", ".join(reasons)

# Algorithm Recipe weights (see README "How The System Works")
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.5
ACOUSTIC_WEIGHT = 0.75
VALENCE_WEIGHT = 0.5
INSTRUMENTAL_WEIGHT = 0.5
DISCOVERY_WEIGHT = 0.5

INT_FIELDS = {"id", "popularity", "release_year"}
FLOAT_FIELDS = {"energy", "tempo_bpm", "valence", "danceability",
                "acousticness", "instrumentalness"}

def profile_to_prefs(user: UserProfile) -> Dict:
    """Convert a UserProfile into the user_prefs dict used by score_song."""
    prefs = asdict(user)
    if prefs["target_acousticness"] is None:
        prefs["target_acousticness"] = 1.0 if user.likes_acoustic else 0.0
    return prefs

def closeness(value: float, target: float) -> float:
    """Return 1.0 when value equals target, falling linearly to 0.0 as they diverge."""
    return max(0.0, 1.0 - abs(value - target))

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dicts, converting numeric columns to int/float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in INT_FIELDS & row.keys():
                row[field] = int(row[field])
            for field in FLOAT_FIELDS & row.keys():
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences, returning (score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("favorite_genre"):
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT:.2f})")
    if song["mood"] == user_prefs.get("favorite_mood"):
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT:.2f})")

    # Closeness features: (label, song field, prefs key, weight)
    if user_prefs.get("target_acousticness") is None and "likes_acoustic" in user_prefs:
        user_prefs = {**user_prefs,
                      "target_acousticness": 1.0 if user_prefs["likes_acoustic"] else 0.0}
    numeric = [
        ("energy", "energy", "target_energy", ENERGY_WEIGHT),
        ("acousticness", "acousticness", "target_acousticness", ACOUSTIC_WEIGHT),
        ("valence", "valence", "target_valence", VALENCE_WEIGHT),
        ("instrumentalness", "instrumentalness", "target_instrumentalness", INSTRUMENTAL_WEIGHT),
    ]
    for label, field, key, weight in numeric:
        target = user_prefs.get(key)
        if target is None or field not in song:
            continue
        points = weight * closeness(song[field], target)
        score += points
        reasons.append(f"{label} {song[field]:.2f} vs target {target:.2f} (+{points:.2f})")

    discovery = user_prefs.get("discovery")
    if discovery is not None and "popularity" in song:
        p = song["popularity"] / 100
        points = DISCOVERY_WEIGHT * (discovery * (1 - p) + (1 - discovery) * p)
        score += points
        reasons.append(f"popularity {song['popularity']} (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank highest first, and return the top k as (song, score, explanation)."""
    target_energy = user_prefs.get("target_energy", 0.5)
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    # Tie-breakers: closer energy first, then title alphabetically
    ranked = sorted(
        scored,
        key=lambda item: (-item[1], abs(item[0]["energy"] - target_energy), item[0]["title"]),
    )
    return ranked[:k]
