# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify, Apple Music and YouTube use hybrid systems. **Collaborative filtering** finds patterns in the behavior of millions of users ("listeners like you also loved…"). **Content-based filtering** recommends songs whose attributes resemble what you already enjoy. They draw on interaction data (plays, skips, likes, playlist adds), audio features (energy, tempo, valence), metadata (genre, artist, mood) and context such as time of day. Our simulation has no listening history from other users, so it is a **content-based** recommender. It prioritizes how well a song's attributes *match* the user's preferences, not whether a value is simply high or low. Each song gets a score from a weighted sum: points for a genre match and a mood match, plus closeness scores such as `1 - |song.energy - user.target_energy|`. A separate ranking step sorts every song by score and returns the top *k*.

**`Song` features used:**
- `genre`: exact match with the user's favorite genre (highest weight)
- `mood`: exact match with the user's favorite mood
- `energy`: closeness to the user's target energy (strongest numeric signal)
- `acousticness`: closeness to the user's acoustic preference (secondary weight)
- `id`, `title`, `artist`: used to identify and display songs, not for scoring
- `valence`: closeness to the user's target positivity (separates "sad" from "happy" within the same energy level)
- `instrumentalness`: closeness to the user's vocal vs. instrumental preference
- `popularity` (0–100): combined with a `discovery` setting so users can opt into lesser-known "hidden gems"
- `release_year`: stored for display and future era-based filtering
- `tempo_bpm`, `danceability`: stored but not scored at first, because in this dataset they mostly overlap with energy

**`UserProfile` features used:**
- `favorite_genre`: the genre to match
- `favorite_mood`: the mood to match
- `target_energy`: the preferred energy level (0.0–1.0)
- `likes_acoustic`: whether acoustic songs should be favored
- `target_acousticness`: optional exact acoustic target (0.0–1.0); if not set, `likes_acoustic` becomes 1.0 or 0.0
- `target_valence`: preferred positivity (0.0 = sad/dark, 1.0 = happy/bright)
- `target_instrumentalness`: preferred balance of vocals vs. instrumental (0.0–1.0)
- `discovery`: 0.0 favors popular hits, 1.0 favors lesser-known "hidden gems"

### Algorithm Recipe

**Scoring rule (one song).** Each song earns points from exact matches plus closeness scores. A closeness score is `weight × (1 - |song value - user target|)`, so a song scores highest when it is *nearest* the user's preference, not when its value is simply high or low.

| Feature | Rule | Max points |
|---|---|---|
| Genre | +2.0 if `song.genre == favorite_genre` | 2.0 |
| Mood | +1.0 if `song.mood == favorite_mood` | 1.0 |
| Energy | 1.5 × (1 − \|energy − target_energy\|) | 1.5 |
| Acousticness | 0.75 × (1 − \|acousticness − target_acousticness\|) | 0.75 |
| Valence | 0.5 × (1 − \|valence − target_valence\|) | 0.5 |
| Instrumentalness | 0.5 × (1 − \|instrumentalness − target_instrumentalness\|) | 0.5 |
| Discovery | 0.5 × (discovery × (1 − p) + (1 − discovery) × p), where p = popularity / 100 | 0.5 |
| **Total** | | **6.75** |

If `target_acousticness` is not set, it is taken from `likes_acoustic` (True → 1.0, False → 0.0). Each score comes with a list of reasons (e.g. "+2.0 genre match", "+1.43 energy close to target") that is used as the explanation.

**Ranking rule (list of songs).** Score every song in the catalog, sort from highest to lowest score, break ties by energy closeness and then by title, and return the top *k* (default 5).

**Why these weights.** Genre counts twice as much as mood because genre is a stable part of a listener's identity, while mood changes with the situation. Energy is the strongest numeric signal in this dataset, so it gets the largest numeric weight. Together the numeric features (3.75 points) outweigh a genre match (2.0), so a song from a different genre that sounds very close can still beat a same-genre song that sounds wrong. Discovery is kept small so it only breaks ties toward lesser-known songs.

### Expected Biases

