# Reasoning and Evaluation Dataset Generator

This project provides a set of modular Python scripts and utilities for generating, verifying, and evaluating synthetic reasoning datasets across formal systems such as logic, symbolic differentiation, lambda calculus, and more.

## Features

- Curriculum-based dataset generation across logic systems
- Symbolic and syntactic verifiers for generated outputs
- Modular and extensible design for adding new task types
- Support for curriculum learning and formal grammars

## Project Structure

- `Curriculum.py`, `Generator.py`, `Verifier.py`: Top-level generic task modules
- `SAT_QBF/`, `lambda_calculus_reduction/`, `symbolic_differentiation/`, etc.: Task-specific generators and evaluators
- `synthetic_formal_system/`: Formal system evaluation and prompt engineering utilities
- `context_free_grammar/`: Tools for structured CFG generation and validation

## Usage

1. Install any required packages or environments.
2. Run any `gen_data.py` or `Generator.py` to create new samples.
3. Use `Verifier.py` or curriculum logic to validate or evaluate outputs.

## License

Distributed for research and educational purposes only.