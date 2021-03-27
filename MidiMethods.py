from mido import MidiFile
import diff_module


def mash_up(first_track, second_track):
    del first_track.tracks[4]

    first_track.tracks.append(second_track.tracks[4])
    first_track.tracks.append(second_track.tracks[5])

    first_track.save('mashup.mid')


def delete_empty_tracks(midi_file):
    del midi_file.tracks[0]
    midi_file.save("without_empty_track.mid")


def show_track_messages(track):
    print(track)
    for x, msg in enumerate(track):
        print(str(x + 1) + " " + str(msg))


def show_tracks(mid):
    for track in mid.tracks:
        print(track)


def main():
    origin = MidiFile("origin.mid", clip=True)  # clip=True normalizes all note velocities above 127 to 127.
    modified = MidiFile("modified.mid", clip=True)
    diff_module.main_diff(origin, modified)


if __name__ == '__main__':
    main()