- **Genre over-prioritization:** a genre match is worth 2 points, so the system may favor a mediocre song in the right genre over a great song that matches the user's mood and sound. Related genres (lofi vs. ambient, pop vs. indie pop) get no partial credit.
- **Uneven catalog:** lofi has 3 songs while most genres have only 1, so lofi fans get more genre-matched options than metal or blues fans.
- **Exact string matching:** moods like "chill", "relaxed" and "peaceful" are treated as completely different, even though listeners would see them as similar.
- **Hand-picked weights and data:** the weights and song values reflect the designer's assumptions, not real listening behavior, and a single user profile only tests one kind of listener.
- **Popularity bias (or its reverse):** with low `discovery`, popular songs keep getting recommended and lesser-known artists stay hidden; with high `discovery`, the opposite happens.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default pop/happy profile (the run also prints a lofi/chill profile for contrast):

```
Loaded songs: 20

================================================================
Profile: pop / happy (default)
================================================================
1. Sunrise City by Neon Echo  [pop, happy]
   Score: 6.42
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.82 vs target 0.80 (+1.47)
     - acousticness 0.18 vs target 0.20 (+0.73)
     - valence 0.84 vs target 0.80 (+0.48)
     - instrumentalness 0.02 vs target 0.05 (+0.48)
     - popularity 88 (+0.25)
2. Gym Hero by Max Pulse  [pop, intense]
   Score: 5.16
     - genre match (+2.00)
     - energy 0.93 vs target 0.80 (+1.30)
     - acousticness 0.05 vs target 0.20 (+0.64)
     - valence 0.77 vs target 0.80 (+0.48)
     - instrumentalness 0.01 vs target 0.05 (+0.48)
     - popularity 92 (+0.25)
3. Rooftop Lights by Indigo Parade  [indie pop, happy]
   Score: 4.32
     - mood match (+1.00)
     - energy 0.76 vs target 0.80 (+1.44)
     - acousticness 0.35 vs target 0.20 (+0.64)
     - valence 0.81 vs target 0.80 (+0.49)
     - instrumentalness 0.05 vs target 0.05 (+0.50)
     - popularity 67 (+0.25)
4. Fuego Lento by Sol Rivera  [latin, playful]
   Score: 3.29
     - energy 0.74 vs target 0.80 (+1.41)
     - acousticness 0.30 vs target 0.20 (+0.68)
     - valence 0.88 vs target 0.80 (+0.46)
     - instrumentalness 0.04 vs target 0.05 (+0.49)
     - popularity 80 (+0.25)
5. Concrete Crown by Verse Theory  [hip hop, confident]
   Score: 3.27
     - energy 0.78 vs target 0.80 (+1.47)
     - acousticness 0.08 vs target 0.20 (+0.66)
     - valence 0.62 vs target 0.80 (+0.41)
     - instrumentalness 0.00 vs target 0.05 (+0.47)
     - popularity 83 (+0.25)

================================================================
Profile: lofi / chill
================================================================
1. Midnight Coding by LoRoom  [lofi, chill]
   Score: 6.36
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.42 vs target 0.40 (+1.47)
     - acousticness 0.71 vs target 0.80 (+0.68)
     - valence 0.56 vs target 0.60 (+0.48)
     - instrumentalness 0.85 vs target 0.80 (+0.48)
     - popularity 54 (+0.25)
2. Library Rain by Paper Lanterns  [lofi, chill]
   Score: 6.33
     ...
3. Focus Flow by LoRoom  [lofi, focused]
   Score: 5.44
     ...
4. Spacewalk Thoughts by Orbit Bloom  [ambient, chill]
   Score: 4.13
     ...
5. Coffee Shop Stories by Slow Stereo  [jazz, relaxed]
   Score: 3.13
     ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Stress test: 7 user profiles

`src/main.py` runs three "normal" profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and four adversarial edge cases designed to trick the scoring logic:

- **Sad but Hyped:** blues + sad mood, but energy 0.9 (the only sad song in the catalog is low energy)
- **Genre Ghost:** k-pop + "dreamy", neither of which exists in the catalog
- **Acoustic Raver:** EDM + euphoric, but wants fully acoustic, instrumental songs
- **Hidden Gem Hunter:** no genre or mood, all targets at 0.5, discovery 1.0

Full output of `python -m src.main`:

```
Loaded songs: 20

