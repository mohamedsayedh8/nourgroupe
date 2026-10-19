import html, json, os, subprocess
import l10n
SITE="https://nourgroupe.com"
MAIL_READY=True  # passer à True quand les redirections @nourgroupe.com existent
MAIL="contact@nourgroupe.com" if MAIL_READY else "contact@fadz.fr"
def amail(a):
    if a=="fadz": return "contact@fadz.fr"
    return f"{a}@nourgroupe.com" if MAIL_READY else MAIL
APPS=[
 dict(id="fadz",name="Fadz",cat="Réservation de coiffeurs et barbiers",tag="Ton coiffeur, maintenant.",
  desc="Fadz met en relation clients et coiffeurs ou barbiers indépendants : réservation en quelques secondes, en salon ou à domicile, ou place dans la file d’attente en direct. Les professionnels gèrent leur agenda, leurs clients et leur activité au même endroit.",
  feats=["Réservation en 3 secondes","Salon ou à domicile","File d’attente en direct"],
  shots=["fadz-screen1.jpg","fadz-screen2.jpg","fadz-screen3.jpg"],icon="fadz-icon.png",
  web="https://fadz.fr",ios=None,android=None,priv="https://fadz.fr/confidentialite",terms="https://fadz.fr/cgu",
  note="Applications iOS et Android bientôt disponibles."),
 dict(id="zikr",name="Zikr",cat="Application mobile",tag="Ton compagnon spirituel quotidien.",
  desc="Zikr t’accompagne au quotidien avec le Coran, les Adhkar et des horaires de prière précis selon ta position. Une interface simple pour garder le lien avec tes routines spirituelles, où que tu sois.",
  feats=["Coran","Adhkar","Horaires de prière"],
  shots=["zikr-screen1.jpg","zikr-screen2.jpg","zikr-screen3.jpg"],icon="zikr-icon.png",
  web=None,ios="https://apps.apple.com/fr/app/zikr/id6759991511",android="https://play.google.com/store/apps/details?id=com.mohamed.zikr",
  priv="/zikr-privacy.html",terms="/zikr-terms.html",note=None),
 dict(id="kinto",name="Kinto",cat="Application mobile",tag="Ton budget, sans effort.",
  desc="Kinto simplifie la gestion de ton budget : scanne tes reçus, suis tes dépenses par catégorie et garde une vue claire sur tes revenus et tes économies, le tout depuis une interface épurée.",
  feats=["Scan des reçus","Dépenses par catégorie","Revenus & économies"],
  shots=["kinto-screen1.jpg","kinto-screen2.jpg","kinto-screen3.jpg"],icon="kinto-icon.png",
  web=None,ios="https://apps.apple.com/fr/app/kinto/id6761582723",android=None,
  priv="/kinto-privacy.html",terms="/kinto-terms.html",note="Version Android bientôt disponible."),
]
HEAD_JS = r'''(function(){try{var d=document.documentElement,t=null,L=d.lang||"fr";
try{t=localStorage.getItem("ng-theme")}catch(e){}
var mq=matchMedia("(prefers-color-scheme: light)");
function ap(){d.dataset.theme=(t==="light"||t==="dark")?t:(mq.matches?"light":"dark")}ap();
if(mq.addEventListener)mq.addEventListener("change",function(){try{t=localStorage.getItem("ng-theme")}catch(e){t=null}if(t!=="light"&&t!=="dark")ap()});
var pref=null;try{pref=localStorage.getItem("ng-lang")}catch(e){}
if(!/bot|crawl|spider|slurp|lighthouse|facebookexternalhit|preview/i.test(navigator.userAgent)){
var want=pref;
if(!want&&L==="fr"){var ls=navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||"fr"];
for(var i=0;i<ls.length;i++){var c=String(ls[i]||"").toLowerCase().split("-")[0];if(c==="fr"||c==="en"||c==="ar"){want=c;break}}}
if(want&&want!==L&&(want==="fr"||want==="en"||want==="ar")){
var p=location.pathname.replace(/^\/(en|ar)(?=\/|$)/,"")||"/";
location.replace((want==="fr"?"":"/"+want)+p+location.search+location.hash)}}
}catch(e){}})();'''
E=html.escape
def head(title,desc,path):
    return f'''<!DOCTYPE html>
<html lang="fr" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Nour Groupe">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{SITE}{path}">
<meta name="theme-color" content="#0b0d12">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:locale" content="fr_FR">
<!--HREFLANG-->
<meta name="author" content="Nour Groupe">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="512x512" href="/assets/icon-512.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<meta property="og:image" content="https://nourgroupe.com/assets/og.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://nourgroupe.com/assets/og.jpg">
<script>{HEAD_JS}</script>
<link rel="stylesheet" href="/style.css?v=15">
</head>
<body>
<header class="pillnav"><div class="pill-in">
<a class="brand" href="/" aria-label="Nour Groupe"><img class="mark-img" src="/assets/logo-icon-dark.png" alt="" width="30" height="30"><span class="bname">Nour Groupe</span></a>
<nav class="plinks" aria-label="Navigation principale"><a href="/#apps">Apps</a><a href="/#services">Services</a><a href="/projets.html">Projets</a><a href="/contact.html">Contact</a></nav>
<div class="pctl"><div class="lang"><button id="lang-open" type="button" class="icbtn lbtn" aria-haspopup="true" aria-expanded="false" aria-label="Langue">__LCODE__</button><div class="lmenu" id="lmenu" hidden><a href="__L_fr__" data-l="fr" hreflang="fr" lang="fr">Français</a><a href="__L_en__" data-l="en" hreflang="en" lang="en">English</a><a href="__L_ar__" data-l="ar" hreflang="ar" lang="ar" dir="rtl">العربية</a></div></div><button id="cmd-open" type="button" class="icbtn" aria-label="Ouvrir les raccourcis" title="Raccourcis · ⌘K">⌕</button>
<button id="theme" class="icbtn" aria-label="Changer de thème" type="button">◐</button></div>
</div></header>
<main>
'''
CMD = r'''<dialog class="cmd" id="cmd"><div class="cmd-panel">
<label class="cmd-search"><span>⌕</span><input id="cmd-q" type="search" autocomplete="off" placeholder="Que veux-tu faire ?" aria-label="Rechercher une action"><kbd>ESC</kbd></label>
<p class="cmd-label">Navigation</p><div id="cmd-items" class="cmd-items"></div>
<div class="cmd-hint"><span><kbd>↑</kbd><kbd>↓</kbd> parcourir</span><span><kbd>↵</kbd> ouvrir</span><span><kbd>⌘K</kbd> raccourcis</span></div>
</div></dialog>
<script>
(function(){
var d=document.documentElement;
try{var hp=document.querySelector('.hero-phones');if(hp&&matchMedia('(pointer:fine)').matches&&!matchMedia('(prefers-reduced-motion: reduce)').matches){document.addEventListener('mousemove',function(e){var x=(e.clientX/innerWidth-.5)*2,y=(e.clientY/innerHeight-.5)*2;hp.style.setProperty('--mx',x.toFixed(3));hp.style.setProperty('--my',y.toFixed(3))})}}catch(e){}
try{if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){d.classList.add('rv');var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});var els=document.querySelectorAll('.showcase,.val,.steps li,.faq details,.band,.panel,.shots img');els.forEach(function(el){el.classList.add('rvi');io.observe(el)});
function chk(){els.forEach(function(el){var r=el.getBoundingClientRect();if(r.top<innerHeight*0.95)el.classList.add('in')})}
addEventListener('scroll',chk,{passive:true});addEventListener('load',chk);setTimeout(chk,300);setTimeout(function(){els.forEach(function(el){el.classList.add('in')})},5000)}}catch(e){}
function theme(){var t=d.dataset.theme==="dark"?"light":"dark";d.dataset.theme=t;try{localStorage.setItem("ng-theme",t)}catch(e){}}
document.getElementById("theme").onclick=theme;
var lo=document.getElementById("lang-open"),lm=document.getElementById("lmenu");lo.onclick=function(e){e.stopPropagation();var h=lm.hidden;lm.hidden=!h;lo.setAttribute("aria-expanded",String(h))};document.addEventListener("click",function(){lm.hidden=true;lo.setAttribute("aria-expanded","false")});lm.addEventListener("click",function(e){var a=e.target.closest("a");if(a){try{localStorage.setItem("ng-lang",a.dataset.l)}catch(x){}}});
var A=[["Accueil","__PFX__/"],["Nos applications","__PFX__/#apps"],["Fadz","__PFX__/fadz.html"],["Zikr","__PFX__/zikr.html"],["Kinto","__PFX__/kinto.html"],["Services","__PFX__/#services"],["Projets sur mesure","__PFX__/projets.html"],["Contact","__PFX__/contact.html"],["Changer de thème",null,theme],["Thème automatique (système)",null,function(){try{localStorage.removeItem("ng-theme")}catch(e){}d.dataset.theme=matchMedia("(prefers-color-scheme: light)").matches?"light":"dark"}],["Français","__L_fr__",null,"fr"],["English","__L_en__",null,"en"],["العربية","__L_ar__",null,"ar"],["Appeler le 07 53 41 88 24","tel:+33753418824"],["Copier l’adresse e-mail",null,function(){var m="contact@nourgroupe.com";(navigator.clipboard?navigator.clipboard.writeText(m):Promise.reject()).catch(function(){location.href="mailto:"+m})}],["Mentions légales","__PFX__/mentions-legales.html"],["Confidentialité","__PFX__/confidentialite.html"]];
var dlg=document.getElementById("cmd"),q=document.getElementById("cmd-q"),box=document.getElementById("cmd-items"),act=0,cur=A;
function render(){box.innerHTML="";cur.forEach(function(it,i){var b=document.createElement("button");b.type="button";b.className="cmd-item"+(i===act?" on":"");b.textContent=it[0];b.onclick=function(){run(it)};box.appendChild(b)});if(!cur.length)box.innerHTML='<p class="small" style="padding:12px">Aucune action trouvée</p>'}
function run(it){dlg.close();if(it[3]){try{localStorage.setItem("ng-lang",it[3])}catch(e){}}if(it[2])it[2]();else location.href=it[1]}
function open(){cur=A;act=0;q.value="";render();if(dlg.showModal)dlg.showModal();setTimeout(function(){q.focus()},30)}
document.getElementById("cmd-open").onclick=open;
document.addEventListener("keydown",function(e){if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==="k"){e.preventDefault();dlg.open?dlg.close():open()}});
q.oninput=function(){var v=q.value.toLowerCase();cur=A.filter(function(x){return x[0].toLowerCase().indexOf(v)>-1});act=0;render()};
q.onkeydown=function(e){if(e.key==="ArrowDown"){act=Math.min(act+1,cur.length-1);render();e.preventDefault()}else if(e.key==="ArrowUp"){act=Math.max(act-1,0);render();e.preventDefault()}else if(e.key==="Enter"&&cur[act]){run(cur[act])}};
dlg.addEventListener("click",function(e){if(e.target===dlg)dlg.close()});
})();
</script>'''
def foot():
    return f'''</main>
<footer class="foot"><div class="wrap">
<div class="foot-row"><strong>Nour Groupe</strong><span>Des apps utiles, soignées et simples.</span></div>
<div class="foot-links"><a href="/projets.html">Projets</a><a href="/contact.html">Contact</a><a href="https://wa.me/33753418824" rel="noopener">WhatsApp</a><a href="tel:+33753418824">07 53 41 88 24</a><a href="/mentions-legales.html">Mentions légales</a><a href="/confidentialite.html">Confidentialité</a></div>
<p class="small">© 2026 Nour Groupe — Mohamed Elhawawshi, entrepreneur individuel · SIRET 982 860 819 00019</p>
</div></footer>
{CMD}
</body></html>
'''
def card(a):
    st = "Disponible" if (a['ios'] or a['android']) else "Bientôt"
    return f'''<a class="card" href="/{a['id']}.html"><img src="assets/{a['icon']}" alt="" width="64" height="64">
<div><h3>{a['name']}</h3><p class="muted">{a['tag']}</p></div><span class="pill">{st}</span></a>'''
OVERRIDE={}
def write(name,s):
    open(name,"w",encoding="utf-8").write(l10n.localize(s,"fr",name) if name.endswith(".html") else s)
    if name.endswith(".html"):
        for lg in ("en","ar"):
            os.makedirs(lg,exist_ok=True)
            open(f"{lg}/{name}","w",encoding="utf-8").write(l10n.localize(s,lg,name,OVERRIDE.get((name,lg))))

