import argparse
import random
import time
import importlib
import numpy as np

from tttarena.bots.simple_bot import SimpleBot
from tttarena.engine.core.engine import TetrisEngine
from tttarena.simulator.logger import save_log
from tttarena.simulator.runner import SimulationRunner

VISUALIZERS = {
    "cli": {"module": "tttarena.simulator.visualizers.cli_visualizer", "class": "CliVisualizer"},
    "pygame": {"module": "tttarena.simulator.visualizers.pygame_visualizer", "class": "PygameVisualizer"},
}

def main():
    """Запускает симуляцию."""
    parser = argparse.ArgumentParser(description="Запуск симуляции")
    parser.add_argument(
        "--seed", type=int, required=True, help="Запустить новую симуляцию с указанным сидом"
    )
    parser.add_argument(
        "--render",
        type=str,
        choices=list(VISUALIZERS.keys()),
        default=None,
        help="Включить визуализацию (cli или pygame)",
    )
    args = parser.parse_args()

    print(f"Инициализация симуляции с сидом: {args.seed}...")
    random.seed(args.seed)
    np.random.seed(args.seed)

    bot = SimpleBot()
    engine = TetrisEngine(width=10, height=20, seed=args.seed)
    runner = SimulationRunner(engine, bot)

    start_time = time.time()
    
    visualizer = None
    if args.render:
        visualizer_info = VISUALIZERS[args.render]
        module = importlib.import_module(visualizer_info["module"])
        visualizer_class = getattr(module, visualizer_info["class"])
        visualizer = visualizer_class()
    
    results = runner.run(
        start_time=start_time,
        visualizer=visualizer,
    )
    duration = time.time() - start_time

    print("Симуляция завершена.")
    print("\n" + "=" * 20 + " ИТОГОВЫЕ РЕЗУЛЬТАТЫ " + "=" * 20)
    print(f"Продолжительность: {duration:.2f} сек.")
    print(f"Сид: {results['seed']}")
    print(f"Итоговый счет (S): {results['final_score_S']}")
    print(f"Ошибка аппроксимации (A): {results['final_error_A']:.4f}")
    print(f"ФИНАЛЬНАЯ МЕТРИКА: {results['final_metric']:.4f}")
    print(f"RPS: {results['final_rps']:.2f}")
    print("=" * 62)

    save_log(results, args.seed)

if __name__ == "__main__":
    main()
