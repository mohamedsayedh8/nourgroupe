# -*- coding: utf-8 -*-
import re, html as H
from i18n import EN, AR
D = {"en": EN, "ar": AR}
SITE = "https://nourgroupe.com"
IGN = {"English", "Français", "__LCODE__", "ESC", "Fadz", "Zikr", "Kinto", "Nour Groupe", "WhatsApp", "App Store", "Google Play", "FR", "EN", "AR", "Netlify", "Firebase"}
missing = {}
def pfx(l): return "" if l == "fr" else "/" + l
def _t(core, lang, page):
    k = H.unescape(core)
    if k in D[lang]:
        return H.escape(D[lang][k], quote=False)
    if re.search(r"[A-Za-zÀ-ÿ]{2,}", k) and k not in IGN and not re.fullmatch(r"[\w.+-]+@[\w.-]+", k) and not k.startswith("http") and not re.fullmatch(r"[\d\s·+().-]+", k):
        missing.setdefault(k, set()).add(page)
    return core
def _attr(tag, lang, page):
    def rep(m):
        name, val = m.group(1), m.group(2)
        k = H.unescape(val)
        if k in D[lang]:
            return '%s="%s"' % (name, H.escape(D[lang][k]))
        if re.search(r"[A-Za-zÀ-ÿ]{2,}", k) and k not in IGN and not k.startswith(("http", "mailto", "/")) and name != "title":
            missing.setdefault(k, set()).add(page + " [attr]")
        return m.group(0)
    return re.sub(r'\b(alt|aria-label|placeholder|value)="([^"]*)"', rep, tag)
def _meta(tag, lang, page):
    if not re.search(r'(name="description"|property="og:(title|description)")', tag):
        return tag
    return re.sub(r'content="([^"]*)"', lambda m: 'content="%s"' % (H.escape(D[lang][H.unescape(m.group(1))]) if H.unescape(m.group(1)) in D[lang] else (missing.setdefault(H.unescape(m.group(1)), set()).add(page + " [meta]") or m.group(1))), tag)
def rewrite_hrefs(s, lang):
    if lang == "fr": return s
    def rep(m):
        u = m.group(2)
        if u.startswith("//") or u.startswith("/assets/") or u.startswith("/style.css") or u.startswith("/sitemap") or u.startswith("/robots"): return m.group(0)
        return '%s="%s%s"' % (m.group(1), pfx(lang), u)
    return re.sub(r'\b(href)="(/[^"]*)"', rep, s)
def script_tr(sc, lang):
    sc = sc.replace("__PFX__", pfx(lang))
    if lang != "fr":
        for k, v in D[lang].items():
            q = '"%s"' % k
            if q in sc: sc = sc.replace(q, '"%s"' % v.replace('"', '\\"'))
    return sc
def localize(s, lang, name, override=None):
    page = lang + "/" + name
    m = re.search(r'rel="canonical" href="%s(/[^"]*)"' % re.escape(SITE), s)
    path = m.group(1) if m else "/" + name
    parts = re.split(r'(<script.*?</script>|<style.*?</style>|<[^>]+>)', s, flags=re.S)
    out = []
    for p in parts:
        if not p: continue
        if p.startswith("<script"):
            if "ld+json" in p[:60]: out.append(p)
            else: out.append(script_tr(p, lang))
        elif p.startswith("<style"): out.append(p)
        elif p.startswith("<"):
            if lang != "fr":
                p = _attr(p, lang, page)
                if p.startswith("<meta"): p = _meta(p, lang, page)
            out.append(p)
        else:
            if lang == "fr": out.append(p)
            else:
                mm = re.match(r'^(\s*)(.*?)(\s*)$', p, re.S)
                out.append(mm.group(1) + (_t(mm.group(2), lang, page) if mm.group(2) else "") + mm.group(3))
    s = "".join(out)
    if override is not None:
        ov = rewrite_hrefs(override, lang)
        s = re.sub(r'<section class="wrap sec legal">.*?</section>', lambda _m: ov, s, count=1, flags=re.S)
    s = rewrite_hrefs(s, lang)
    # chemins relatifs -> absolus
    s = s.replace('src="assets/', 'src="/assets/').replace('href="style.css', 'href="/style.css')
    # langue / direction
    s = s.replace('<html lang="fr" data-theme="dark">', '<html lang="%s"%s data-theme="dark">' % (lang, ' dir="rtl"' if lang == "ar" else ""))
    # canonical, og:url, hreflang
    cu = SITE + pfx(lang) + path
    s = re.sub(r'(rel="canonical" href=")[^"]*"', lambda _m: _m.group(1) + cu + '"', s)
    s = re.sub(r'(property="og:url" content=")[^"]*"', lambda _m: _m.group(1) + cu + '"', s)
    alts = "".join('<link rel="alternate" hreflang="%s" href="%s%s%s">' % (l, SITE, pfx(l), path) for l in ("fr", "en", "ar"))
    alts += '<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, path)
    s = s.replace("<!--HREFLANG-->", alts)
    s = s.replace('content="fr_FR"', 'content="%s"' % {"fr": "fr_FR", "en": "en_US", "ar": "ar_AR"}[lang])
    for l in ("fr", "en", "ar"):
        s = s.replace("__L_%s__" % l, pfx(l) + (path if path != "/" or l == "fr" else "/") if True else "")
    s = s.replace("__LCODE__", lang.upper())
    if lang == "ar":
        s = s.replace("family=Inter:wght@400;500;600;700;800&display=swap", "family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Arabic:wght@400;500;600;700;800&display=swap")
    return s
