from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from .forms import EncryptionForm, DecryptionForm
from .encryption_module import encrypt_text_to_midi, decrypt_text_from_midi

def encryption(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST, request.FILES)
        if form.is_valid():
            text_to_encrypt = form.cleaned_data['text_to_encrypt']
            uploaded_file = request.FILES['midi_file']
            
            # Call the encryption function
            encrypted_midi_path = encrypt_text_to_midi(text_to_encrypt, uploaded_file)

            # Provide the encrypted file to the user for download
            response = redirect('encryption_result')
            response['Location'] += f'?encrypted_file={encrypted_midi_path}'
            return response

    else:
        form = EncryptionForm()

    return render(request, 'encryption.html', {'encryption_form': form})

def decryption(request):
    if request.method == 'POST':
        form = DecryptionForm(request.POST, request.FILES)
        
        if form.is_valid():
            if 'midi_file' in request.FILES:
            # Get the uploaded encrypted MIDI file from the request.FILES dictionary
                uploaded_file = request.FILES['midi_file']
                
                # Call your decryption function with uploaded_file
                decrypted_text = decrypt_text_from_midi(uploaded_file)
                
                return render(request, 'decryption.html', {'decryption_form':form, 'result': f"Decrypted Text: {decrypted_text}"})
            else:
                return render(request, 'decryption.html', {'decryption_form': form, 'error_message': 'No file uploaded.'})

    else:
        form = DecryptionForm()

    return render(request, 'decryption.html', {'decryption_form': form})

def HomePage(request):
    return render(request, 'index.html')

# Temporary change in encryption_result view
def encryption_result(request):
    encrypted_file_path = request.GET.get('encrypted_file', '')

    if encrypted_file_path:
        try:
            # Use FileResponse directly
            response = FileResponse(open(encrypted_file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename=Encrypted_File.mid'
            return response
        except FileNotFoundError:
            return render(request, 'encryption_result.html', {'error_message': 'File not found'})
    else:
        return render(request, 'encryption_result.html', {'error_message': 'File not found'})

