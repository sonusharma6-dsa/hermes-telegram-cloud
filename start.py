import os
import sys
from hermes_cli.gateway import run_gateway

if __name__ == "__main__":
    print("Starting Hermes Gateway on Render Cloud...")
    run_gateway(verbose=1, quiet=False, replace=True, force=True)
