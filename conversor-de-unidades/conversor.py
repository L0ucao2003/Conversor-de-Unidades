"""Conversor de unidades de medida."""

from __future__ import annotations

import sys

UNITS = {
    "comprimento": {
        "m": 1.0,
        "km": 1000.0,
        "cm": 0.01,
        "mm": 0.001,
        "in": 0.0254,
        "ft": 0.3048,
    },
    "area": {
        "m2": 1.0,
        "km2": 1_000_000.0,
        "cm2": 0.0001,
        "mm2": 0.000001,
        "ha": 10_000.0,
        "ac": 4046.8564224,
    },
    "volume": {
        "l": 1.0,
        "ml": 0.001,
        "m3": 1000.0,
        "cm3": 0.001,
        "gal": 3.785411784,
    },
}


def normalize_name(name: str) -> str:
    return name.strip().lower().replace(" ", "")


def list_units(category: str) -> list[str]:
    return list(UNITS[category].keys())


def convert_value(category: str, value: float, from_unit: str, to_unit: str) -> float:
    normalized_category = normalize_name(category)
    from_key = normalize_name(from_unit)
    to_key = normalize_name(to_unit)

    if normalized_category not in UNITS:
        raise ValueError(f"Categoria inválida: {category}")

    category_units = UNITS[normalized_category]
    if from_key not in category_units:
        raise ValueError(f"Unidade de origem inválida para {normalized_category}: {from_unit}")
    if to_key not in category_units:
        raise ValueError(f"Unidade de destino inválida para {normalized_category}: {to_unit}")

    value_in_base = value * category_units[from_key]
    return value_in_base / category_units[to_key]


def ask_for_category() -> str:
    print("Escolha a categoria:")
    for index, category in enumerate(UNITS.keys(), start=1):
        print(f"  {index}. {category}")

    while True:
        try:
            choice = int(input("Opção: ").strip())
        except ValueError:
            print("Entrada inválida. Digite um número.")
            continue

        categories = list(UNITS.keys())
        if 1 <= choice <= len(categories):
            return categories[choice - 1]
        print("Opção inválida. Tente novamente.")


def ask_for_unit(category: str, prompt: str) -> str:
    units = list_units(category)
    print(f"Unidades disponíveis em {category}:")
    print(", ".join(units))

    while True:
        unit = input(f"{prompt}: ").strip()
        normalized = normalize_name(unit)
        if normalized in {normalize_name(u) for u in units}:
            return next(u for u in units if normalize_name(u) == normalized)
        print("Unidade inválida. Escolha uma das opções listadas.")


def run_interactive() -> None:
    category = ask_for_category()
    value = float(input("Digite o valor: ").strip().replace(",", "."))
    from_unit = ask_for_unit(category, "Unidade de origem")
    to_unit = ask_for_unit(category, "Unidade de destino")

    result = convert_value(category, value, from_unit, to_unit)
    print(f"\n{value} {from_unit} = {result:.6f} {to_unit}")


def run_cli(args: list[str]) -> None:
    if len(args) != 4:
        print("Uso: python conversor.py <categoria> <valor> <unidade_origem> <unidade_destino>")
        print("Categorias disponíveis: " + ", ".join(UNITS.keys()))
        raise SystemExit(1)

    category, value_str, from_unit, to_unit = args
    try:
        value = float(value_str.replace(",", "."))
    except ValueError as exc:
        raise ValueError(f"Valor inválido: {value_str}") from exc

    result = convert_value(category, value, from_unit, to_unit)
    print(f"{value} {from_unit} = {result:.6f} {to_unit}")


def main() -> None:
    if len(sys.argv) > 1:
        run_cli(sys.argv[1:])
        return
    run_interactive()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, SystemExit):
        raise