================================================================
Profile: High-Energy Pop (default)
================================================================
1. Sunrise City by Neon Echo  [pop, happy]
   Score: 6.42
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.82 vs target 0.80 (+1.47)
     - acousticness 0.18 vs target 0.20 (+0.73)
     - valence 0.84 vs target 0.80 (+0.48)
     - instrumentalness 0.02 vs target 0.05 (+0.48)
     - popularity 88 (+0.25)
2. Gym Hero by Max Pulse  [pop, intense]
   Score: 5.16
     - genre match (+2.00)
     - energy 0.93 vs target 0.80 (+1.30)
     - acousticness 0.05 vs target 0.20 (+0.64)
     - valence 0.77 vs target 0.80 (+0.48)
     - instrumentalness 0.01 vs target 0.05 (+0.48)
     - popularity 92 (+0.25)
3. Rooftop Lights by Indigo Parade  [indie pop, happy]
   Score: 4.32
     - mood match (+1.00)
     - energy 0.76 vs target 0.80 (+1.44)
     - acousticness 0.35 vs target 0.20 (+0.64)
     - valence 0.81 vs target 0.80 (+0.49)
     - instrumentalness 0.05 vs target 0.05 (+0.50)
     - popularity 67 (+0.25)
4. Fuego Lento by Sol Rivera  [latin, playful]
   Score: 3.29
     - energy 0.74 vs target 0.80 (+1.41)
     - acousticness 0.30 vs target 0.20 (+0.68)
     - valence 0.88 vs target 0.80 (+0.46)
     - instrumentalness 0.04 vs target 0.05 (+0.49)
     - popularity 80 (+0.25)
5. Concrete Crown by Verse Theory  [hip hop, confident]
   Score: 3.27
     - energy 0.78 vs target 0.80 (+1.47)
     - acousticness 0.08 vs target 0.20 (+0.66)
     - valence 0.62 vs target 0.80 (+0.41)
     - instrumentalness 0.00 vs target 0.05 (+0.47)
     - popularity 83 (+0.25)

================================================================
Profile: Chill Lofi
================================================================
1. Midnight Coding by LoRoom  [lofi, chill]
   Score: 6.36
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.42 vs target 0.40 (+1.47)
     - acousticness 0.71 vs target 0.80 (+0.68)
     - valence 0.56 vs target 0.60 (+0.48)
     - instrumentalness 0.85 vs target 0.80 (+0.48)
     - popularity 54 (+0.25)
2. Library Rain by Paper Lanterns  [lofi, chill]
   Score: 6.33
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.35 vs target 0.40 (+1.42)
     - acousticness 0.86 vs target 0.80 (+0.71)
     - valence 0.60 vs target 0.60 (+0.50)
     - instrumentalness 0.90 vs target 0.80 (+0.45)
     - popularity 38 (+0.25)
3. Focus Flow by LoRoom  [lofi, focused]
   Score: 5.44
     - genre match (+2.00)
     - energy 0.40 vs target 0.40 (+1.50)
     - acousticness 0.78 vs target 0.80 (+0.73)
     - valence 0.59 vs target 0.60 (+0.49)
     - instrumentalness 0.88 vs target 0.80 (+0.46)
     - popularity 45 (+0.25)
4. Spacewalk Thoughts by Orbit Bloom  [ambient, chill]
   Score: 4.13
     - mood match (+1.00)
     - energy 0.28 vs target 0.40 (+1.32)
     - acousticness 0.92 vs target 0.80 (+0.66)
     - valence 0.65 vs target 0.60 (+0.47)
     - instrumentalness 0.95 vs target 0.80 (+0.43)
     - popularity 22 (+0.25)
