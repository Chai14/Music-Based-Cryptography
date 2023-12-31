import mido
import tempfile
import os
from mido import MidiFile, MidiTrack, Message
import string
import zlib

def text_to_binary(text):
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string

def binary_to_text(binary_string):
    text = ''.join([chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8)])
    return text
    


def encrypt_text_to_midi(text, uploaded_file):
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    try:
        # Load the original MIDI file from the temporary file
        midi_file = MidiFile(temp_file_path)

        # Create a new MIDI track for hiding text
        text_track = MidiTrack()
        midi_file.tracks.append(text_track)

        # Set a constant MIDI note value (e.g., 60 for Middle C)
        midi_note = 60

        # Keep track of time for the new track
        current_time = 0

        # Hide text length in velocity values using LSB method
        binary_length = format(len(text), '08b')
        for char in binary_length:
            new_velocity = int(char)
            text_track.append(Message('note_on', note=midi_note, velocity=new_velocity, time=current_time))
            current_time += 100  # Set the time increment based on your preference

        # Hide text in velocity values using LSB method
        binary_text = text_to_binary(text)
        for char in binary_text:
            new_velocity = int(char)
            text_track.append(Message('note_on', note=midi_note, velocity=new_velocity, time=current_time))
            current_time += 100  # Set the time increment based on your preference

    finally:
        # Clean up: remove the temporary file
        os.remove(temp_file_path)

    # Save the new MIDI file to a different temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='_encrypted.mid') as encrypted_temp_file:
        midi_file.save(encrypted_temp_file.name)
        encrypted_midi_path = encrypted_temp_file.name

    return encrypted_midi_path

def decrypt_text_from_midi(uploaded_file):
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    try:
        # Load encrypted MIDI file from the temporary file
        encrypted_midi_file = MidiFile(temp_file_path)

        # Assume the encrypted text is in the last track
        text_track = encrypted_midi_file.tracks[-1]

        # Extract binary string from velocity values using LSB method
        binary_string = ''
        for msg in text_track:
            if msg.type == 'note_on':
                # Extract the LSB from the velocity value
                lsb = msg.velocity & 1
                binary_string += str(lsb)

        # Convert binary string to text
        decrypted_text = binary_to_text(binary_string)
        decrypted_text = ''.join(char for char in decrypted_text if char in string.printable)
        return decrypted_text

    finally:
        # Clean up: remove the temporary file
        os.remove(temp_file_path)