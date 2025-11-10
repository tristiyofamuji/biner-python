from flask import Flask, render_template, request

app = Flask(__name__)


# =======================================================
#          FUNGSI KONVERSI DETAIL
# =======================================================

def to_binary_steps(decimal):
    """Langkah pembagian berulang untuk Decimal → Binary."""
    if decimal == 0:
        return "0 ÷ 2 = 0 sisa 0\nBinary = 0"

    steps = []
    n = decimal
    while n > 0:
        q = n // 2
        r = n % 2
        steps.append(f"{n} ÷ 2 = {q} sisa {r}")
        n = q

    binary = format(decimal, '08b')
    return "\n".join(steps) + f"\nBinary = {binary}"


def to_octal_steps(decimal):
    """Langkah pembagian berulang untuk Decimal → Octal."""
    if decimal == 0:
        return "0 ÷ 8 = 0 sisa 0\nOctal = 0"

    steps = []
    n = decimal
    result = ""

    while n > 0:
        q = n // 8
        r = n % 8
        steps.append(f"{n} ÷ 8 = {q} sisa {r}")
        result = str(r) + result
        n = q

    return "\n".join(steps) + f"\nOctal = {result}"


def to_hex_steps(decimal):
    """Langkah pembagian berulang untuk Decimal → Hex."""
    hex_digits = "0123456789ABCDEF"
    if decimal == 0:
        return "0 ÷ 16 = 0 sisa 0 (0)\nHex = 0"

    steps = []
    n = decimal
    result = ""

    while n > 0:
        q = n // 16
        r = n % 16
        steps.append(f"{n} ÷ 16 = {q} sisa {r} ({hex_digits[r]})")
        result = hex_digits[r] + result
        n = q

    return "\n".join(steps) + f"\nHex = {result}"


def octal_to_decimal_steps(octal_str):
    """Konversi Octal → Decimal menggunakan rumus pangkat 8."""
    total = 0
    steps = []
    length = len(octal_str)

    for i, digit in enumerate(octal_str):
        d = int(digit)
        power = length - i - 1
        calc = d * (8 ** power)
        steps.append(f"{digit} × 8^{power} = {calc}")
        total += calc

    return "\n".join(steps) + f"\nTotal = {total}"


def hex_to_decimal_steps(hex_str):
    """Konversi Hex → Decimal menggunakan rumus pangkat 16."""
    hex_digits = "0123456789ABCDEF"
    hex_str = hex_str.upper()

    total = 0
    steps = []
    length = len(hex_str)

    for i, digit in enumerate(hex_str):
        value = hex_digits.index(digit)
        power = length - i - 1
        calc = value * (16 ** power)
        steps.append(f"{digit} × 16^{power} = {calc}")
        total += calc

    return "\n".join(steps) + f"\nTotal = {total}"


# =======================================================
#          BANGUN TABEL ASCII
# =======================================================

def build_sections():
    sections = {
        "Uppercase A–M": [],
        "Uppercase N–Z": [],
        "Lowercase a–m": [],
        "Lowercase n–z": [],
        "Digits (0-9)": [],
        "Punctuation & Symbols": []
    }

    for code in range(32, 127):
        ch = chr(code)
        entry = {
            "char": ch,
            "decimal": code,
            "binary": format(code, "08b"),
            "octal": format(code, "03o"),
            "hex": format(code, "02X")
        }

        if "A" <= ch <= "M":
            sections["Uppercase A–M"].append(entry)
        elif "N" <= ch <= "Z":
            sections["Uppercase N–Z"].append(entry)
        elif "a" <= ch <= "m":
            sections["Lowercase a–m"].append(entry)
        elif "n" <= ch <= "z":
            sections["Lowercase n–z"].append(entry)
        elif "0" <= ch <= "9":
            sections["Digits (0-9)"].append(entry)
        else:
            sections["Punctuation & Symbols"].append(entry)

    return sections


# =======================================================
#          KONVERSI TEKS
# =======================================================

def convert_text(text):
    output = []

    for ch in text:
        code = ord(ch)
        hex_value = format(code, "X")
        oct_value = format(code, "o")

        output.append({
            "char": ch,
            "decimal": code,
            "binary": format(code, "08b"),
            "octal": oct_value,
            "hex": format(code, "X"),
            "calc_binary": to_binary_steps(code),
            "calc_octal": to_octal_steps(code),
            "calc_hex": to_hex_steps(code),
            "calc_octal_to_dec": octal_to_decimal_steps(oct_value),
            "calc_hex_to_dec": hex_to_decimal_steps(hex_value)
        })

    return output


# =======================================================
#          ROUTES
# =======================================================

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    converted = []

    if request.method == "POST":
        text = request.form.get("input_text", "").strip()
        converted = convert_text(text) if text != "" else []

    sections = build_sections()

    return render_template("index.html",
                           input_text=text,
                           converted=converted,
                           sections=sections)


# =======================================================
#          RUN APP
# =======================================================

if __name__ == "__main__":
    app.run(debug=True)