5. Coffee Shop Stories by Slow Stereo  [jazz, relaxed]
   Score: 3.13
     - energy 0.37 vs target 0.40 (+1.46)
     - acousticness 0.89 vs target 0.80 (+0.68)
     - valence 0.71 vs target 0.60 (+0.45)
     - instrumentalness 0.40 vs target 0.80 (+0.30)
     - popularity 35 (+0.25)

================================================================
Profile: Deep Intense Rock
================================================================
1. Storm Runner by Voltline  [rock, intense]
   Score: 6.40
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.91 vs target 0.92 (+1.48)
     - acousticness 0.10 vs target 0.10 (+0.75)
     - valence 0.48 vs target 0.35 (+0.43)
     - instrumentalness 0.12 vs target 0.15 (+0.48)
     - popularity 71 (+0.25)
2. Gym Hero by Max Pulse  [pop, intense]
   Score: 4.17
     - mood match (+1.00)
     - energy 0.93 vs target 0.92 (+1.48)
     - acousticness 0.05 vs target 0.10 (+0.71)
     - valence 0.77 vs target 0.35 (+0.29)
     - instrumentalness 0.01 vs target 0.15 (+0.43)
     - popularity 92 (+0.25)
3. Iron Requiem by Grave Hollow  [metal, angry]
   Score: 3.30
     - energy 0.97 vs target 0.92 (+1.43)
     - acousticness 0.02 vs target 0.10 (+0.69)
     - valence 0.22 vs target 0.35 (+0.43)
     - instrumentalness 0.15 vs target 0.15 (+0.50)
     - popularity 41 (+0.25)
4. Concrete Crown by Verse Theory  [hip hop, confident]
   Score: 3.06
     - energy 0.78 vs target 0.92 (+1.29)
     - acousticness 0.08 vs target 0.10 (+0.73)
     - valence 0.62 vs target 0.35 (+0.36)
     - instrumentalness 0.00 vs target 0.15 (+0.42)
     - popularity 83 (+0.25)
5. Sunrise City by Neon Echo  [pop, happy]
   Score: 2.98
     - energy 0.82 vs target 0.92 (+1.35)
     - acousticness 0.18 vs target 0.10 (+0.69)
     - valence 0.84 vs target 0.35 (+0.26)
     - instrumentalness 0.02 vs target 0.15 (+0.43)
     - popularity 88 (+0.25)

================================================================
Profile: Edge case: Sad but Hyped
================================================================
1. Empty Station Blues by Hank Marlowe  [blues, sad]
   Score: 5.30
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.38 vs target 0.90 (+0.72)
     - acousticness 0.75 vs target 0.20 (+0.34)
     - valence 0.18 vs target 0.20 (+0.49)
     - instrumentalness 0.20 vs target 0.20 (+0.50)
     - popularity 15 (+0.25)
2. Storm Runner by Voltline  [rock, intense]
   Score: 3.23
     - energy 0.91 vs target 0.90 (+1.48)
     - acousticness 0.10 vs target 0.20 (+0.68)
     - valence 0.48 vs target 0.20 (+0.36)
     - instrumentalness 0.12 vs target 0.20 (+0.46)
     - popularity 71 (+0.25)
3. Iron Requiem by Grave Hollow  [metal, angry]
   Score: 3.23
     - energy 0.97 vs target 0.90 (+1.40)
     - acousticness 0.02 vs target 0.20 (+0.61)
     - valence 0.22 vs target 0.20 (+0.49)
     - instrumentalness 0.15 vs target 0.20 (+0.47)
     - popularity 41 (+0.25)
4. Gym Hero by Max Pulse  [pop, intense]
   Score: 2.96
     - energy 0.93 vs target 0.90 (+1.46)
     - acousticness 0.05 vs target 0.20 (+0.64)
     - valence 0.77 vs target 0.20 (+0.21)
     - instrumentalness 0.01 vs target 0.20 (+0.41)
     - popularity 92 (+0.25)
