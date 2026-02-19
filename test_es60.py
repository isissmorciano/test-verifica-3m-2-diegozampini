"""Unit tests for es60_student.py - test logic functions without user input."""

import os
import tempfile
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src/m09_files"))
from src.m09_files.es60_student import (
    load_studenti,
    save_studenti,
    valida_voto,
    formatta_lista,
    mostra_dettaglio,
    ricerca_per_nome,
    filtra_per_voto,
    calcola_media,
    trova_migliore,
    trova_peggiore,
)


class TestValidazione:
    def test_valida_voto_valido(self):
        """Test valid vote validation."""
        is_valid, result = valida_voto("7.5")
        assert is_valid is True
        assert result == 7.5

    def test_valida_voto_zero(self):
        """Test zero vote."""
        is_valid, result = valida_voto("0")
        assert is_valid is True
        assert result == 0.0

    def test_valida_voto_dieci(self):
        """Test max vote."""
        is_valid, result = valida_voto("10")
        assert is_valid is True
        assert result == 10.0

    def test_valida_voto_troppo_alto(self):
        """Test vote > 10."""
        is_valid, result = valida_voto("11")
        assert is_valid is False

    def test_valida_voto_negativo(self):
        """Test negative vote."""
        is_valid, result = valida_voto("-1")
        assert is_valid is False

    def test_valida_voto_non_numero(self):
        """Test non-numeric vote."""
        is_valid, result = valida_voto("abc")
        assert is_valid is False


class TestLoadSave:
    def test_load_empty_file_not_exists(self):
        """Test loading from non-existent file returns empty list."""
        result = load_studenti("/tmp/nonexistent_xyz.json")
        assert result == []

    def test_save_and_load(self):
        """Test saving and loading data."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
            path = f.name

        try:
            data = [{"nome": "Alice", "voto": 8.5}, {"nome": "Bob", "voto": 7.0}]
            save_studenti(data, path)
            loaded = load_studenti(path)
            assert len(loaded) == 2
            assert loaded[0]["nome"] == "Alice"
            assert loaded[1]["voto"] == 7.0
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_load_corrupted_json(self):
        """Test loading corrupted JSON returns empty list."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
            path = f.name
            f.write("{ invalid json }")

        try:
            result = load_studenti(path)
            assert result == []
        finally:
            if os.path.exists(path):
                os.unlink(path)


class TestFormattaLista:
    def test_formatta_lista_vuota(self):
        """Test formatting empty list."""
        output = formatta_lista([])
        assert output == "Nessuno studente."

    def test_formatta_lista_uno(self):
        """Test formatting single student."""
        studenti = [{"nome": "Alice", "voto": 8.5}]
        output = formatta_lista(studenti)
        assert "0. Alice - Voto: 8.5" in output

    def test_formatta_lista_molti(self):
        """Test formatting multiple students."""
        studenti = [{"nome": "Alice", "voto": 8.5}, {"nome": "Bob", "voto": 7.0}, {"nome": "Carlo", "voto": 9.0}]
        output = formatta_lista(studenti)
        assert "0. Alice" in output
        assert "1. Bob" in output
        assert "2. Carlo" in output


class TestMostraDettaglio:
    def test_dettaglio_valido(self):
        """Test showing valid student detail."""
        studenti = [{"nome": "Alice", "voto": 8.5}]
        success, msg, data = mostra_dettaglio(studenti, 0)
        assert success is True
        assert "Alice" in msg
        assert "8.5" in msg
        assert data == studenti[0]

    def test_dettaglio_indice_negativo(self):
        """Test invalid negative index."""
        studenti = [{"nome": "Alice", "voto": 8.5}]
        success, msg, data = mostra_dettaglio(studenti, -1)
        assert success is False
        assert data is None

    def test_dettaglio_indice_troppo_alto(self):
        """Test index out of range."""
        studenti = [{"nome": "Alice", "voto": 8.5}]
        success, msg, data = mostra_dettaglio(studenti, 10)
        assert success is False
        assert data is None


class TestRicerca:
    def test_ricerca_esatta(self):
        """Test exact name search."""
        studenti = [{"nome": "Alice", "voto": 8.5}, {"nome": "Bob", "voto": 7.0}]
        risultati = ricerca_per_nome(studenti, "alice")
        assert len(risultati) == 1
        assert risultati[0]["nome"] == "Alice"

    def test_ricerca_substring(self):
        """Test substring search."""
        studenti = [{"nome": "Alice", "voto": 8.5}, {"nome": "Andrea", "voto": 9.0}, {"nome": "Bob", "voto": 7.0}]
        risultati = ricerca_per_nome(studenti, "And")
        assert len(risultati) == 1
        assert risultati[0]["nome"] == "Andrea"

    def test_ricerca_case_insensitive(self):
        """Test case-insensitive search."""
        studenti = [{"nome": "Alice", "voto": 8.5}]
        risultati = ricerca_per_nome(studenti, "ALICE")
        assert len(risultati) == 1

    def test_ricerca_non_trovata(self):
        """Test search with no results."""
        studenti = [{"nome": "Alice", "voto": 8.5}]
        risultati = ricerca_per_nome(studenti, "xyz")
        assert len(risultati) == 0

    def test_ricerca_vuoto(self):
        """Test search with empty term."""
        studenti = [{"nome": "Alice", "voto": 8.5}]
        risultati = ricerca_per_nome(studenti, "")
        assert len(risultati) == 0


