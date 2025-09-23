import numpy as np
import pygame
import threading
import platform


class Sound:

    FREQ_C = 261.63  # Sound for ド(C)
    FREQ_CS = 277.18
    FREQ_D = 293.66  # Sound for レ(D)
    FREQ_DS = 311.13
    FREQ_E = 329.63  # Sound for ミ(E)
    FREQ_F = 349.23  # Sound for ファ(F)
    FREQ_FS = 369.99
    FREQ_G = 392.00  # Sound for ソ(G)
    FREQ_GS = 415.30
    FREQ_A = 440.00  # Sound for ラ(A)
    FREQ_AS = 466.16
    FREQ_B = 493.88  # Sound for シ(B)

    def __init__(self):
        self.__sample_rate = 44100

        # Sound for coins
        self.__coin_durations = (0.1, 0.7)
        coin_frequencies = (self.FREQ_B * 2, self.FREQ_E * 4)
        coin_fades = (False, True)
        self.__coin_sounds = self._make_sound(coin_frequencies, self.__coin_durations, coin_fades)

        # Sound for mushrooms
        self.__item_durations = [0.04] * 8
        item_frequencies = (self.FREQ_C, self.FREQ_GS, self.FREQ_CS, self.FREQ_D, self.FREQ_AS, self.FREQ_DS, self.FREQ_AS)
        self.__item_sounds = self._make_sound(item_frequencies, self.__item_durations, [False] * 8)
        
        # Sound for power up
        power_frequencies = (
            self.FREQ_C * 2, self.FREQ_G, self.FREQ_C * 2, self.FREQ_E * 2, self.FREQ_G * 2, self.FREQ_C * 4,
            self.FREQ_G * 2, self.FREQ_GS, self.FREQ_C * 2, self.FREQ_DS * 2, self.FREQ_GS * 2, self.FREQ_E * 2,
            self.FREQ_A * 2, self.FREQ_C * 4, self.FREQ_DS * 4, self.FREQ_GS * 4, self.FREQ_DS * 4, self.FREQ_AS,
            self.FREQ_D * 2, self.FREQ_F * 2, self.FREQ_AS * 2, self.FREQ_F * 2, self.FREQ_B * 2, self.FREQ_D * 4, 
            self.FREQ_AS * 4, self.FREQ_D * 4
        )
        self.__power_durations = [0.05] * len(power_frequencies)
        self.__power_sounds = self._make_sound(power_frequencies, self.__power_durations, [False] * len(self.__power_durations))
        
        # Sound for Clear game
        self.__clear_durations = [0.2] * len(power_frequencies)
        self.__clear_sounds = self._make_sound(power_frequencies, self.__clear_durations, [False] * len(self.__power_durations))
        
        # Sound for a fire ball
        fire_frequencies = (self.FREQ_G, self.FREQ_G * 2, self.FREQ_G * 4)
        self.__fire_durations = [0.02] * len(fire_frequencies)
        self.__fire_sounds = self._make_sound(fire_frequencies, self.__fire_durations, [False] * len(self.__fire_durations))
        
        # Sound for 1 UP
        oneup_frequencies = (self.FREQ_E * 4, self.FREQ_G * 4, self.FREQ_E * 8, self.FREQ_C * 8, self.FREQ_D * 8, self.FREQ_G * 8)
        self.__oneup_durations = [0.1, 0.1, 0.1, 0.1, 0.1, 0.25] 
        self.__oneup_sounds = self._make_sound(oneup_frequencies, self.__oneup_durations, [False, False, False, False, False, False, True])
        
        # TODO: Sound for BGM
        # TODO: Sound for Star Mario
        # TODO: Sound for defeating enemies
        # TODO: Sound for Mario getting damaged
        
    def _make_square_sound(self, frequency, duration, fadeout=False):
        """Generate a sawtooth sound"""
        t = np.linspace(0, duration, int(self.__sample_rate * duration), endpoint=False)
        
        # Create a wave
        waveform = 0.125 * np.sign(np.sin(2 * np.pi * frequency * t))

        if fadeout:
            waveform *= np.exp(-5 * t)
        
        if platform.system() == 'Windows':
            # For windows
            mono = (waveform * 32767).astype(np.int16)
            stereo = np.column_stack((mono, mono))  # duplicate to L/R channels
            return pygame.sndarray.make_sound(stereo)
        else:
            # For mac
            return pygame.sndarray.make_sound(((waveform * 32767)).astype(np.int16))
    
    def _make_sound(self, freqs, durs, fades):
        return [self._make_square_sound(freq, dur, fade) for freq, dur, fade in zip(freqs, durs, fades)]
    
    def play_sound_asnync(self, func):
        threading.Thread(target=func).start()

    def play_sounds(self, sounds, durations):
         for sound, dur in zip(sounds, durations):
            sound.play()
            pygame.time.wait(int(dur * 1000))       

    def play_coin(self):
        self.play_sounds(self.__coin_sounds, self.__coin_durations)
    
    def play_item(self):
        self.play_sounds(self.__item_sounds, self.__item_durations)
        
    def play_power(self):
        self.play_sounds(self.__power_sounds, self.__power_durations)
    
    def play_clear(self):
        self.play_sounds(self.__clear_sounds, self.__clear_durations)
    
    def play_fire(self):
        self.play_sounds(self.__fire_sounds, self.__fire_durations)
    
    def play_oneup(self):
        self.play_sounds(self.__oneup_sounds, self.__oneup_durations)
        