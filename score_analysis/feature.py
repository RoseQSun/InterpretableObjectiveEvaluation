from music21 import stream, meter, key, interval
import numpy as np


def measure_count(score):
    try:
        return len(score.getElementsByClass(stream.Part)[0].getElementsByClass(stream.Measure))
    except IndexError:
        return None


def time_sig(score):
    try:
        return score.recurse().getElementsByClass(meter.TimeSignature)[0].ratioString
    except IndexError:
        return None


def key_sig(score):
    try:
        b = score.recurse().getElementsByClass(key.Key)[0]
        return b.tonicPitchNameWithCase, b.mode
    except IndexError:
        return None
    

def _strong_beat_pos(timesig):
    _strong_beats_dict = {
        '2/4': [1.0],
        '3/2': [1.0],
        '3/4': [1.0],
        '4/4': [1.0, 3.0],
        '6/8': [1.0, 2.0],
        '9/8': [1.0, 2.0, 3.0],
        '12/8': [1.0, 2.0, 3.0, 4.0]
    }
    x = _strong_beats_dict.get(timesig)
    if x is None:
        return x
    return np.array(x)


def _rests_on_beat(score, timesig=None, strong=True):
    timesig = time_sig(score) if timesig is None else timesig
    event_beats = []  # [n.beat]
    are_rests = [] # [n.isRest]

    for n in score.recurse().notesAndRests:
        event_beats.append(n.beat)
        are_rests.append(n.isRest)

    event_beats = np.array(event_beats)  
    are_rests = np.array(are_rests)     
    rest_beats = event_beats[are_rests]
    strong_array = _strong_beat_pos(timesig)

    events_in_array = np.in1d(event_beats, strong_array)
    rests_in_array = np.in1d(rest_beats, strong_array)

    all_strong_beats = event_beats[events_in_array if strong else ~events_in_array]
    rest_strong_beats = rest_beats[rests_in_array if strong else ~rests_in_array]

    if len(all_strong_beats) == 0:
        return None

    return len(rest_strong_beats) / len(all_strong_beats)


def rests_on_strong_ratio(score, keysig=None):
    return _rests_on_beat(score, keysig, strong=True)


def rests_on_weak_ratio(score, keysig=None):
    return _rests_on_beat(score, keysig, strong=False)


def _lengths_on_beat(score, timesig=None, strong=True):
    timesig = time_sig(score) if timesig is None else timesig
    event_beats = []  # [n.beat]
    event_lengths = []

    for n in score.recurse().notesAndRests:
        event_beats.append(n.beat)
        event_lengths.append(n.quarterLength)

    event_beats = np.array(event_beats)  
    event_lengths = np.array(event_lengths)     
    strong_array = _strong_beat_pos(timesig)

    events_in_array = np.where(np.in1d(event_beats, strong_array))[0]

    lengths = event_lengths[events_in_array if strong else ~events_in_array]

    if len(lengths) == 0:
        return None

    return lengths
 
def lengths_on_strong(score, keysig=None):
    return _lengths_on_beat(score, keysig, strong=True)


def lengths_on_weak(score, keysig=None):
    return _lengths_on_beat(score, keysig, strong=False)


def _scale_degrees_on_beat(score, keysig=None, timesig=None, strong=True):
    keysig = key_sig(score) if keysig is None else keysig
    if keysig is None: return None
    timesig = time_sig(score) if timesig is None else timesig

    beats = []
    degrees = []
    k = key.Key(*keysig)
    strong_array = _strong_beat_pos(timesig)

    for i in score.parts:
        for j in i.flat.getElementsByClass("Note"):
            degree, accidental = k.getScaleDegreeAndAccidentalFromPitch(j.pitch)
            if accidental is None:
                degrees.append(degree)
                beats.append(j.beat)
    degrees = np.array(degrees)
    beats = np.array(beats)

    events_in_array = np.where(np.in1d(beats, strong_array))[0]
    return degrees[events_in_array if strong else ~events_in_array]


def scale_degrees_on_strong(score, keysig=None, timesig=None):
    return _scale_degrees_on_beat(score, keysig=keysig, timesig=timesig, strong=True)


def scale_degrees_on_weak(score, keysig=None, timesig=None):
    return _scale_degrees_on_beat(score, keysig=keysig, timesig=timesig, strong=False)


def pitch_intervals(score):
    intlist = []
    for i in score.recurse().getElementsByClass('Note'):
        if i.next('Note') is None:
            continue
        thisint = interval.Interval(i, i.next('Note'))
        intlist.append(thisint.semitones)
    return np.array(intlist)


def average_interval(intervals):
    return np.mean(np.abs(intervals))


def direction_change_count(intervals):
    zero_removed = intervals[intervals != 0]
    return (np.diff(np.sign(zero_removed)) != 0).sum()