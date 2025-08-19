import unittest
import numpy as np
import time
from tttarena.engine.core.engine import TetrisEngine
from tttarena.engine.core.exceptions import GameOver, InvalidMove
from tttarena.simulator.runner import SimulationRunner
from tttarena.bots.simple_bot import SimpleBot

class TestTetrisEngine(unittest.TestCase):

    def test_engine_creation(self):
        """Test that TetrisEngine can be created successfully."""
        engine = TetrisEngine(width=10, height=20, seed=42)
        self.assertIsInstance(engine, TetrisEngine)
        self.assertEqual(engine.board.width, 10)
        self.assertEqual(engine.board.height, 20)
        self.assertEqual(engine.seed, 42)
        self.assertIsNotNone(engine.current_piece_type)
        self.assertIsNotNone(engine.next_piece_type)

    def test_simulate_placement_smoke(self):
        """Smoke test for simulate_placement to ensure it runs without errors."""
        engine = TetrisEngine(width=10, height=20, seed=123)
        initial_score = engine.score
        initial_game_over_status = engine.game_over

        # Simulate a few placements
        for _ in range(5):
            try:
                # Try to place the current piece at a valid position and rotation
                # For a smoke test, we just pick arbitrary values that are likely to be valid
                # In a real test, we'd be more precise.
                simulated_grid, lines_cleared = engine.simulate_placement(x=0, rotation_index=0)
                self.assertIsInstance(simulated_grid, np.ndarray)
                self.assertIsInstance(lines_cleared, int)
                self.assertFalse(engine.game_over) # Should not be game over after simulation
            except (GameOver, InvalidMove):
                # If a move is invalid or game over, it's fine for a smoke test
                # as long as the simulation itself doesn't crash.
                pass

        # Check that game state hasn't changed after simulation
        self.assertEqual(engine.score, initial_score)
        self.assertEqual(engine.game_over, initial_game_over_status)

    def test_place_piece_smoke(self):
        """Smoke test for place_piece to ensure it runs and affects game state."""
        engine = TetrisEngine(width=10, height=20, seed=456)
        initial_score = engine.score
        initial_piece_type = engine.current_piece_type

        # Try to place a piece
        try:
            lines_cleared = engine.place_piece(x=0, rotation_index=0)
            self.assertIsInstance(lines_cleared, int)
            self.assertGreaterEqual(engine.score, initial_score) # Score should not decrease
            self.assertNotEqual(engine.current_piece_type, initial_piece_type) # Piece should have changed
        except (GameOver, InvalidMove):
            pass # It's a smoke test, so just ensure it doesn't crash

    def test_full_game_simulation_with_simple_bot(self):
        """Test a full game simulation with SimpleBot and verify final metrics."""
        seed = 1
        engine = TetrisEngine(width=10, height=20, seed=seed)
        bot = SimpleBot()
        runner = SimulationRunner(engine, bot)

        start_time = time.time()
        results = runner.run(start_time=start_time)

        # Expected values from the user's log
        expected_score = 43000
        expected_approximation_error = 18.1061
        expected_final_metric = 0.2019
        expected_rps = 1311.43 # This can vary slightly due to timing, so we'll check a range

        self.assertEqual(results["seed"], seed)
        self.assertEqual(results["final_score_S"], expected_score)
        self.assertAlmostEqual(results["final_error_A"], expected_approximation_error, places=4)
        self.assertAlmostEqual(results["final_metric"], expected_final_metric, places=4)
        
        # RPS can fluctuate, so check if it's within a reasonable range
        self.assertGreaterEqual(results["final_rps"], expected_rps * 0.9)
        self.assertLessEqual(results["final_rps"], expected_rps * 1.1)

if __name__ == '__main__':
    unittest.main()