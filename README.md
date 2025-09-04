# mouth-peace
In-game chat assistant


# Getting Started

This script performs voice recognition on local hardware using CUDA and works if you have good Nvidia GPU.

If you would like a version without relying on good hardware, please raise an issue or agree to an existing one.

Note: You might still need to set up an account for speech recognition API services and pay for it.

1. Install torch for CUDA: run nvidia-smi and record CUDA Version
2. Go to [text](https://pytorch.org/get-started/locally/). For "Compute Platform", choose your CUDA version.
3. Run the command in your python environment to install torch.

1. If you haven't already, register for an OpenAI platform account so you can call OpenAI APIs. Alternatively, Use your own provide.
2. Create a .env and enter your OpenAI API key following .env.example
