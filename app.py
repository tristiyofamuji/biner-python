from flask import Flask, render_template, request
app = Flask(__name__)

# ============================================
#  FUNGSI KONVERSI DETAIL
# ============================================

def to_binary_steps(decimal):
    """Menghasilkan langkah pembagian berulang untuk konversi decimal → binary."""
    if decimal == 0:
        return "0 → 0"

    steps = []
    n = decimal
    while n > 0:
        q = n // 2
        r = n % 2
        steps.append(f"{n} ÷ 2 = {q} sisa {r}")
        n = q

    binary = format(decimal, '08b')
    steps_text = "\n".join(steps) + f"\nBinary = {binary}"

    return steps_text


def to_hex_steps(decimal):
    """Menghasilkan langkah pembagian berulang untuk konversi decimal → hex."""
    hex_digits = "0123456789ABCDEF"

    if decimal == 0:
        return "0 → 0"

    steps = []
    n = decimal
    hex_result = ""

    while n > 0:
        q = n // 16
        r = n % 16
        steps.append(f"{n} ÷ 16 = {q} sisa {r} ({hex_digits[r]})")
        hex_result = hex_digits[r] + hex_result
        n = q

    steps_text = "\n".join(steps) + f"\nHex = {hex_result}"

    return steps_text


def hex_to_decimal_steps(hex_str):
    """Rumus pangkat 16 seperti contoh 2AF16."""
    hex_digits = "0123456789ABCDEF"
    hex_str = hex_str.upper()

    result_steps = []
    total = 0
    length = len(hex_str)

    for i, digit in enumerate(hex_str):
        value = hex_digits.index(digit)
        power = length - i - 1
        calc = value * (16 ** power)
        result_steps.append(f"{digit} × 16^{power} = {calc}")
        total += calc

    steps_text = "\n".join(result_steps) + f"\nTotal = {total}"
    return steps_text


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


def convert_text(text):
    output = []
    for ch in text:
        code = ord(ch)
        hex_value = format(code, "X")

        output.append({
            "char": ch,
            "decimal": code,
            "binary": format(code, "08b"),
            "hex": hex_value,
            "calc_binary": to_binary_steps(code),
            "calc_hex": to_hex_steps(code),
            "calc_hex_to_dec": hex_to_decimal_steps(hex_value)
        })
    return output


# ============================================
#  ROUTES
# ============================================

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    converted = []

    if request.method == "POST":
        text = request.form.get("input_text", "")
        converted = convert_text(text)

    sections = build_sections()
    return render_template("index.html",
                           input_text=text,
                           converted=converted,
                           sections=sections)


if __name__ == "__main__":
    app.run(debug=True)
