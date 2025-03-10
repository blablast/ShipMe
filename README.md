# ShipMe Data Warehouse

Projekt hurtowni danych dla fikcyjnej firmy logistycznej ShipMe, przechowujący dane o przesyłkach, trasach, pojazdach, magazynach i innych aspektach operacyjnych. Hurtownia danych działa w schemacie gwiazdy, z tabelami faktów (`fact_`) i wymiarów (`dim_`).

Projekt używa PostgreSQL jako bazy danych, Docker do uruchomienia środowiska, SQLAlchemy jako ORM do definicji schematu, Alembic do migracji oraz Pythona do procesów ETL, generowania danych testowych i analizy danych. Aplikacja frontendowa jest zbudowana w Streamlit i umożliwia interaktywną analizę danych.

## Wymagania

Aby uruchomić projekt, potrzebujesz następujących narzędzi:
- **Docker i Docker Compose**: Do uruchomienia PostgreSQL w kontenerze.
- **Python 3.9+**: Do uruchamiania skryptów ETL, generowania danych i analiz.
- System operacyjny: Linux, macOS lub Windows (z WSL2 dla Dockera na Windows).

## Struktura projektu
```
ShipMe/
├── app.py                      # Główny plik aplikacji Streamlit
├── docker-compose.yml          # Definicja kontenera PostgreSQL
├── src/                        # Kod źródłowy projektu
│   ├── analysis/               # Skrypty analityczne
│   │   ├── init.py
│   │   └── queries.py          # Przykładowe zapytania SQL
│   ├── etl/                    # Skrypty ETL
│   │   ├── init.py
│   │   ├── generate_data.py    # Generowanie danych testowych
│   │   └── load_data.py        # Ładowanie danych do bazy
│   ├── migrations/             # Migracje Alembic
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   ├── versions/
│   │   └── ...
│   ├── models/                 # Modele SQLAlchemy (tabele)
│   │   ├── init.py
│   │   ├── dim_customer.py
│   │   ├── fact_shipments.py
│   │   └── ... (inne modele)
│   ├── pages/                  # Strony analiz dla Streamlit
│   │   ├── init.py
│   │   ├── avg_delivery_time_by_city.py
│   │   ├── most_frequent_drivers.py
│   │   └── ... (inne strony)
│   ├── templates/              # Szablony wyświetlania stron
│   │   ├── init.py
│   │   └── display_template.py
│   └── config.py               # Konfiguracja (np. dane do połączenia z bazą)
├── requirements.txt            # Zależności Pythona
└── README.md                   # Instrukcja uruchomienia projektu
```

## Uruchomienie projektu

