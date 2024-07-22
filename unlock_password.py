import pikepdf

def crack(orginal_filepath, cracked_filepath):
    pdf = pikepdf.open(orginal_filepath, allow_overwriting_input=True)
    pdf.save(cracked_filepath)
    return 'DONE'