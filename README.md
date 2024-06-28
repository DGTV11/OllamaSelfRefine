# OllamaSelfRefine
An implementation of the SELF-REFINE iterative feedback and refinement approach for LLMs using Ollama

## Installation
1) Install Python 3.10+ and Ollama

2) Install Python dependencies
```sh
pip install -r requirements.txt
```

3) Install an Ollama model (default model used: `qwen2:1.5b`)

## Usage
1) Edit constants.py if required (e.g. you are using a different Ollama model)

2) Run OllamaSelfRefine
```sh
python3 main.py
```

## References
<a id=1>[1]</a>
Aman Madaan and Niket Tandon and Prakhar Gupta and Skyler Hallinan and Luyu Gao and Sarah Wiegreffe and Uri Alon and Nouha Dziri and Shrimai Prabhumoye and Yiming Yang and Shashank Gupta and Bodhisattwa Prasad Majumder and Katherine Hermann and Sean Welleck and Amir Yazdanbakhsh and Peter Clark (2023).
Self-Refine: Iterative Refinement with Self-Feedback

<a id=2>[2]</a>
Saravia, Elvis (2022).
Prompt Engineering Guide
