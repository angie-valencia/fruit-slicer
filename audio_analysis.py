import mido
import os

class AnalyseurMIDI:
    def __init__(self, chemin_midi):
        if not os.path.exists(chemin_midi):
            raise FileNotFoundError(f"Fichier MIDI non trouvé: {chemin_midi}")
        
        self.mid = mido.MidiFile(chemin_midi)
        self.duree = self.mid.length
        self.notes_evenements = []
        
        # --- RÉGLAGES DES FILTRES ---
        self.VELOCITY_MIN = 60    # Ignore les notes "douces" (0-127)
        self.COOLDOWN = 0.2       # Temps minimum (en sec) entre deux fruits
        # ----------------------------

        self._analyser_notes()

    def _analyser_notes(self):
        temps_cumule = 0
        dernier_temps_spawn = -1.0
        
        for msg in self.mid:
            temps_cumule += msg.time 
            
            # FILTRE 1 : On ne prend que les notes assez fortes (Velocity)
            if msg.type == 'note_on' and msg.velocity >= self.VELOCITY_MIN:
                
                # FILTRE 2 : Cooldown (évite que 10 fruits apparaissent en même temps)
                if temps_cumule - dernier_temps_spawn >= self.COOLDOWN:
                    self.notes_evenements.append({
                        'temps': temps_cumule,
                        'note': msg.note,
                        'colonne': msg.note % 4 
                    })
                    dernier_temps_spawn = temps_cumule
        
        self.notes_evenements.sort(key=lambda x: x['temps'])
        print(f"[FILTRAGE] {len(self.notes_evenements)} fruits conservés sur la partition.")

    def get_fruits_precalcules(self, anticipation=1.8):
        fruits = []
        for n in self.notes_evenements:
            fruits.append({
                'temps_spawn': n['temps'] - anticipation,
                'temps_cible': n['temps'],
                'colonne': n['colonne'],
                'spawned': False
            })
        return fruits