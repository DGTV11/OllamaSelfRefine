# OllamaSelfRefine
An implementation of the SELF-REFINE iterative feedback and refinement approach for LLMs using Ollama

## Installation
1) Install Python 3.10+ and Ollama

2) Install Python dependencies
```sh
pip install -r requirements.txt
```

3) Install an Ollama model (default model used: `phi3`)

## Usage
1) Edit constants.py if required (e.g. you are using a different Ollama model)

2) Run OllamaSelfRefine
```sh
python3 main.py
```

## References
- Madaan, Aman, et al. ‘Self-Refine: Iterative Refinement with Self-Feedback’. arXiv [Cs.CL], 2023, http://arxiv.org/abs/2303.17651. arXiv.
- Saravia, Elvis. ‘Prompt Engineering Guide’. https://github.com/dair-ai/Prompt-Engineering-Guide, 12 2022.
