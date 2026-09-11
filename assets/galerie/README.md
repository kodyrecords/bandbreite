# Galerie-Fotos

Fotos einfach in diesen Ordner legen, committen und auf `main` pushen. Die
GitHub-Action baut das Manifest automatisch neu und die Fotos erscheinen auf
`galerie.html` – neueste zuerst, ohne dass irgendwas an der Seite geändert
werden muss.

## Vorgaben

| | |
|---|---|
| **Dateiformat** | `.jpg` / `.jpeg`, `.png` oder `.webp` (JPEG/WebP für Fotos empfohlen) |
| **Breite** | ca. 1600–2000 px |
| **Qualität (JPEG)** | ca. 80 |
| **Dateigröße** | möglichst unter 500 KB pro Foto |
| **Dateiname** | beliebig – keine Datumspräfixe nötig |

## Warum diese Werte

- **JPEG/WebP statt PNG:** Für Fotos deutlich kleinere Dateigröße bei kaum
  sichtbarem Qualitätsverlust. PNG lohnt sich nur für Grafiken mit
  Transparenz oder wenigen Farben.
- **~1600–2000 px Breite:** Handy-Fotos sind oft 4000 px+ und mehrere MB –
  weit mehr, als im Browser je dargestellt wird. Größere Dateien machen die
  Seite nur langsamer, ohne sichtbaren Vorteil.
- **Dateiname egal:** Die Reihenfolge (neu → alt) ergibt sich automatisch aus
  dem Datum, an dem die Datei zu Git hinzugefügt wurde – nicht aus dem
  Dateinamen.

## Reihenfolge ändern oder Foto entfernen

- **Entfernen:** Datei einfach löschen und committen.
- **Reihenfolge:** richtet sich nach dem Git-Verlauf, lässt sich also nicht
  nachträglich per Umbenennen ändern. Um ein Foto "neuer" wirken zu lassen,
  einmal löschen und in einem späteren Commit erneut hinzufügen.
