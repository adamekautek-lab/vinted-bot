# Vinted watch → Telegram

Malutki, darmowy bot, który co 15 minut sprawdza wybrane wyszukiwania na
Vinted i wysyła Ci powiadomienie na Telegramie, gdy pojawi się nowa
pasująca oferta. Działa na darmowej infrastrukturze GitHub Actions —
nie potrzebujesz własnego serwera ani włączonego komputera 24/7.

## Konfiguracja (jednorazowa)

1. Załóż bota na Telegramie przez **@BotFather** (komenda `/newbot`)
   i zapisz otrzymany **token**.
2. Napisz cokolwiek do swojego nowego bota, potem wejdź w przeglądarce na
   `https://api.telegram.org/bot<TWOJ_TOKEN>/getUpdates` i znajdź swoje
   **chat_id** w odpowiedzi (`"chat":{"id": ...}`).
3. Wrzuć te pliki (zachowując strukturę folderów, łącznie z
   `.github/workflows/`) do nowego, pustego repozytorium na GitHubie.
4. W repo: **Settings → Secrets and variables → Actions → New repository
   secret** — dodaj `TELEGRAM_BOT_TOKEN` i `TELEGRAM_CHAT_ID`.
5. W pliku `vinted_watch.py`, w liście `SEARCH_URLS`, wklej link(i)
   wyszukiwania skopiowane z paska adresu na vinted.pl (filtry — marka,
   rozmiar, cena, stan — ustaw wcześniej normalnie, jak przy ręcznym
   szukaniu, potem skopiuj gotowy link).
6. Zakładka **Actions** w repo → wybierz workflow "Vinted watch" →
   **Run workflow**, żeby sprawdzić, czy wszystko działa od razu, zamiast
   czekać do 15 minut.

Od teraz bot sam sprawdza oferty co 15 minut, 24/7, za darmo — możesz
zamknąć laptopa, to wszystko dzieje się na serwerach GitHuba.

## Uwagi

- Pierwsze uruchomienie tylko zapisuje obecne oferty jako punkt
  startowy (żeby nie zasypało Cię powiadomieniami o wszystkim naraz) —
  właściwe powiadomienia lecą od drugiego przebiegu.
- Repo może być publiczne — token i chat_id siedzą w sekretach GitHuba
  i nigdy nie pojawiają się w kodzie ani w logach.
- Jeśli automatyczny commit z nowymi ID nie zadziała, sprawdź
  **Settings → Actions → General → Workflow permissions → Read and
  write permissions**.
- Chcesz dodać kolejne wyszukiwania? Po prostu dopisz kolejne linki do
  listy `SEARCH_URLS`.
