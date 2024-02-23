import subprocess
import os

def run_script_within_venv(script_path):
    """
    Run a script within the activated virtual environment.
    """
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'env')
    python_executable = os.path.join(env_path, 'bin', 'python')
    try:
        subprocess.check_call([python_executable, script_path])
        print("Script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")

# Example usage:
if __name__ == "__main__":
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
    run_script_within_venv(script_path)