# index
def phone(src,alt,cls=""):
    return f'<figure class="phone {cls}"><img src="assets/{src}" alt="{E(alt)}" width="780" height="1692"></figure>'
def abtns(a):
    st=[]
    if a['ios']: st.append(f'<a class="btn" href="{a["ios"]}" rel="noopener">App Store</a>')
    if a['android']: st.append(f'<a class="btn" href="{a["android"]}" rel="noopener">Google Play</a>')
    if a['web']: st.append(f'<a class="btn" href="{a["web"]}" rel="noopener">Ouvrir {a["name"]}</a>')
    if not a['ios'] and not a['web']: st.append('<span class="btn off">App Store · bientôt</span>')
    if not a['android']: st.append('<span class="btn off">Google Play · bientôt</span>')
    return " ".join(st)
LD='''<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Nour Groupe","url":"https://nourgroupe.com","logo":"https://nourgroupe.com/assets/icon-512.png","email":"contact@nourgroupe.com","telephone":"+33753418824","address":{"@type":"PostalAddress","addressLocality":"Paris","addressCountry":"FR"},"description":"Nour Groupe conçoit des applications mobiles, des sites web et des outils sur mesure : Fadz, Zikr, Kinto."}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"Nour Groupe","url":"https://nourgroupe.com","inLanguage":"fr"}</script>
'''
s=head("Nour Groupe — Des apps utiles et soignées","Nour Groupe conçoit des applications mobiles et web utiles, soignées et simples : Fadz, Zikr, Kinto.","/")
s+=LD+f'''<section class="hero"><div class="glow"></div><div class="wrap hero-grid">
<div class="hero-copy">
<p class="avail"><span class="dot"></span>Ouvert aux nouveaux projets</p>
<p class="eyebrow">Éditeur d’applications · Paris</p>
<h1>Des apps utiles,<br><span class="grad">soignées et simples.</span></h1>
<p class="lead">Nour Groupe conçoit et publie ses propres applications, et réalise vos projets numériques sur mesure : applications, sites web et outils.</p>
<p class="cta"><a class="btn" href="#apps">Découvrir les apps</a> <a class="btn ghost" href="/contact.html">Nous contacter</a></p>

</div>
<div class="hero-phones" aria-hidden="true">{phone("kinto-screen1.jpg","","p1")}{phone("zikr-screen1.jpg","","p2")}{phone("fadz-screen1.jpg","","p3")}</div>
</div></section>
<section id="apps" class="wrap sec"><p class="eyebrow">Nos applications</p><h2 class="big">Trois apps, une même exigence.</h2>
'''
for i,a in enumerate(APPS):
    st = "Disponible" if (a['ios'] or a['android']) else "Bientôt"
    s+=f'''<article class="showcase {'rev' if i%2 else ''}">
<div class="sc-copy"><div class="sc-head"><img src="assets/{a['icon']}" alt="" width="64" height="64"><div><h3>{a['name']}</h3><span class="pill">{st}</span></div></div>
<p class="sc-tag">{a['tag']}</p><p class="muted">{a['desc']}</p>
<ul class="feats">{"".join(f"<li>{f}</li>" for f in a['feats'])}</ul>
<p><a class="btn" href="/{a['id']}.html">Découvrir {a['name']}</a></p></div>
<div class="sc-shots">{phone(a['shots'][0],a['name'],'s1')}{phone(a['shots'][1],a['name'],'s2')}</div>
</article>
'''
s+='''</section>
<section id="services" class="wrap sec"><div class="sec-head"><div><p class="eyebrow">Services</p><h2 class="big">Un projet ? On le réalise.</h2>
<p class="lead">Entreprises, associations ou particuliers : si vous avez besoin d’une application, d’un site ou d’un outil sur mesure, Nour Groupe s’en charge, de l’idée à la mise en ligne.</p></div><img class="sec-mascot" src="/assets/mascotte-3.png" alt="" width="180" height="320" loading="lazy"></div>
<div class="values">
<div class="val"><span class="ico">▣</span><h3>Applications mobiles</h3><p>Apps iOS et Android, de la conception à la publication sur les stores.</p></div>
<div class="val"><span class="ico">◈</span><h3>Sites web &amp; plateformes</h3><p>Sites vitrines, réservation en ligne, espaces clients et outils métiers.</p></div>
<div class="val"><span class="ico">✎</span><h3>Design &amp; accompagnement</h3><p>Identité, maquettes, mise en ligne et suivi après lancement.</p></div>
</div>
<p><a class="btn" href="/contact.html">Parler de mon projet</a></p></section>
<section class="wrap sec"><p class="eyebrow">Comment on travaille</p><h2 class="big">Du premier échange au lancement.</h2>
<ol class="steps">
<li><b>01</b><h3>Échange</h3><p>On cadre votre besoin, vos objectifs et vos contraintes.</p></li>
<li><b>02</b><h3>Maquette</h3><p>Vous voyez le produit avant qu’il ne soit développé.</p></li>
<li><b>03</b><h3>Développement</h3><p>Réalisation par étapes, avec des points réguliers.</p></li>
<li><b>04</b><h3>Lancement</h3><p>Mise en ligne, publication sur les stores et suivi.</p></li>
</ol></section>
<section class="wrap sec"><p class="eyebrow">Questions fréquentes</p><h2 class="big">Ce qu’on nous demande souvent.</h2>
<div class="faq">
<details><summary>Quels types de projets réalisez-vous ?</summary><p>Applications mobiles iOS et Android, sites vitrines, plateformes de réservation, espaces clients et outils internes.</p></details>
<details><summary>Comment démarrer un projet ?</summary><p>Écrivez-nous à contact@nourgroupe.com avec une description de votre besoin. On revient vers vous pour en discuter.</p></details>
<details><summary>Vous occupez-vous de la publication sur les stores ?</summary><p>Oui, de la préparation des fiches App Store et Google Play jusqu’à la publication.</p></details>
<details><summary>Peut-on vous confier la suite après le lancement ?</summary><p>Oui : corrections, évolutions et suivi technique peuvent être assurés après la mise en ligne.</p></details>
</div></section>
<section class="wrap sec"><div class="sec-head"><div><p class="eyebrow">Notre approche</p><h2 class="big">Fait pour durer.</h2></div><img class="sec-mascot" src="/assets/mascotte-1.png" alt="" width="180" height="278" loading="lazy"></div>
<div class="values">
<div class="val"><span class="ico">✦</span><h3>Simple</h3><p>Chaque écran a un seul objectif. Pas de fonctions inutiles, pas de friction.</p></div>
<div class="val"><span class="ico">◎</span><h3>Soigné</h3><p>Un design cohérent, fluide et lisible, en clair comme en sombre.</p></div>
<div class="val"><span class="ico">⛨</span><h3>Transparent</h3><p>Une politique de confidentialité claire et accessible pour chaque application.</p></div>
</div></section>
<section class="wrap sec"><div class="band"><img class="band-mascot" src="/assets/mascotte-2.png" alt="" width="150" height="232"><div><h2>Un projet, une question ?</h2><p class="muted">Écris-nous, on répond en général sous quelques jours.</p></div>
<a class="btn" href="/contact.html">Nous contacter</a></div></section>
'''+foot()
write("index.html",s)

