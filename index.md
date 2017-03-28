## Dialog Launch

<script src="https://cdn.rawgit.com/knsv/mermaid/6.0.0/dist/mermaid.min.js"></script>
<div class="mermaid">
sequenceDiagram
Note left of User: Dialog Launch
User->> Alexa: Query intent
Note left of User: Alexa, starte WDR Verkehr
Alexa->> User: Answer
Note right of Alexa: Nennen Sie eine Strecke, zum Beispiel A1.
User->>Alexa: Query
Note left of Alexa: A1
Alexa->>User: Answer
Note left of Alexa: A1, Dortmund Richtung Köln zwischen Burscheid und Kreuz Leverkusen: 8 Km Stau. Zeitverlust: mehr als 20 Minuten.
Note left of Alexa: Nennen sie noch eine weitere Strecke oder sagen Sie Stopp.
User->>Alexa: Query
Note left of Alexa: A2
Alexa->>User: Answer
Note left of Alexa: Keine Meldungen für die A2.
Note left of Alexa: Nennen sie noch eine weitere Strecke oder sagen Sie Stopp.
User->>Alexa: Stopp
Note left of Alexa: Stopp
Alexa->>User: Stopp Answer
Note left of Alexa: Gute Fahrt!
</div>
<div class="mermaid">
sequenceDiagram
participant John
Note right of John: Text in note
</div>
