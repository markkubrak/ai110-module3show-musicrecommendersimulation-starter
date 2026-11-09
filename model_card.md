# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**Vibenator 6000**: it hunts down songs that fit the vibe you describe.

---

## 2. Intended Use  

**Goal / Task:** The Vibenator 6000 suggests the top 5 songs from a small catalog that best fit a listener's taste. You describe your favorite genre, your mood, and how energetic, acoustic, positive and instrumental you want the music to be. It gives every song a score and shows the best matches, with reasons for each one.

**Assumptions:** It assumes you can describe your taste with a few numbers and labels, and that your taste doesn't change while you're listening. It doesn't know anything about what you've listened to before.

**Intended use:**
- A classroom project for learning how content-based recommenders work.
- Trying out different taste profiles and seeing how the scoring reacts.
- Showing how weights and data choices create bias.

**Not intended for:**
- Real users or a real music app. The catalog is only 20 made-up songs.
- Making decisions about artists, like which songs get promoted or paid. The song values are hand-written, not measured.
- Judging anyone's "real" music taste. A few numbers can't capture that.

---

## 3. How the Model Works  

Think of it like a points game. Every song starts at zero and earns points for how well it fits you.

- **Same genre as your favorite?** +2 points.
- **Same mood?** +1 point.
- **Energy:** up to 1.5 points. The closer the song's energy is to what you want, the more points it gets. A song isn't rewarded for being "more" energetic, only for being *closer* to your target.
- **Acoustic sound:** up to 0.75 points, using the same "closer is better" idea.
- **Happiness (valence) and vocals vs. instrumental:** up to 0.5 points each.
- **Discovery:** up to 0.5 points. If you want hidden gems, less popular songs get a little boost. If you want hits, popular songs get it.

The best possible score is 6.75. After every song is scored, they're sorted from highest to lowest, and the top 5 are shown. Each recommendation lists exactly where its points came from, like "genre match (+2.00)".

**Changes from the starter:** The starter only had genre, mood and energy. I added acousticness, valence, instrumentalness and a popularity-based discovery setting. I also made the score explain itself with a list of reasons.

---

## 4. Data  

- **Size:** 20 songs in `data/songs.csv`. The starter had 10, and I added 10 more.
- **Genres (17):** pop, indie pop, lofi, rock, ambient, jazz, synthwave, hip hop, classical, country, edm, r&b, metal, reggae, folk, latin, blues.
- **Moods (16):** including happy, chill, intense, sad, angry, romantic, nostalgic, euphoric and peaceful. The starter only had positive or calm moods, so I added sad and angry ones.
- **Features per song:** genre, mood, energy, tempo, valence (happiness), danceability, acousticness, plus three I added: instrumentalness, popularity (0–100) and release year.

**Limits:**
- It's tiny. Most genres have only 1 song, while lofi has 3.
- The songs and their numbers are made up, not real measurements.
- Tempo and danceability are stored but not scored, because they mostly repeat what energy already says.
- Nothing about lyrics, language, culture, or what people actually listen to.

---

## 5. Strengths  

- **Clear, opposite tastes work great.** Pop, lofi and rock listeners get completely different top 5 lists, and the #1 song is always the obvious pick.
- **It finds good songs outside your genre.** The lofi listener also gets ambient and jazz songs, which really do fit a study vibe.
- **Every result explains itself.** You can see exactly why a song ranked where it did, which made it easy to spot problems.
- **"Closer is better" scoring works.** A user who wants medium energy isn't pushed toward the loudest songs.

---

## 6. Limitations and Bias 

**Main weakness: an exact genre + mood match can overpower everything else.** A genre match (+2.0) plus a mood match (+1.0) is worth 3 points, while a song that is completely wrong on energy only loses about 0.8 points. In the "Sad but Hyped" test, a user asked for energy 0.9, but the top pick was Empty Station Blues at energy 0.38, simply because it was the only blues/sad song. Matching is also exact text, so "intense" and "angry" count as unrelated: for the Deep Intense Rock listener, Gym Hero (a pop song tagged "intense") ranked above Iron Requiem (a 0.97-energy metal song tagged "angry"). This creates a filter bubble: users mostly see their own genre label, and great songs that sound right but carry a different tag get pushed down.

Other limitations found in testing:

- **Small, uneven catalog:** 20 songs, 17 genres. Lofi has 3 songs, while most genres have only 1, so a blues or metal fan gets one genre match and then filler.
- **Middle-of-the-road users are treated differently:** a user with target energy 0.5 is never more than 0.5 away from any song, so energy barely separates songs for them. A user at 0.9 or 0.1 sees much bigger differences.
- **Discovery is too weak:** with discovery 1.0, the Hidden Gem Hunter's top pick was Velvet Hours (popularity 62), not the obscure songs. The popularity bonus is worth at most 0.5 points, so it rarely changes the order.
- **Missing taste dimensions:** no lyrics, language, artist familiarity, or listening history, and the song values were hand-made rather than measured.

---

## 7. Evaluation  

**Profiles tested** (full terminal output is in the README under "Experiments You Tried"):

- Three normal listeners: **High-Energy Pop**, **Chill Lofi**, **Deep Intense Rock**
- Four edge cases built to trick the scorer: **Sad but Hyped** (sad mood with high energy), **Genre Ghost** (genre and mood not in the catalog), **Acoustic Raver** (EDM but fully acoustic), **Hidden Gem Hunter** (no genre or mood, everything at 0.5, maximum discovery)

I checked whether the #1 song fit the profile, whether the rest of the top 5 "felt" like the same listener, and whether each score's reasons explained the ranking.

