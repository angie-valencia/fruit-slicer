# ============================================
# CALCUL DE DIFFICULTÉ DYNAMIQUE ET SPAWN
# Analyse la complexité musicale et génère les fruits
# ============================================

import numpy as np


def compute_difficulty(frame_index, spectrogram, onset_env):
    """
    Calcule la difficulté à partir d'un frame avec onset detection.
    
    Formule:
        difficulty = 0.4 * spectral_variation 
                   + 0.3 * onset_strength 
                   + 0.2 * intensity 
                   + 0.1 * spectral_density
    
    Args:
        frame_index: Index du frame dans le spectrogramme (0-based)
        spectrogram: Spectrogramme mel (shape: [n_mels, n_frames])
        onset_env: Vecteur onset strength (shape: [n_frames])
    
    Returns:
        Difficulté normalisée entre 0 et 1
    """
    if frame_index < 0 or frame_index >= spectrogram.shape[1]:
        return 0.0
    
    # Intensité normalisée
    frame_spectrum = spectrogram[:, frame_index]
    intensity = np.mean(frame_spectrum)
    intensity_min = np.min(spectrogram)
    intensity_max = np.max(spectrogram)
    intensity_norm = (intensity - intensity_min) / (intensity_max - intensity_min + 1e-6)
    
    # Densité spectrale normalisée
    seuil = 0.3 * np.max(frame_spectrum)
    bins_actifs = np.sum(frame_spectrum > seuil)
    spectral_density = bins_actifs / spectrogram.shape[0]
    
    if frame_index == 0:
        spectral_density_norm = spectral_density
    else:
        all_densities = np.array([
            np.sum(spectrogram[:, i] > 0.3 * np.max(spectrogram[:, i])) / spectrogram.shape[0]
            for i in range(spectrogram.shape[1])
        ])
        dens_min = np.min(all_densities)
        dens_max = np.max(all_densities)
        spectral_density_norm = (spectral_density - dens_min) / (dens_max - dens_min + 1e-6)
    
    # Variation spectrale normalisée
    if frame_index == 0:
        spectral_variation = 0.0
    else:
        prev_spectrum = spectrogram[:, frame_index - 1]
        variation = np.mean(np.abs(frame_spectrum - prev_spectrum))
        all_variations = np.array([
            np.mean(np.abs(spectrogram[:, i] - spectrogram[:, i-1]))
            for i in range(1, spectrogram.shape[1])
        ])
        var_min = np.min(all_variations)
        var_max = np.max(all_variations)
        spectral_variation = (variation - var_min) / (var_max - var_min + 1e-6)
    
    # Onset strength normalisée
    onset_min = np.min(onset_env)
    onset_max = np.max(onset_env)
    onset_norm = (onset_env[frame_index] - onset_min) / (onset_max - onset_min + 1e-6)
    
    # Formule de difficulté
    difficulty = (0.4 * spectral_variation + 
                 0.3 * onset_norm + 
                 0.2 * intensity_norm + 
                 0.1 * spectral_density_norm)
    
    return float(np.clip(difficulty, 0, 1))


