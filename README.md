# Lorenzo Devicienti — Portfolio

Sito personale pubblicato con GitHub Pages: https://l0renx0.github.io/LorenzoWebSite/

Una sola pagina in tre lingue, in HTML, CSS e JavaScript semplici, senza framework.

| Lingua   | Indirizzo |
|----------|-----------|
| English  | `/`       |
| Italiano | `/it/`    |
| Español  | `/es/`    |

## Struttura

```
index.html, it/, es/   Pagine generate (non modificarle a mano)
404.html               Pagina "non trovata" (generata)
about/ photo/ ...      Vecchi indirizzi: portano alla sezione giusta (generati)
assets/css/style.css   Stile di tutto il sito (colori e misure in :root)
assets/js/main.js      Interazioni: motto-poster, menu, galleria, tema, lingua
assets/img/            Immagini
_build/build.py        Genera tutte le pagine: testi in inglese e struttura
_build/i18n.py         Traduzioni in italiano e spagnolo, righe del motto per lingua
_build/manifest.json   Elenco e ordine delle immagini
```

## Modificare il sito

1. Cambia i testi in `_build/build.py` (inglese) e le traduzioni in `_build/i18n.py`.
2. Rigenera le pagine:

   ```bash
   python3 _build/build.py
   ```

3. Fai commit e push su `main`: GitHub Pages pubblica in un paio di minuti.

Per vederlo in locale: `python3 -m http.server` dalla cartella che contiene il repository, poi apri `http://localhost:8000/LorenzoWebSite/`.
