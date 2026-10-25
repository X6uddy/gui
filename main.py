import argparse

from lab_runner import LabRunner


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Запуск лабораторной работы")
    parser.add_argument("lab", type=int, nargs="?", default=4, choices=[1, 2, 3, 4],
                        help="номер лабораторной работы (по умолчанию 4)")
    args = parser.parse_args()

    runner = LabRunner()
    getattr(runner, f"start_{args.lab}_lab")()
