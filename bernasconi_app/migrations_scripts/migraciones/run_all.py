import _01_materiales
# from migraciones import _02_ficha_tecnica
# from migraciones import _03_ficha_material


def main():
    print("🚀 INICIO MIGRACIÓN COMPLETA\n")

    _01_materiales.run()
    # _02_ficha_tecnica.run()
    # _03_ficha_material.run()

    print("\n✅ MIGRACIÓN COMPLETA FINALIZADA")


if __name__ == "__main__":
    main()
