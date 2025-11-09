from flask import Flask, render_template, request
app = Flask(__name__)

def to_binary(n, bits=8):
    return format(n, '0{}b'.format(bits))

def build_tables():
    # Pisah tabel ASCII menjadi kategori
    sections = {
        'Uppercase A–M': [],
        'Uppercase N–Z': [],
        'Lowercase a–m': [],
        'Lowercase n–z': [],
        'Digits (0-9)': [],
        'Punctuation & Symbols': []
    }

    for code in range(32, 127):  # printable ASCII (spasi sampai ~)
        ch = chr(code)
        entry = {
            'char': ch,
            'decimal': code,
            'binary': to_binary(code, 8),
            'hex': format(code, '02X')
        }

        # ✅ Uppercase A–Z
        if 'A' <= ch <= 'Z':
            if 'A' <= ch <= 'M':
                sections['Uppercase A–M'].append(entry)
            else:
                sections['Uppercase N–Z'].append(entry)

        # ✅ Lowercase a–z
        elif 'a' <= ch <= 'z':
            if 'a' <= ch <= 'm':
                sections['Lowercase a–m'].append(entry)
            else:
                sections['Lowercase n–z'].append(entry)

        # ✅ Digit 0–9
        elif '0' <= ch <= '9':
            sections['Digits (0-9)'].append(entry)

        # ✅ Punctuation & Symbols
        else:
            sections['Punctuation & Symbols'].append(entry)

    return sections


def text_to_binary(text, bits=8, sep=' '):
    out = []
    for ch in text:
        code = ord(ch)
        # Sesuaikan bit jika karakter butuh lebih dari 8 bit
        b = format(code, 'b')
        bits_needed = max(bits, len(b))
        binary = format(code, '0{}b'.format(bits_needed))

        out.append({
            'char': ch,
            'decimal': code,
            'binary': binary,
            'hex': format(code, '02X')
        })
    return out


@app.route('/', methods=['GET', 'POST'])
def index():
    sections = build_tables()
    input_text = ''
    converted = []

    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        converted = text_to_binary(input_text)

    return render_template(
        'index.html',
        sections=sections,
        input_text=input_text,
        converted=converted
    )


if __name__ == '__main__':
    app.run(debug=True)
