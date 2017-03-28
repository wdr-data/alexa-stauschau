## Dialog Launch

<script src="https://cdn.rawgit.com/knsv/mermaid/6.0.0/dist/mermaid.min.js"></script>
<div class="mermaid">
sequenceDiagram
User->> Alexa: Query intent
Note left of User: Alexa, starte WDR Verkehr
Alexa->> User: Answer
Note right of Alexa: Nennen Sie eine Strecke, zum Beispiel A1.
User->>Alexa: Query
Note left of User: A1
Alexa->>User: Answer
Note right of Alexa: A1, Dortmund Richtung Köln zwischen Burscheid und Kreuz Leverkusen: 8 Km Stau. Zeitverlust: mehr als 20 Minuten.
Note right of Alexa: Nennen sie noch eine weitere Strecke oder sagen Sie Stopp.
User->>Alexa: Query
Note left of User: A2
Alexa->>User: Answer
Note right of Alexa: Keine Meldungen für die A2.
Note right of Alexa: Nennen sie noch eine weitere Strecke oder sagen Sie Stopp.
User->>Alexa: Stopp
Note left of User: Stopp
Alexa->>User: Stopp Answer
Note right of Alexa: Gute Fahrt!
</div>

## OneShot Launch
<div class="mermaid">
sequenceDiagram
User->> Alexa: OneShot
Note left of User: Alexa, frage WDR Verkehr nach A1
Alexa->>User: Answer
Note left of Alexa: A1, Dortmund Richtung Köln zwischen Burscheid und Kreuz Leverkusen: 8 Km Stau. Zeitverlust: mehr als 20 Minuten.  
Note left of Alexa: Nennen sie noch eine weitere Strecke oder sagen Sie Stopp.
User->>Alexa: Query
Note left of User: A7
Alexa->>User: Answer
Note right of Alexa: Keine Meldungen für die A7.
Note right of Alexa: Nennen sie noch eine weitere Strecke oder sagen Sie Stopp.
User->>Alexa: Stopp
Note left of User: Stopp
Alexa->>User: Stopp Answer
Note right of Alexa: Tschüs!
</div>

## Error Handling
<div class="mermaid">
sequenceDiagram
User->> Alexa: Query
Note left of User: A irgendwas
Alexa->>User: Repeat
Note right of Alexa: Kannst Du das noch einmal wiederholen?
User->> Alexa: Unclear match
Note left of User: Mach 3
Alexa->>User: Answer if unclear
Note right of Alexa: Keine Meldungen für die "Mach 3"
Note right of Alexa: Nennen sie noch eine weitere Strecke oder sagen Sie Stopp.
User->>Alexa: > 8 sec. not responding.
Note left of User: ...
Alexa->>User: Error answer
Note right of Alexa: Beim angeforderten Skill ist ein Fehler aufgetreten.
</div>