def spawn_fruits(beat_index, difficulty, beat_times, sr=22050, hop_length=512, max_fruits_per_beat=5):
    """
    Génère le nombre et le timing des fruits pour un beat donné.
    
    Règles:
    - Minimum 1 fruit par beat
    - spawn_count = 1 + floor(difficulty * 4)
    - Si difficulty > 0.6 : autoriser subdivisions en ½ beat
    - Si difficulty > 0.8 : autoriser subdivisions en ¼ beat
    - Capper le nombre max
    
    Args:
        beat_index: Index du beat (dans le tableau beats de librosa)
        difficulty: Valeur de difficulté (0.0 à 1.0)
        beat_times: Tableau des temps de beats en secondes
        sr: Sample rate
        hop_length: Hop length du spectrogramme
        max_fruits_per_beat: Nombre max de fruits par beat
    
    Returns:
        Liste de temps (en secondes) d'apparition des fruits
    """
    if beat_index >= len(beat_times):
        return []
    
    beat_time = beat_times[beat_index]
    next_beat_time = beat_times[beat_index + 1] if beat_index + 1 < len(beat_times) else beat_time + 0.5
    beat_duration = next_beat_time - beat_time
    
    # Nombre de fruits à générer
    spawn_count = 1 + int(np.floor(difficulty * 4))
    spawn_count = min(spawn_count, max_fruits_per_beat)
    
    # Déterminer la subdivision
    if difficulty > 0.8:
        # ¼ beat (16ème notes)
        subdivision = 4
    elif difficulty > 0.6:
        # ½ beat (8ème notes)
        subdivision = 2
    else:
        # 1 beat (noire)
        subdivision = 1
    
    # Générer les temps d'apparition
    fruit_times = []
    
    if subdivision == 1:
        # 1 fruit au beat
        fruit_times.append(beat_time)
        
        # Fruits supplémentaires répartis aléatoirement
        for _ in range(spawn_count - 1):
            offset = np.random.uniform(0, beat_duration * 0.8)
            fruit_times.append(beat_time + offset)
    else:
        # Subdivision : répartir les fruits sur le beat
        step = beat_duration / subdivision
        positions = []
        
        for i in range(subdivision):
            if len(positions) < spawn_count:
                pos = beat_time + i * step + np.random.uniform(0, step * 0.3)
                positions.append(pos)
        
        # Ajouter des fruits supplémentaires
        for _ in range(spawn_count - len(positions)):
            pos = beat_time + np.random.uniform(0, beat_duration)
            positions.append(pos)
        
        fruit_times = sorted(positions)
    
    return fruit_times


def compute_difficulty_batch(spectrogram, onset_env):
    """
    Calcule la difficulté pour tous les frames.
    
    Formule:
        difficulty = 0.4 * spectral_variation 
                   + 0.3 * onset_strength 
                   + 0.2 * intensity 
                   + 0.1 * spectral_density
    
    Args:
        spectrogram: Spectrogramme mel (shape: [n_mels, n_frames])
        onset_env: Vecteur onset strength (shape: [n_frames])
    
    Returns:
        Array de difficulté (shape: [n_frames])
    """
    n_frames = spectrogram.shape[1]
    difficulty = np.zeros(n_frames)
    
    # Intensité
    intensity = np.mean(spectrogram, axis=0)
    intensity_min = np.min(spectrogram)
    intensity_max = np.max(spectrogram)
    intensity_norm = (intensity - intensity_min) / (intensity_max - intensity_min + 1e-6)
    
    # Densité spectrale
    seuil_local = 0.3 * np.max(spectrogram, axis=0)
    bins_actifs = np.sum(spectrogram > seuil_local, axis=0)
    spectral_density = bins_actifs / spectrogram.shape[0]
    dens_min = np.min(spectral_density)
    dens_max = np.max(spectral_density)
    spectral_density_norm = (spectral_density - dens_min) / (dens_max - dens_min + 1e-6)
    
    # Variation spectrale
    spectral_variation = np.zeros(n_frames)
    for i in range(1, n_frames):
        spectral_variation[i] = np.mean(np.abs(spectrogram[:, i] - spectrogram[:, i-1]))
    var_min = np.min(spectral_variation)
    var_max = np.max(spectral_variation)
    spectral_variation_norm = (spectral_variation - var_min) / (var_max - var_min + 1e-6)
    
    # Onset strength
    onset_min = np.min(onset_env)
    onset_max = np.max(onset_env)
    onset_norm = (onset_env - onset_min) / (onset_max - onset_min + 1e-6)
    
    # Formule
    difficulty = (0.4 * spectral_variation_norm + 
                 0.3 * onset_norm + 
                 0.2 * intensity_norm + 
                 0.1 * spectral_density_norm)
    
    return np.clip(difficulty, 0, 1)