for a in APPS:
    s=head(f"{a['name']} — Nour Groupe",a['desc'],f"/{a['id']}.html")
    sup=amail(a['id'])
    s+=f'''<section class="hero small-hero"><div class="glow"></div><div class="wrap hero-grid">
<div class="hero-copy"><p><a class="back" href="/">← Nour Groupe</a></p>
<div class="app-head"><img src="assets/{a['icon']}" alt="Icône {a['name']}" width="88" height="88"><div>
<p class="eyebrow">{a['cat']}</p><h1>{a['name']}</h1></div></div>
<p class="lead">{a['tag']}</p><p class="desc">{a['desc']}</p>
<ul class="feats">{"".join(f"<li>{f}</li>" for f in a['feats'])}</ul>
<p class="cta">{abtns(a)}</p>
{f'<p class="muted">{a["note"]}</p>' if a['note'] else ''}</div>
<div class="hero-phones one" aria-hidden="true">{phone(a['shots'][0],a['name'],'p2')}</div>
</div></section>
<section class="wrap sec"><div class="shots">{"".join(f'<img src="assets/{x}" alt="Capture {a["name"]}" loading="lazy">' for x in a['shots'])}</div></section>
<section class="wrap sec"><div class="panel info"><div><h2>Informations</h2>
<p><a href="{a['priv']}" rel="noopener">Politique de confidentialité</a><br><a href="{a['terms']}" rel="noopener">Conditions d’utilisation</a></p></div>
<div><h2>Support</h2><p><a href="mailto:{sup}">{sup}</a></p><p class="small">{a['name']} est édité par Nour Groupe.</p></div></div></section>
'''+foot()
    write(a['id']+".html",s)

