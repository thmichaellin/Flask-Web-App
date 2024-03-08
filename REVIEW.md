Student 1: Teun <br>
Student 2: Jade


1. <br>Er zijn een paar stukjes code die refactored kunnen worden naar
functies. Door de code te abstracteren naar een functie, is wordt
app.py meer leesbaar. Bij het checken of een user een admin is
en bij het maken van een SQL-query was dit inderdaad het geval.
Ik heb daarom is_admin(), get_username, get_email en db_query()
toegevoegd aan helpers.py. Deze "functies" worden vaker gebruikt
en zijn volgens mij beter leesbaar dan SQLALchemy queries zoals:
User.query.filter_by(username=username).first().email. <br>
2. <br>Er zijn een paar lijsten die niet helemaal kloppen. Ik 
miste een start time en de volgorder van studentennamen was 
omgekeerd. Deze heb ik gecorrigeerd. Bij de begin tijden heb ik
eerst hardcoded nummers gebruikt maar ze worden nu gegenereerd
door een for-loop. De functionaliteit bestaat nog niet maar als 
een leraar de tijden wil aanpassen, is het veel makkelijker om
een nummer te wijzigen in plaats van 15.
3. <br>Bij de register pagina wordt de studentennaam en 
wachtwoord automatisch ingevuld. Dit is natuurlijk niet de
bedoeling want de pagina is bedoeld voor registratie niet inloggen.
Ik heb het probleem opgezocht en het blijkt een Chrome probleem te
zijn. Ik heb een paar oplossingen geprobeerd zoals het 'name' van
de formuleren te veranderen naar iets anders dan 'username' en
'password' maar dit hielp niet. Ik heb uiteindelijk het zoals het
is laten staan omdat het meer een esthetische probleem is dan een
functionele.
4. <br>Er was een grote bug gevonden bij het submitten van een 
formulier. Als een user meer dan een keer op een submit knopje 
clickt voor dat de redirect gebeurt, word er meerdere versies van
een regel geschreven. Als ik me niet vergis, heet dit "Race
Condition". Ik heb dit opgelost door een stukje javascript te 
gebruiken dat de submit knopje uitzet na het eerste click.
5. <br>Op dit moment werkt het API alleen als ik een email-adres 
bevoegd. Dit kan op dit moment alleen door een invitatie te 
sturen via Google Calendar met bewerkte rechten. Idealiter zou 
ik dit process willen automatiseren omdat het de UX van de app
verslechtert om aan de gebruiker te vragen om op een email te
wachten en dan op een link clicken. Ik heb nu niet genoeg tijd
om dit op te lossen maar er is wel een optie om Access privilege
te geven door middel van Google Calendar API.
