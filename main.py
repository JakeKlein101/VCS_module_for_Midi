from mido import MidiFile


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
