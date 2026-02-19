# Esercizio 60: Gestione Studenti (Menu CLI) - Versione Semplificata

## Obiettivo
Realizzare una applicazione interattiva a menu per gestire una lista di studenti
salvata in file JSON. Uso menu in console, cicli for espliciti, separazione tra 
logica (funzioni che ritornano valori) e presentazione (print nel main).

## Requisiti
- **Storage**: file `studenti.json` (UTF-8, indentato)
- **Comandi via menu**: aggiungi, visualizza, cerca, filtra, aggiorna, cancella, statistiche
- **Identificatori**: indice progressivo (posizione nella lista)
- **Persistenza**: carica/salva JSON automaticamente
- **Sintassi semplice**: cicli for, senza list comprehension, niente argparse
- **Architettura**: funzioni ritornano dati/messaggi, main gestisce output

## Struttura dati
```python
studenti = [
    {"nome": "Alice", "voto": 8.5},
    {"nome": "Bob", "voto": 7.0},
    {"nome": "Carlo", "voto": 9.0}
]
```

## Funzioni - Validazione

```python
def valida_voto(voto_str) -> list[bool, str | float]
    """Validate vote. Returns (is_valid, value_or_error)."""
```

## Funzioni - I/O Formattazione

```python
def formatta_lista(studenti) -> str
    """Format student list as string. Returns formatted output."""

def mostra_dettaglio(studenti, indice) -> list[bool, str, dict | None]
    """Show detail for one student. Returns (success, message, data)."""
```

## Funzioni - Operazioni CRUD

```python
def aggiungi_studente(studenti) -> list[bool, str, dict | None]
    """Add student. Returns (success, message, new_student)."""

def cancella_studente(studenti) -> list[bool, str]
    """Delete student by index. Returns (success, message)."""

def aggiorna_studente(studenti) -> list[bool, str]
    """Update student voto. Returns (success, message)."""
```

## Funzioni - Ricerca e Filtro

```python
def ricerca_per_nome(studenti, termine=None) -> list
    """Search students by name. Returns list of results."""

def filtra_per_voto(studenti, min_voto=None, max_voto=None) -> list
    """Filter by grade range. Returns list of results."""
```

## Funzioni - Statistiche

```python
def calcola_media(studenti) -> float
    """Calculate average grade. Returns float."""

def trova_migliore(studenti) -> dict | None
    """Find best student. Returns student dict or None."""

def trova_peggiore(studenti) -> dict | None
    """Find worst student. Returns student dict or None."""
```

## Funzioni - I/O e Main

```python
def load_studenti(path=STORAGE_FILE) -> list
    """Load from JSON. Return empty list if not found."""

def save_studenti(studenti, path=STORAGE_FILE) -> None
    """Save to JSON file."""

def main() -> None
    """Main menu loop - handles all output."""
```

## Menu principale
```
=== GESTIONE STUDENTI ===
1. Aggiungi studente
2. Visualizza lista
3. Visualizza dettaglio (per indice)
4. Aggiorna voto
5. Cancella studente
6. Ricerca per nome
7. Filtra per voto (range)
8. Statistiche (media, migliore, peggiore)
9. Esci
Scelta:
```

## Comandi dettaglio

**Aggiungi**: chiede nome e voto, valida (voto 0-10), ritorna (success, msg, student).

**Visualizza lista**: formatta e stampa tutti con indice.
```
0. Alice - Voto: 8.5
1. Bob - Voto: 7.0
2. Carlo - Voto: 9.0
```

**Visualizza dettaglio**: chiede indice, mostra nome e voto.

**Aggiorna**: chiede indice e nuovo voto, valida, aggiorna. Ricorda di mostrare lista prima.

**Cancella**: chiede indice, rimuove studente.

**Ricerca**: chiede termine, cerca substring in nomi (case-insensitive). Ritorna lista di risultati.

**Filtra**: chiede min/max voto, ritorna lista di studenti in range.

**Statistiche**: mostra
- Numero totale studenti
- Media voti (formato: `media:.2f`)
- Voto più alto (nome + voto)
- Voto più basso (nome + voto)

**Esci**: salva automaticamente in JSON e termina.

## Validazione
- Nome obbligatorio (non vuoto)
- Voto numerico tra 0 e 10
- Indice deve essere valido
- Funzione `valida_voto()` centralizza la logica di validazione

## Note Architettura
- **Separazione logica/presentazione**: funzioni ritornano (success, msg, data) o liste
- **Main gestisce output**: tutti i print sono nel main, non nelle funzioni
- **Testabilità**: funzioni senza side-effect I/O sono facili da testare
- **Riusabilità**: funzioni logiche usabili da API, GUI, CLI, ecc.
- Niente UUID, niente argparse
- Usare `for` loop, niente list comprehension
- Messaggi chiari e user-friendly

