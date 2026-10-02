import re, unicodedata
ARABIC_DIGITS="٠١٢٣٤٥٦٧٨٩"
PERSIAN_DIGITS="۰۱۲۳۴۵۶۷۸۹"
def fa_digits(s):
    if s is None: return ""
    s=str(s)
    return s.translate(str.maketrans(ARABIC_DIGITS+PERSIAN_DIGITS,"0123456789"*2))
def normalize_fa(s):
    if s is None: return ""
    s=fa_digits(s)
    s=unicodedata.normalize("NFKC",str(s))
    repl={"ي":"ی","ى":"ی","ك":"ک","ۀ":"ه","ة":"ه","ؤ":"و","إ":"ا","أ":"ا","‌":" ","ـ":" "}
    for a,b in repl.items(): s=s.replace(a,b)
    s=re.sub(r"\s+"," ",s).strip().lower()
    s=re.sub(r"[()\[\]{}،,:؛.!؟/\\\-]+"," ",s)
    return re.sub(r"\s+"," ",s).strip()
def slug(s):
    x=normalize_fa(s)
    return re.sub(r"[^0-9a-zA-Z\u0600-\u06ff]+","-",x).strip("-")
