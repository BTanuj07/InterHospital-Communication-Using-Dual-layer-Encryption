import os
import sys
import subprocess


def main():
    """Start the Streamlit app (`app.py`) using the current Python environment.

    This uses `python -m streamlit run app.py ...` which is more reliable than
    calling a platform-specific `streamlit` executable.
    """
    app_file = "app.py"
    if not os.path.exists(app_file):
        print(f"Error: '{app_file}' not found in {os.getcwd()}")
        return 1

    cmd = [sys.executable, "-m", "streamlit", "run", app_file,
           "--server.address", "0.0.0.0",
           "--server.port", "8501",
           "--server.enableCORS", "false"]

    print("Starting Streamlit app with command:")
    print(" ".join(cmd))

    try:
        # Run Streamlit in the foreground so logs appear in this terminal
        return subprocess.call(cmd)
    except FileNotFoundError:
        print("Streamlit is not installed in this Python environment.")
        print(f"Install it with: {sys.executable} -m pip install streamlit")
        return 2


if __name__ == "__main__":
    sys.exit(main())
