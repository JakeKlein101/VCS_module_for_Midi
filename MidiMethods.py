import os
from mido import MidiFile


def mash_up(first_track, second_track):
    del first_track.tracks[4]

    first_track.tracks.append(second_track.tracks[4])
    first_track.tracks.append(second_track.tracks[5])

    first_track.save('mashup.mid')


def show_track_messages(track):
    print(track)
    for x, msg in enumerate(track):
        print(str(x + 1) + " " + str(msg))


def show_tracks(mid):
    for track in mid.tracks:
        print(track)


def main():
    mid = MidiFile("untitled.mid", clip=True)  # clip=True normalizes all note velocities above 127 to 127.
    print(mid)
    # show_tracks(mid)
    show_track_messages(mid.tracks[1])


if __name__ == '__main__':
    main()
