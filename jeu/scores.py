import os

FICHIER_SCORE = "highscores.txt"

def charger_scores():
    scores = []
    if os.path.exists(FICHIER_SCORE):
        with open(FICHIER_SCORE, "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    scores.append((parts[0], int(parts[1])))
    # Trie par score décroissant et garde le top 5
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:5]

def sauver_score(pseudo, score):
    scores = charger_scores()
    scores.append((pseudo[:3].upper(), score))
    scores.sort(key=lambda x: x[1], reverse=True)
    with open(FICHIER_SCORE, "w") as f:
        for s in scores[:5]:
            f.write(f"{s[0]}:{s[1]}\n")