class TestFiltra:
    def test_filtra_single_value(self):
        """Test filtering by single value."""
        studenti = [{"nome": "A", "voto": 6.0}, {"nome": "B", "voto": 7.0}, {"nome": "C", "voto": 8.0}]
        risultati = filtra_per_voto(studenti, 7.0, 7.0)
        assert len(risultati) == 1
        assert risultati[0]["nome"] == "B"

    def test_filtra_range(self):
        """Test filtering by range."""
        studenti = [
            {"nome": "A", "voto": 6.0},
            {"nome": "B", "voto": 7.0},
            {"nome": "C", "voto": 8.0},
            {"nome": "D", "voto": 9.0},
        ]
        risultati = filtra_per_voto(studenti, 7.0, 8.5)
        assert len(risultati) == 2
        assert risultati[0]["nome"] == "B"
        assert risultati[1]["nome"] == "C"

    def test_filtra_vuoto(self):
        """Test filtering with no matches."""
        studenti = [{"nome": "A", "voto": 6.0}]
        risultati = filtra_per_voto(studenti, 8.0, 10.0)
        assert len(risultati) == 0

    def test_filtra_min_max_invertiti(self):
        """Test filter with inverted min/max."""
        studenti = [{"nome": "A", "voto": 7.0}]
        risultati = filtra_per_voto(studenti, 9.0, 5.0)
        assert len(risultati) == 0


class TestStatistiche:
    def test_media_vuoto(self):
        """Test average with no students."""
        media = calcola_media([])
        assert media == 0.0

    def test_media_uno(self):
        """Test average of one student."""
        studenti = [{"nome": "A", "voto": 8.0}]
        media = calcola_media(studenti)
        assert media == 8.0

    def test_media_molti(self):
        """Test average of multiple students."""
        studenti = [{"nome": "A", "voto": 6.0}, {"nome": "B", "voto": 8.0}, {"nome": "C", "voto": 10.0}]
        media = calcola_media(studenti)
        assert media == 8.0

    def test_migliore_vuoto(self):
        """Test best student with no students."""
        result = trova_migliore([])
        assert result is None

    def test_migliore_uno(self):
        """Test best student with one student."""
        studenti = [{"nome": "A", "voto": 8.0}]
        result = trova_migliore(studenti)
        assert result["nome"] == "A"

    def test_migliore_molti(self):
        """Test best student with multiple students."""
        studenti = [{"nome": "A", "voto": 6.0}, {"nome": "B", "voto": 9.0}, {"nome": "C", "voto": 7.0}]
        result = trova_migliore(studenti)
        assert result["nome"] == "B"
        assert result["voto"] == 9.0

    def test_peggiore_vuoto(self):
        """Test worst student with no students."""
        result = trova_peggiore([])
        assert result is None

    def test_peggiore_uno(self):
        """Test worst student with one student."""
        studenti = [{"nome": "A", "voto": 8.0}]
        result = trova_peggiore(studenti)
        assert result["nome"] == "A"

    def test_peggiore_molti(self):
        """Test worst student with multiple students."""
        studenti = [{"nome": "A", "voto": 6.0}, {"nome": "B", "voto": 9.0}, {"nome": "C", "voto": 4.0}]
        result = trova_peggiore(studenti)
        assert result["nome"] == "C"
        assert result["voto"] == 4.0


class TestDataManipulation:
    def test_list_operations(self):
        """Test append and pop operations on student list."""
        studenti = []
        s1 = {"nome": "Alice", "voto": 8.5}
        studenti.append(s1)
        assert len(studenti) == 1

        s2 = {"nome": "Bob", "voto": 7.0}
        studenti.append(s2)
        assert len(studenti) == 2

        studenti.pop(0)
        assert len(studenti) == 1
        assert studenti[0]["nome"] == "Bob"

    def test_update_voto(self):
        """Test updating student voto."""
        studenti = [{"nome": "Alice", "voto": 8.0}]
        studenti[0]["voto"] = 9.5
        assert studenti[0]["voto"] == 9.5

    def test_find_by_index(self):
        """Test finding student by index."""
        studenti = [{"nome": "A", "voto": 6.0}, {"nome": "B", "voto": 7.0}, {"nome": "C", "voto": 8.0}]
        assert studenti[1]["nome"] == "B"
        assert studenti[2]["voto"] == 8.0


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