s=head("Contact — Nour Groupe","Un projet à confier, une question, un souci avec une app ? Écrivez à Nour Groupe : e-mail, téléphone ou WhatsApp.","/contact.html")
WA="https://wa.me/33753418824"
sup="".join(f'''<div class="sup"><img src="assets/{a['icon']}" alt="" width="48" height="48"><div><h3>{a['name']}</h3><a href="mailto:{amail(a['id'])}">{amail(a['id'])}</a><p class="small"><a href="{a['priv']}">Confidentialité</a> · <a href="/{a['id']}.html">Page {a['name']}</a></p></div></div>''' for a in APPS)
s+=f'''<section class="hero small-hero"><div class="glow"></div><div class="wrap"><p class="eyebrow">Contact</p>
<h1>Parlons de <span class="grad">votre projet.</span></h1>
<p class="lead">Une application, un site, un outil sur mesure, ou une question sur l’une de nos apps : écrivez-nous, on revient vers vous rapidement.</p>
<div class="chan">
<a class="chan-i" href="mailto:{MAIL}"><span class="ico">@</span><div><b>E-mail</b><span>{MAIL}</span></div></a>
<a class="chan-i" href="{WA}" rel="noopener"><span class="ico">✆</span><div><b>WhatsApp</b><span>07 53 41 88 24</span></div></a>
<a class="chan-i" href="tel:+33753418824"><span class="ico">☏</span><div><b>Téléphone</b><span>07 53 41 88 24</span></div></a>
</div></div><img class="hero-mascot" src="/assets/mascotte-1.png" alt="Mascotte Nour Groupe" width="300" height="464"></section>
<section class="wrap sec"><div class="panel"><h2>Décrivez votre projet</h2>
<p class="muted">Remplissez ce formulaire : il prépare un message prêt à envoyer par e-mail ou WhatsApp. Aucune donnée n’est enregistrée sur ce site.</p>
<form id="pf" class="pform" onsubmit="return false">
<fieldset><legend>Type de projet</legend>
<label class="chip"><input type="radio" name="type" value="Application mobile" checked><span>Application mobile</span></label>
<label class="chip"><input type="radio" name="type" value="Site web / vitrine"><span>Site web</span></label>
<label class="chip"><input type="radio" name="type" value="Plateforme / réservation"><span>Plateforme</span></label>
<label class="chip"><input type="radio" name="type" value="Outil sur mesure"><span>Outil sur mesure</span></label>
<label class="chip"><input type="radio" name="type" value="Autre"><span>Autre</span></label></fieldset>
<fieldset><legend>Où en êtes-vous ?</legend>
<label class="chip"><input type="radio" name="stage" value="Juste une idée" checked><span>Une idée</span></label>
<label class="chip"><input type="radio" name="stage" value="J’ai une maquette"><span>J’ai une maquette</span></label>
<label class="chip"><input type="radio" name="stage" value="Un produit existe déjà"><span>Un produit existe déjà</span></label></fieldset>
<div class="frow"><label>Votre nom<input id="pn" type="text" autocomplete="name" placeholder="Prénom Nom"></label>
<label>Votre e-mail ou téléphone<input id="pc" type="text" autocomplete="email" placeholder="pour vous répondre"></label></div>
<label>Votre besoin<textarea id="pm" rows="5" placeholder="Décrivez en quelques lignes ce que vous souhaitez…"></textarea></label>
<p class="cta"><a class="btn" id="pmail" href="mailto:{MAIL}">Envoyer par e-mail</a> <a class="btn ghost" id="pwa" href="{WA}" rel="noopener">Envoyer sur WhatsApp</a></p>
</form></div></section>
<section class="wrap sec"><p class="eyebrow">Support des applications</p><h2 class="big">Un souci avec une app ?</h2>
<p class="muted">Chaque application a sa propre adresse de support. Indiquez le modèle de votre téléphone et décrivez le problème.</p>
<div class="sups">{sup}</div></section>
<section class="wrap sec"><div class="panel info"><div><h2>Réponse</h2><p class="muted">Nous répondons généralement sous quelques jours ouvrés.</p></div>
<div><h2>Basés à</h2><p class="muted">Paris, France</p></div>
<div><h2>Entreprise</h2><p class="muted">Nour Groupe<br>SIRET 982 860 819 00019</p></div></div></section>
<script>
(function(){{var f=document.getElementById("pf");function v(n){{var e=f.querySelector("input[name="+n+"]:checked");return e?e.value:""}}
function body(){{var t=document.getElementById("pm").value.trim(),n=document.getElementById("pn").value.trim(),c=document.getElementById("pc").value.trim();
return "Bonjour,\\n\\nType de projet : "+v("type")+"\\nAvancement : "+v("stage")+"\\n\\n"+(t||"(décrivez votre besoin ici)")+"\\n\\n"+(n?n+"\\n":"")+(c?"Contact : "+c:"")}}
function upd(){{var b=body(),sub="Projet : "+v("type");document.getElementById("pmail").href="mailto:{MAIL}?subject="+encodeURIComponent(sub)+"&body="+encodeURIComponent(b);document.getElementById("pwa").href="{WA}?text="+encodeURIComponent(sub+"\\n\\n"+b)}}
f.addEventListener("input",upd);f.addEventListener("change",upd);upd()}})();
</script>
'''+foot()
write("contact.html",s)


