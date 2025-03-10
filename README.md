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
