# ============================================
# GESTION DE LA SAUVEGARDE DES SCORES (JSON)
# ============================================

import json
import os
from constantes import NOMBRE_SCORES_A_SAUVER

# Nom du fichier JSON
FICHIER_SCORES = "scores.json"


def charger_scores():
    """
    Charge les meilleurs scores depuis le fichier JSON.
    Retourne: Liste de dictionnaires {"nom": str, "score": int} triée du meilleur au moins bon
    """
    if not os.path.exists(FICHIER_SCORES):
        return []
    
    try:
        with open(FICHIER_SCORES, "r", encoding="utf-8") as fichier:
            scores = json.load(fichier)
            
            # Vérifier que c'est bien une liste
            if not isinstance(scores, list):
                return []
            
            # Trier par score décroissant
            scores.sort(key=lambda x: x.get("score", 0), reverse=True)
            return scores[:NOMBRE_SCORES_A_SAUVER]
    
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Erreur lors du chargement des scores : {e}")
        return []


def sauvegarder_score(nom, score):
    """
    Sauvegarde un nouveau score dans le fichier JSON.
    
    Args:
        nom: Nom du joueur
        score: Score obtenu
    """
    # Charger les scores existants
    scores = charger_scores()
    
    # Ajouter le nouveau score
    scores.append({
        "nom": nom,
        "score": score
    })
    
    # Trier par score décroissant et garder seulement les meilleurs
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:NOMBRE_SCORES_A_SAUVER]
    
    # Sauvegarder dans le fichier JSON
    try:
        with open(FICHIER_SCORES, "w", encoding="utf-8") as fichier:
            json.dump(scores, fichier, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")


def est_dans_top_scores(score):
    """
    Vérifie si un score mérite d'être sauvegardé.
    
    Args:
        score: Score à vérifier
    
    Retourne: True si le score est dans le top 5
    """
    scores = charger_scores()
    
    # Si on a moins de 5 scores, on peut toujours ajouter
    if len(scores) < NOMBRE_SCORES_A_SAUVER:
        return True
    
    # Sinon, vérifier si le score est meilleur que le pire du top 5
    pire_score = scores[-1]["score"]
    return score > pire_score