# ---- contenus juridiques EN / AR (remplacent la section .legal) ----
def _links(lang):
    return "".join(f'<li><a href="{a["priv"]}" rel="noopener">{a["name"]}</a></li>' for a in APPS)
OVERRIDE[("mentions-legales.html","en")]=f'''<section class="wrap sec legal"><p><a class="back" href="/">← Nour Groupe</a></p><h1>Legal notice</h1>
<h2>Publisher</h2>
<p>The nourgroupe.com website is published by <b>Nour Groupe</b>, trade name of <b>Mohamed Elhawawshi</b>, sole proprietor.<br>
SIREN 982 860 819 · SIRET 982 860 819 00019 · EU VAT FR40 982 860 819<br>
Registered office: 75001 Paris, France<br>Publication director: Mohamed Elhawawshi<br>
Contact: <a href="mailto:{MAIL}">{MAIL}</a></p>
<h2>Hosting</h2>
<p>Netlify, Inc., 512 2nd Street, Suite 200, San Francisco, CA 94107, United States.</p>
<h2>Intellectual property</h2>
<p>The Nour Groupe name, logos and the content of this site belong to their publisher. The names Fadz, Zikr and Kinto refer to apps published by Nour Groupe.</p>
</section>'''
OVERRIDE[("mentions-legales.html","ar")]=f'''<section class="wrap sec legal"><p><a class="back" href="/">→ Nour Groupe</a></p><h1>الإشعار القانوني</h1>
<h2>الناشر</h2>
<p>موقع nourgroupe.com من إصدار <b>Nour Groupe</b>، وهي الاسم التجاري لـ <b>Mohamed Elhawawshi</b>، مقاول فردي.<br>
SIREN 982 860 819 · SIRET 982 860 819 00019 · رقم ضريبة القيمة المضافة FR40 982 860 819<br>
المقر: 75001 باريس، فرنسا<br>مدير النشر: Mohamed Elhawawshi<br>
للتواصل: <a href="mailto:{MAIL}">{MAIL}</a></p>
<h2>الاستضافة</h2>
<p>Netlify, Inc., 512 2nd Street, Suite 200, San Francisco, CA 94107, الولايات المتحدة.</p>
<h2>الملكية الفكرية</h2>
<p>اسم Nour Groupe والشعارات ومحتويات هذا الموقع ملك لناشرها. تشير الأسماء Fadz وZikr وKinto إلى تطبيقات من إصدار Nour Groupe.</p>
</section>'''
OVERRIDE[("confidentialite.html","en")]=f'''<section class="wrap sec legal"><p><a class="back" href="/">← Nour Groupe</a></p><h1>Privacy</h1>
<h2>This site</h2>
<p>nourgroupe.com is a showcase website: it has no user accounts, no forms, no advertising cookies and no analytics tools. Only your light/dark theme and language choices are remembered in your browser (local storage, never sent anywhere).</p>
<p>Like any host, Netlify may record technical logs (IP address, date, page) for security and proper operation of the service.</p>
<h2>If you write to us</h2>
<p>Your message and email address are used only to reply to you and are neither sold nor shared. You can request their deletion at any time at <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<h2>Our apps</h2>
<p>Each app has its own privacy policy:</p>
<ul>{_links("en")}</ul>
<p class="small">Data controller: Mohamed Elhawawshi (Nour Groupe), sole proprietor, 75001 Paris.</p>
</section>'''
OVERRIDE[("confidentialite.html","ar")]=f'''<section class="wrap sec legal"><p><a class="back" href="/">→ Nour Groupe</a></p><h1>الخصوصية</h1>
<h2>هذا الموقع</h2>
<p>nourgroupe.com موقع تعريفي: لا يحتوي على حسابات مستخدمين ولا نماذج ولا ملفات تعريف ارتباط إعلانية ولا أدوات قياس للجمهور. يُحفظ فقط اختيارك للمظهر (فاتح/داكن) واللغة في متصفحك (تخزين محلي، لا يُرسل إلى أي جهة).</p>
<p>مثل أي مستضيف، قد تسجّل Netlify سجلات تقنية (عنوان IP والتاريخ والصفحة) لأغراض الأمان وحسن سير الخدمة.</p>
<h2>إذا راسلتنا</h2>
<p>تُستخدم رسالتك وبريدك الإلكتروني فقط للرد عليك، ولا يتم بيعهما أو مشاركتهما. يمكنك طلب حذفهما في أي وقت عبر <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<h2>تطبيقاتنا</h2>
<p>لكل تطبيق سياسة خصوصية خاصة به:</p>
<ul>{_links("ar")}</ul>
<p class="small">المسؤول عن المعالجة: Mohamed Elhawawshi (Nour Groupe)، مقاول فردي، 75001 باريس.</p>
</section>'''