### 1. Uruchom PostgreSQL w Dockerze
1. Upewnij się, że masz zainstalowany Docker i Docker Compose. Możesz pobrać je z [oficjalnej strony Dockera](https://www.docker.com/get-started).
2. W katalogu głównym projektu (`ship_me/`) uruchom następującą komendę, aby uruchomić PostgreSQL w kontenerze:
   ```bash
   docker-compose up -d
   ```
   To uruchomi PostgreSQL na porcie 5432 z bazą danych `ship_me_db`, użytkownikiem `ship_me_user` i hasłem `ship_me_password`.
3. Sprawdź, czy kontener działa:
   ```bash
   docker ps
   ```
    Powinieneś zobaczyć kontener z nazwą `shipme_postgres_1`.
4. Włącz POstGIS w kontenerze:
   ```bash
   docker exec -it shipme-postgres-1 psql -U ship_me_user -d ship_me_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"
   ```
   ```bash
   docker exec -it shipme-postgres-1 psql -U ship_me_user -d ship_me_db -c "DROP EXTENSION IF EXISTS postgis_tiger_geocoder CASCADE;DROP EXTENSION IF EXISTS postgis_topology CASCADE;DROP EXTENSION IF EXISTS fuzzystrmatch CASCADE;"
   ```
### 2. Zainstaluj zależności Pythona
1. Utwórz wirtualne środowisko Pythona (zalecane):
   ```bash
   python -m venv venv
   ```
2. Aktywuj wirtualne środowisko:
Windows:
   ```bash
   .\venv\Scripts\Activate.ps1
   ```
Linux/macOS:
   ```bash
   source venv/bin/activate
   ```
3. Zainstaluj zależności z pliku `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Wykonaj migracje Alembic
1. Przejdź do katalogu `src/`:
   ```bash
   cd src
   ```
2. Zastosuj migracje do bazy danych:
   ```bash
   alembic upgrade head
   ```
**Uwaga**: Folder `migrations/` powinien już istnieć w projekcie. Jeśli go nie ma, upewnij się, że poprawnie sklonowałeś repozytorium lub skontaktuj się z twórcą projektu.
Jeśli chcesz utworzyć nową migrację, wykonaj:
```bash
   alembic revision --autogenerate -m "Nazwa migracji"
 ```
Następnie wykonaj migracje ponownie.

**Uwaga**: Jeśli chcesz zresetować bazę danych, możesz usunąć kontener Docker i utworzyć go ponownie:
```bash
   docker-compose down
   docker-compose up -d
```
Następnie wykonaj migracje ponownie.

### 4. Wygeneruj i załaduj dane testowe
W katalogu `src/` uruchom skrypt do generowania i ładowania danych testowych
```bash
  python etl/load_data.py
```
Skrypt ten generuje dane testowe (używając biblioteki Faker) i ładuje je do bazy danych.

### 5. Uruchom aplikację Streamlit
1. W katalogu głównym projektu uruchom aplikację Streamlit:
   ```bash
   streamlit run app.py
    ```  
2. Otwórz przeglądarkę i przejdź do adresu wskazanego przez Streamlit (domyślnie http://localhost:8501).

## Struktura bazy danych
Hurtownia danych działa w schemacie gwiazdy i zawiera 15 tabel podzielonych na tabele faktów (`fact_`) i wymiarów (`dim_`):

Tabele faktów:
- `fact_shipments`: Dane o przesyłkach (np. waga, koszt, czas dostawy).
- `fact_vehicleUsage`: Dane o wykorzystaniu pojazdów (np. dystans, zużycie paliwa).
- `fact_warehouseActivity`: Dane o aktywnościach magazynowych (np. przyjęcia, wydania).

Tabele wymiarów:
- `dim_customer`: Klienci (nadawcy i odbiorcy).
- `dim_route`: Trasy.
- `dim_vehicle`: Pojazdy.
- `dim_driver`: Kierowcy.
- `dim_warehouse`: Magazyny.
- `dim_product`: Produkty w przesyłkach.
- `dim_date`: Wymiar czasowy.
- `dim_fuel`: Dane o paliwie.

Szczegółowy opis każdej tabeli znajdziesz w plikach w katalogu `src/models/`.

## Analizy dostępne w aplikacji Streamlit
Aplikacja Streamlit (`app.py`) umożliwia interaktywną analizę danych w następujących kategoriach:
- **Analizy czasowe**: trendy w czasie (np. czasy dostaw, efektywność kierowców).
- **Analizy transportowe**: dane związane z transportem (np. koszty paliwa, ranking kierowców).
- **Analizy magazynowe**: informacje o magazynach (np. całkowita waga).
- **Analizy geograficzne**: wizualizacje przestrzenne (np. rozkład tras).
- **Schematy**: schematy tabel faktów w formie diagramów.

Każda analiza zawiera opis celu, kod SQL zapytania, tabelę wyników oraz wykres (jeśli dotyczy).

## Rozwój projektu
Jeśli chcesz dodać nowe analizy:
1. Utwórz nowy plik w `src/pages/` (np. `new_analysis.py`).
2. Zdefiniuj funkcję `get_page_content()` zwracającą dane w formacie zgodnym z szablonem `render_page`.
3. Dodaj nową analizę do listy `grouped_analyses` w `app.py`.