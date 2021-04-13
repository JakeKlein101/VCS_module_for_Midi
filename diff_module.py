from mido import MidiFile


def send_to_diff(latest_file_path, second_to_last_file_path):
    """
    Parses the file paths to the MIDI files into MidiFile objects and send those objects to the main_diff function
    to operate on them.
    """
    lastest_file = MidiFile(latest_file_path, clip=True)  # clip=True might cause bugs in the future so watch out!!!!
    second_to_last_file = MidiFile(second_to_last_file_path, clip=True)
    main_diff(lastest_file, second_to_last_file)


def main_diff(latest_file, second_to_last_file):  # TODO: Make it do something.
    print(latest_file.tracks)
    print(second_to_last_file.tracks)