s=head("Mentions légales — Nour Groupe","Éditeur, hébergement et informations légales du site Nour Groupe.","/mentions-legales.html")
s+=f'''<section class="wrap sec legal"><p><a class="back" href="/">← Nour Groupe</a></p><h1>Mentions légales</h1>
<h2>Éditeur</h2>
<p>Le site nourgroupe.com est édité par <b>Nour Groupe</b>, nom commercial de <b>Mohamed Elhawawshi</b>, entrepreneur individuel.<br>
SIREN 982 860 819 · SIRET 982 860 819 00019 · TVA intracommunautaire FR40 982 860 819<br>
Siège : 75001 Paris<br>Directeur de la publication : Mohamed Elhawawshi<br>
Contact : <a href="mailto:{MAIL}">{MAIL}</a></p>
<h2>Hébergement</h2>
<p>Netlify, Inc., 512 2nd Street, Suite 200, San Francisco, CA 94107, États-Unis.</p>
<h2>Propriété intellectuelle</h2>
<p>Le nom Nour Groupe, les logos et les contenus de ce site sont la propriété de leur éditeur. Les noms Fadz, Zikr et Kinto désignent des applications éditées par Nour Groupe.</p>
</section>
'''+foot()
write("mentions-legales.html",s)

s=head("Confidentialité — Nour Groupe","Politique de confidentialité du site nourgroupe.com et liens vers celle de chaque application.","/confidentialite.html")
s+=f'''<section class="wrap sec legal"><p><a class="back" href="/">← Nour Groupe</a></p><h1>Confidentialité</h1>
<h2>Ce site</h2>
<p>nourgroupe.com est un site vitrine : il n’a ni compte utilisateur, ni formulaire, ni cookie publicitaire ni outil de mesure d’audience. Seul le choix du thème clair/sombre est mémorisé dans ton navigateur (stockage local, jamais envoyé).</p>
<p>Comme tout hébergeur, Netlify peut enregistrer des journaux techniques (adresse IP, date, page) pour la sécurité et le bon fonctionnement du service.</p>
<h2>Si tu nous écris</h2>
<p>Ton message et ton adresse e-mail servent uniquement à te répondre et ne sont ni vendus ni partagés. Tu peux demander leur suppression à tout moment à <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<h2>Nos applications</h2>
<p>Chaque application a sa propre politique de confidentialité :</p>
<ul>{"".join(f'<li><a href="{a["priv"]}" rel="noopener">{a["name"]}</a></li>' for a in APPS)}</ul>
<p class="small">Responsable du traitement : Mohamed Elhawawshi (Nour Groupe), entrepreneur individuel, 75001 Paris.</p>
</section>
'''+foot()
write("confidentialite.html",s)

