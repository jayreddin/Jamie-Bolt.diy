import subprocess

def take_screenshot(output_file):
    try:
        subprocess.run(['mate-screenshot', '--file', output_file], check=True)
        print(f"Screenshot saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to take screenshot: {e}")


if __name__ == "__main__":
    take_screenshot()
