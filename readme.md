<h2>FORMULARZ</h2>

<h3>Cel:</h3> 

Zbieranie wyników wypełnionych formularzy, poddanie ich analizie i wyświetlenie wyników.

<h3>Opis działania:</h3>

<ul>
<li>Aplikacja umożliwia stworzenie kont administratora oraz użytkownika. Konta będą posiadały osobne upranienia.</li>
<li>Administrator będzie miał możliwość zalogowania się do swojego panelu.</li>
<li>Administrator będzie miał możliwość zdefiniowania pytań w formularzu.</li>
<li>Pytania zostaną zapisane w badzie danych SQLite3.</li>
<li>Administrator będzie miał możliwość wyświetlenia pytań w przegladarce oraz usuwania poszczególnego pytania.</li>
<li>Formularz będzie prezentowany w przeglądarce.</li>
<li>Użytkownicy będą mogli  zarejestrować się przez panel "Register", a nastepnie zalogować się do formularza.</li>
<li>Użytkownicy wypełnią formularz, który zostanie zapisany w badzie danych.</li>
<li>Administrator po wypełnieniu formularza będzię mial możliwość przgladania wyników ankiety w postaci średniej procentowej względem konkretnego pytania.</li>
<li>Administrator będzie miał możliwość analizy danych zapisanych w bazie.</li>
</ul>

<h4>Lista alertów:<h4>

<ul>
<li>Sprawdzenie hasła oraz loginu w panelu "Login".</li>
<li>Walidacja hasła w panelu "Register".</li>
<li>Walidacja loginu w panelu "Register".</li>
<li>Dodanie pytania do bazy.</li>
<li>Aplikacja zapisuje konkretne zdarzenia w logach - w pliku "form_app.log".</li>
</ul>

<h3>Instrukcja uruchomienia:</h3>

<ol>
<li>Uruchom plik data_init.py</li>
<li>W celu utworzenia dodatkowych kont "Admin" uruchom plik create_Admin_account.py</li>
<li>W pliku session_k.txt wpisz dowolny ciąg znaków</li>
<li>Uruchom plik app.py</li>
</ol>

<h3>API {"json"}:</h3>
<h5> Dostępne tylko dla zalogowanych użytkowników z uprawnieniami 'Admin'</h5>
<ul>
<li>"/api/uzytkownicy"  - zestawienie wszystkich dostępnych użytkowników.</li>
<li>"/api/pytania"  - zestawienie pytań wykożystywanych obecnie do ankiety.</li>
<li>"/api/odpowiedzi"  - zestawienie wszystkich odpowiedzi z przeprowadzonych ankiet.</li>

</ul>

<h3>Wideoprezentacja:</h3>

<link>https://drive.google.com/file/d/1jxGh9hS_T9C9cU1thLFjw2iagYTiPX5B/view</link>

----------

 NARZĘDZIA: 
<h3>Python 3.7, SQLite3, SQL, Flask, Jinja2, HTML5, CSS3, HTTP, Git.</h3>