**Does it match my intuition?** For the three normal profiles, mostly yes. Sunrise City, Midnight Coding and Storm Runner are the obvious top picks, and the lofi list fills in with ambient and jazz, which a study-music listener would enjoy.

**Why does "Gym Hero" keep showing up?** Gym Hero appears in the top 5 for Happy Pop, Intense Rock *and* Sad but Hyped. In plain terms: the system gives points for each thing a song has in common with you. Gym Hero is labeled "pop", so pop fans get a 2-point bonus. It's also labeled "intense", so rock fans looking for "intense" get a 1-point bonus. And it's extremely high energy, which earns points from anyone who wants loud music. It's a "pretty good at everything" song, so it scores well for lots of people even though it isn't the perfect fit for any of them. A happy-pop listener probably wants Rooftop Lights (happy indie pop) more, but that song loses the 2-point genre bonus because "indie pop" isn't spelled "pop".

**Comparing profiles:**

- **High-Energy Pop vs. Chill Lofi:** the two lists share no songs at all. Pop pulls bright, high-energy, vocal tracks (energy 0.74–0.93), while lofi pulls quiet, acoustic, instrumental tracks (energy 0.28–0.42). This makes sense: their targets are opposite on energy, acousticness and instrumentalness.
- **Chill Lofi vs. Deep Intense Rock:** again no overlap. Rock's list is loud and electric (Storm Runner, Iron Requiem), while lofi's is soft and acoustic. This confirms the profiles can tell "intense rock" from "chill lofi".
- **High-Energy Pop vs. Deep Intense Rock:** these overlap on Gym Hero, Concrete Crown and Sunrise City, because both want high energy and low acousticness. The difference is at the top: Storm Runner wins for rock thanks to its genre and mood matches, and the rock list includes the darker Iron Requiem.
- **Deep Intense Rock vs. Sad but Hyped:** both want loud music, so Storm Runner, Iron Requiem and Gym Hero appear in both. But Sad but Hyped's #1 is a quiet blues song, because the blues + sad label bonus outweighed the energy request. This was the most surprising result.
- **Genre Ghost vs. High-Energy Pop:** with no genre or mood matches available, Genre Ghost's scores are bunched together (3.05–3.25), so its ranking depends on tiny numeric differences. Compare pop's clear 6.42 → 3.27 spread. The system still produces sensible mid-energy, upbeat songs, but with much less confidence.
- **Acoustic Raver vs. Chill Lofi:** surprisingly, three lofi songs land in the Raver's top 5. The Raver asked for acoustic, instrumental songs, and only lofi and ambient songs have those traits. So the contradictory request was resolved in favor of texture rather than energy.
- **Hidden Gem Hunter vs. everyone:** with every target at 0.5 and discovery maxed, almost all songs score about 3.0. The list is essentially arbitrary, which shows that the discovery bonus is too small to steer recommendations by itself.

**Experiment (energy x2, genre x0.5):** Rooftop Lights moved above Gym Hero for the pop listener, and the Acoustic Raver's list switched from lofi songs to genuinely high-energy songs. Both changes feel more accurate. The Sad but Hyped result didn't change, because genre and mood together still outweigh energy. The change made the system less "label-driven" and more "sound-driven".

---

## 8. Future Work  

1. **Partial credit for similar labels.** "Pop" and "indie pop", or "chill" and "peaceful", should earn some points instead of zero. Then a song like Rooftop Lights wouldn't lose to Gym Hero just because of how its genre is spelled.
2. **Rebalance the weights.** My experiment showed that more energy weight and less genre weight gave more accurate results. I'd also make the discovery bonus stronger, since right now it barely changes anything.
3. **More variety in the top 5.** Limit how many songs from the same genre or artist can appear, and add a lot more songs so every genre has real options.

---

## 9. Personal Reflection  

**Biggest learning moment:** Realizing that scoring one song and ranking a list are two separate jobs. At first I thought a recommender just "picks songs". But a score by itself means nothing until you compare it to every other song. Splitting it into `score_song` and `recommend_songs` made the whole thing click. The second big moment was the "Sad but Hyped" test. I asked for high-energy music and got a slow blues song at #1, just because its labels matched. That's when I saw how much my weights decided the results.

**How AI helped, and when I double-checked:** AI was really useful for explaining ideas like collaborative vs. content-based filtering, and for writing code fast. It also suggested new features like popularity and instrumentalness that made the project more interesting. But I still had to check its work. When it edited my README, it couldn't find the "How The System Works" heading at first because the capitalization was different. It also caught that `main.py` imported the recommender the wrong way, which would have crashed `python -m src.main`. And when it changed the default profile to lofi, I had to remember that my class instructions expected pop/happy. AI is fast, but I'm the one who has to know what the assignment and the results should look like.

**What surprised me:** How "real" a few lines of math can feel. It's just adding up points, but the lists honestly looked like something a music app would show me. The lofi list even pulled in ambient and jazz songs on its own, which felt smart. It also surprised me how one song, Gym Hero, kept showing up for different people just by being "pretty good" at everything.

**What I'd try next:** Add fake listening histories for a bunch of users and try collaborative filtering, "people like you also liked...". Then I'd combine it with my content-based scores to make a hybrid, like real apps do. I'd also give partial credit for similar genres and moods.

**How this changed my view of music apps:** I now see that every recommendation app makes choices about what matters more, and those choices can quietly create filter bubbles. When Spotify keeps showing me the same kind of songs, it's probably not because nothing else exists. It's because the system was built to reward what I already like.