pages=["/zikr-privacy.html","/zikr-terms.html","/kinto-privacy.html","/kinto-terms.html","/","/fadz.html","/zikr.html","/kinto.html","/projets.html","/contact.html","/mentions-legales.html","/confidentialite.html"]
def _sm():
    x='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    for p in pages:
        for lg in ("fr","en","ar"):
            pf="" if lg=="fr" else "/"+lg
            x+=f"<url><loc>{SITE}{pf}{p}</loc><lastmod>2026-10-19</lastmod>"
            for l2 in ("fr","en","ar"):
                p2="" if l2=="fr" else "/"+l2
                x+=f'<xhtml:link rel="alternate" hreflang="{l2}" href="{SITE}{p2}{p}"/>'
            x+=f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{p}"/></url>\n'
    return x+"</urlset>\n"
write("sitemap.xml",_sm())
write("robots.txt",f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
write("netlify.toml",'''[build]
  publish = "."

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "DENY"

[[redirects]]
  from = "https://www.nourgroupe.com/*"
  to = "https://nourgroupe.com/:splat"
  status = 301
  force = true
''')

import re,os
SRC="../portfolio/"
for app in ("zikr","kinto"):
    for kind,label in (("privacy","Politique de confidentialité"),("terms","Conditions d’utilisation")):
        raw=open(f"{SRC}{app}-{kind}.html",encoding="utf-8").read()
        m=re.search(r'<h1[^>]*>(.*?)</h1>',raw,re.S); h1=re.sub(r"[^\w ’'—-].*?(?=[A-Za-zÀ-ÿ])","",m.group(1),count=1).strip() if m else label
        h1=f"{label} — {app.capitalize()}"
        upd=re.search(r'<span class="last-updated"[^>]*>(.*?)</span>',raw,re.S)
        ident=re.search(r'<p class="app-identity"[^>]*>(.*?)</p>',raw,re.S)
        body=re.search(r'<div class="legal-content">(.*?)</div>\s*</div>\s*</section>',raw,re.S).group(1)
        for t in (body,):
            pass
        body=re.sub(r' data-page-i18n="[^"]*"','',body)
        body=re.sub(r' data-i18n="[^"]*"','',body)
        body=body.replace("Mohamed Sayed","Nour Groupe")
        body=body.replace("contact@mohamedelhawawshi.com",amail(app)).replace("contact@fadz.fr",amail(app))
        ident_html=re.sub(r' data-page-i18n="[^"]*"','',ident.group(1)) if ident else ""
        ident_html=ident_html.replace("4 Rue Perrault, 75001 Paris","75001 Paris").replace("Éditeur : <strong>Mohamed Elhawawshi</strong>","Éditeur : <strong>Nour Groupe</strong> (Mohamed Elhawawshi, entrepreneur individuel)")
        page=head(f"{h1} — Nour Groupe",f"{label} de l’application {app.capitalize()}.",f"/{app}-{kind}.html")
        page+=f'''<section class="wrap sec legal"><p><a class="back" href="/{app}.html">← {app.capitalize()}</a></p>
<h1>{E(h1)}</h1>
<p class="small">{upd.group(1) if upd else ""}</p>
<p class="small">{ident_html}</p>
{body}
<p class="small">{app.capitalize()} est édité par Nour Groupe.</p>
</section>'''+foot()
        PT=json.load(open(f"logo/pt-{app}-{kind}.json",encoding="utf-8"))
        for lg in ("en","ar"):
            T=PT[lg]
            bodyl=re.sub(r' data-page-i18n="[^"]*"','',body)
            # remplace le contenu de chaque élément par sa traduction (même clé)
            rawbody=re.search(r'<div class="legal-content">(.*?)</div>\s*</div>\s*</section>',raw,re.S).group(1)
            def sub_key(mm):
                key=mm.group(3)
                return mm.group(1)+(T.get(key,mm.group(4)))+mm.group(5)
            rb=re.sub(r'(<(\w+)[^>]*?data-page-i18n="([^"]+)"[^>]*>)(.*?)(</\2>)',lambda mm:mm.group(1)+T.get(mm.group(3),mm.group(4))+mm.group(5),rawbody,flags=re.S)
            rb=re.sub(r' data-page-i18n="[^"]*"','',rb)
            rb=rb.replace("Mohamed Sayed","Nour Groupe").replace("contact@mohamedelhawawshi.com",amail(app)).replace("contact@fadz.fr",amail(app))
            title=re.sub(r"^[^\w\u0600-\u06FF]+","",T.get("title",label)).strip()
            idl=T.get("identity","").replace("4 Rue Perrault, 75001 Paris","75001 Paris")
            idl=idl.replace("Publisher: <strong>Mohamed Elhawawshi</strong>","Publisher: <strong>Nour Groupe</strong> (Mohamed Elhawawshi, sole proprietor)").replace("الناشر: <strong>Mohamed Elhawawshi</strong>","الناشر: <strong>Nour Groupe</strong> (Mohamed Elhawawshi، مقاول فردي)")
            arrow="→" if lg=="ar" else "←"
            pubby={"en":f"{app.capitalize()} is published by Nour Groupe.","ar":f"تطبيق {app.capitalize()} من إصدار Nour Groupe."}[lg]
            OVERRIDE[(f"{app}-{kind}.html",lg)]=f'''<section class="wrap sec legal"><p><a class="back" href="/{app}.html">{arrow} {app.capitalize()}</a></p>
<h1>{title}</h1>
<p class="small">{T.get("updated","")}</p>
<p class="small">{idl}</p>
{rb}
<p class="small">{pubby}</p>
</section>'''
        write(f"{app}-{kind}.html",page)

p=head("Page introuvable — Nour Groupe","Cette page n’existe pas.","/404.html").replace("index,follow,max-image-preview:large","noindex,follow")
p+='''<section class="hero small-hero"><div class="glow"></div><div class="wrap"><p class="eyebrow">Erreur 404</p><h1>Page introuvable.</h1>
<p class="lead">Le lien est peut-être incorrect ou la page a été déplacée.</p><p><a class="btn" href="/">Retour à l’accueil</a></p><img class="hero-mascot" src="/assets/mascotte-2.png" alt="" width="260" height="400"></div></section>'''+foot()
write("404.html",p)

CASES=[
 dict(n="Fadz",icon="fadz-icon.png",shot="fadz-screen1.jpg",tag="Plateforme de réservation",
  need="Mettre en relation clients et coiffeurs ou barbiers indépendants, sans appels ni messages.",
  done=["Réservation en quelques secondes, en salon ou à domicile","File d’attente en direct","Espace professionnel : agenda, clients, activité","Site web + applications iOS et Android"],
  tech="Next.js · SwiftUI · Jetpack Compose · Firebase",link="/fadz.html"),
 dict(n="Zikr",icon="zikr-icon.png",shot="zikr-screen1.jpg",tag="Application mobile",
  need="Une app de pratique spirituelle quotidienne, claire et rapide à utiliser, partout.",
  done=["Coran, Adhkar et horaires de prière selon la position","Rappels et routine quotidienne","Publiée sur l’App Store et Google Play"],
  tech="iOS natif · Android natif · Firebase",link="/zikr.html"),
 dict(n="Kinto",icon="kinto-icon.png",shot="kinto-screen1.jpg",tag="Application mobile",
  need="Suivre son budget sans effort, sans saisie fastidieuse.",
  done=["Scan des reçus","Dépenses par catégorie","Vue claire des revenus et des économies"],
  tech="React Native (Expo) · Supabase",link="/kinto.html"),
]
p=head("Projets sur mesure — Nour Groupe","Exemples de projets réalisés par Nour Groupe : Fadz, Zikr, Kinto. Application, site web, plateforme.","/projets.html")
p+='''<section class="hero small-hero"><div class="glow"></div><div class="wrap"><p class="eyebrow">Projets</p><h1>Ce qu’on sait <span class="grad">construire.</span></h1>
<p class="lead">Trois produits conçus et publiés en interne : voici comment un besoin devient une application.</p></div></section>'''
for c in CASES:
    p+=f'''<section class="wrap sec"><article class="showcase case">
<div class="sc-copy"><div class="sc-head"><img src="assets/{c['icon']}" alt="" width="64" height="64"><div><h3>{c['n']}</h3><span class="pill">{c['tag']}</span></div></div>
<h4>Le besoin</h4><p class="muted">{c['need']}</p>
<h4>Ce qu’on a réalisé</h4><ul class="done">{"".join(f"<li>{x}</li>" for x in c['done'])}</ul>
<p class="small">{c['tech']}</p><p><a class="btn" href="{c['link']}">Voir {c['n']}</a></p></div>
<div class="sc-shots">{phone(c['shot'],c['n'],'s1')}</div></article></section>'''
p+='''<section class="wrap sec"><div class="band"><div><h2>Un projet similaire ?</h2><p class="muted">Décrivez-nous votre besoin, on vous répond en général sous quelques jours.</p></div><a class="btn" href="/contact.html">Parler de mon projet</a></div></section>'''+foot()
write("projets.html",p)