5. Sunrise City by Neon Echo  [pop, happy]
   Score: 2.96
     - energy 0.82 vs target 0.90 (+1.38)
     - acousticness 0.18 vs target 0.20 (+0.73)
     - valence 0.84 vs target 0.20 (+0.18)
     - instrumentalness 0.02 vs target 0.20 (+0.41)
     - popularity 88 (+0.25)

================================================================
Profile: Edge case: Genre Ghost
================================================================
1. Fuego Lento by Sol Rivera  [latin, playful]
   Score: 3.25
     - energy 0.74 vs target 0.65 (+1.36)
     - acousticness 0.30 vs target 0.30 (+0.75)
     - valence 0.88 vs target 0.70 (+0.41)
     - instrumentalness 0.04 vs target 0.10 (+0.47)
     - popularity 80 (+0.25)
2. Island Hours by Roots Harbor  [reggae, uplifting]
   Score: 3.23
     - energy 0.60 vs target 0.65 (+1.42)
     - acousticness 0.45 vs target 0.30 (+0.64)
     - valence 0.86 vs target 0.70 (+0.42)
     - instrumentalness 0.10 vs target 0.10 (+0.50)
     - popularity 33 (+0.25)
3. Rooftop Lights by Indigo Parade  [indie pop, happy]
   Score: 3.22
     - energy 0.76 vs target 0.65 (+1.33)
     - acousticness 0.35 vs target 0.30 (+0.71)
     - valence 0.81 vs target 0.70 (+0.44)
     - instrumentalness 0.05 vs target 0.10 (+0.47)
     - popularity 67 (+0.25)
4. Velvet Hours by Amara Lane  [r&b, romantic]
   Score: 3.07
     - energy 0.48 vs target 0.65 (+1.24)
     - acousticness 0.40 vs target 0.30 (+0.67)
     - valence 0.58 vs target 0.70 (+0.44)
     - instrumentalness 0.02 vs target 0.10 (+0.46)
     - popularity 62 (+0.25)
5. Concrete Crown by Verse Theory  [hip hop, confident]
   Score: 3.05
     - energy 0.78 vs target 0.65 (+1.30)
     - acousticness 0.08 vs target 0.30 (+0.58)
     - valence 0.62 vs target 0.70 (+0.46)
     - instrumentalness 0.00 vs target 0.10 (+0.45)
     - popularity 83 (+0.25)

================================================================
Profile: Edge case: Acoustic Raver
================================================================
1. Neon Overdrive by Pulsewave  [edm, euphoric]
   Score: 5.74
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.96 vs target 0.95 (+1.48)
     - acousticness 0.03 vs target 0.95 (+0.06)
     - valence 0.73 vs target 0.75 (+0.49)
     - instrumentalness 0.80 vs target 0.90 (+0.45)
     - popularity 78 (+0.25)
2. Library Rain by Paper Lanterns  [lofi, chill]
   Score: 2.46
     - energy 0.35 vs target 0.95 (+0.60)
     - acousticness 0.86 vs target 0.95 (+0.68)
     - valence 0.60 vs target 0.75 (+0.42)
     - instrumentalness 0.90 vs target 0.90 (+0.50)
     - popularity 38 (+0.25)
3. Focus Flow by LoRoom  [lofi, focused]
   Score: 2.46
     - energy 0.40 vs target 0.95 (+0.68)
     - acousticness 0.78 vs target 0.95 (+0.62)
     - valence 0.59 vs target 0.75 (+0.42)
     - instrumentalness 0.88 vs target 0.90 (+0.49)
     - popularity 45 (+0.25)
4. Night Drive Loop by Neon Echo  [synthwave, moody]
   Score: 2.42
     - energy 0.75 vs target 0.95 (+1.20)
     - acousticness 0.22 vs target 0.95 (+0.20)
     - valence 0.49 vs target 0.75 (+0.37)
     - instrumentalness 0.70 vs target 0.90 (+0.40)
     - popularity 60 (+0.25)
5. Midnight Coding by LoRoom  [lofi, chill]
   Score: 2.40
     - energy 0.42 vs target 0.95 (+0.70)
     - acousticness 0.71 vs target 0.95 (+0.57)
     - valence 0.56 vs target 0.75 (+0.41)
     - instrumentalness 0.85 vs target 0.90 (+0.47)
     - popularity 54 (+0.25)

