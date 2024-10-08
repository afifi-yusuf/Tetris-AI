Tetris AI Autoplayer

Welcome to the Tetris AI Autoplayer project! This project is designed to create an AI that plays Tetris automatically while adhering to specific constraints, such as a maximum number of blocks and additional scoring for consecutive rows destroyed in a single move.

Table of Contents

	•	Introduction
	•	Features
	•	Constraints
	•	How It Works

Introduction

Tetris is a classic puzzle game where players rotate and place falling blocks (Tetrominoes) to clear rows on the game board. This AI implementation focuses on optimizing gameplay by using algorithms to make decisions based on the current state of the board and pre-defined scoring rules.

Features

	•	Autoplay Mechanism: Automatically plays Tetris using AI algorithms.
	•	Scoring System: Additional points for clearing multiple rows in one go.
	•	Constraint Handling: Enforces a maximum number of blocks to be placed.
	•	Visualization: Real-time board visualization to see AI decisions in action.

Constraints

	•	Maximum Number of Blocks: The AI can only place a limited number of blocks in a single game session.
	•	Row Clearing Bonus: The AI receives bonus points for clearing multiple rows simultaneously.

How It Works

The Tetris AI uses a combination of heuristics and algorithms to determine the best move for each incoming Tetromino. Key components include:

	1.	Evaluation Function: Scores potential placements based on the number of rows cleared, the height of the board, and other metrics.
	2.	Search Algorithm: Implements a search strategy to explore possible placements and select the optimal one.
	3.	Game State Management: Keeps track of the current game state, including the position of blocks and score.