================================================================
Profile: Edge case: Hidden Gem Hunter
================================================================
1. Velvet Hours by Amara Lane  [r&b, romantic]
   Score: 3.06
     - energy 0.48 vs target 0.50 (+1.47)
     - acousticness 0.40 vs target 0.50 (+0.68)
     - valence 0.58 vs target 0.50 (+0.46)
     - instrumentalness 0.02 vs target 0.50 (+0.26)
     - popularity 62 (+0.19)
2. Island Hours by Roots Harbor  [reggae, uplifting]
   Score: 3.02
     - energy 0.60 vs target 0.50 (+1.35)
     - acousticness 0.45 vs target 0.50 (+0.71)
     - valence 0.86 vs target 0.50 (+0.32)
     - instrumentalness 0.10 vs target 0.50 (+0.30)
     - popularity 33 (+0.33)
3. Dusty Porch Swing by Willow Creek  [country, nostalgic]
   Score: 3.00
     - energy 0.52 vs target 0.50 (+1.47)
     - acousticness 0.68 vs target 0.50 (+0.61)
     - valence 0.70 vs target 0.50 (+0.40)
     - instrumentalness 0.03 vs target 0.50 (+0.27)
     - popularity 49 (+0.26)
4. Midnight Coding by LoRoom  [lofi, chill]
   Score: 3.00
     - energy 0.42 vs target 0.50 (+1.38)
     - acousticness 0.71 vs target 0.50 (+0.59)
     - valence 0.56 vs target 0.50 (+0.47)
     - instrumentalness 0.85 vs target 0.50 (+0.33)
     - popularity 54 (+0.23)
5. Empty Station Blues by Hank Marlowe  [blues, sad]
   Score: 3.00
     - energy 0.38 vs target 0.50 (+1.32)
     - acousticness 0.75 vs target 0.50 (+0.56)
     - valence 0.18 vs target 0.50 (+0.34)
     - instrumentalness 0.20 vs target 0.50 (+0.35)
     - popularity 15 (+0.42)
```

### Experiment: weight shift (energy x2, genre x0.5)

Temporarily changed `ENERGY_WEIGHT` 1.5 → 3.0 and `GENRE_WEIGHT` 2.0 → 1.0 (max score stays valid: 6.75 → 7.25, and every term is still ≥ 0). Top 5 per profile:

| Profile | Baseline top 5 | Energy x2, genre x0.5 |
|---|---|---|
| High-Energy Pop | Sunrise City, Gym Hero, Rooftop Lights, Fuego Lento, Concrete Crown | Sunrise City, **Rooftop Lights**, Gym Hero, Concrete Crown, Fuego Lento |
| Chill Lofi | Midnight Coding, Library Rain, Focus Flow, Spacewalk Thoughts, Coffee Shop Stories | same order (gap to Spacewalk shrinks 1.31 → 0.49) |
| Deep Intense Rock | Storm Runner, Gym Hero, Iron Requiem, Concrete Crown, Sunrise City | same order |
| Sad but Hyped | Empty Station Blues (5.30), Storm Runner (3.23), ... | Empty Station Blues (5.02), Storm Runner (4.71), ... |
| Acoustic Raver | Neon Overdrive, **Library Rain, Focus Flow**, Night Drive Loop, Midnight Coding | Neon Overdrive, **Gym Hero, Storm Runner**, Night Drive Loop, Iron Requiem |

**Result: different, and mostly more accurate.** Rooftop Lights (indie pop, *happy*) now beats Gym Hero (pop, *intense*) for the happy-pop listener, which feels right. The Acoustic Raver's list switches from quiet lofi tracks to actual high-energy songs. The change didn't fix everything, though: Empty Station Blues (energy 0.38) still wins for a listener who asked for energy 0.9, because genre and mood together still outweigh the energy gap. The weights were restored to the baseline afterwards.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



