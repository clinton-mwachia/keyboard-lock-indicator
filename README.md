# LockIndicator

LockIndicator is a simple utility application that provides visual indicators for Caps Lock and Num Lock states on your Windows system. The application features customizable themes and includes a settings panel for personalization.

## Motivation

I developed LockIndicator because my laptop does not have a built-in way to visually indicate when Caps Lock and Num Lock are active. This often leads to inadvertent typing errors and a lack of clarity on the current state of these keys. This application was created to address this gap and provide a clear, customizable visual indicator for these important keyboard states.

## Features

- **Caps Lock and Num Lock Indicators**: Shows the current status of Caps Lock and Num Lock with on-screen labels.
- **Notification**: Display lock states change.
- **Customizable Themes**: Allows users to choose from predefined themes (Light, Dark, Blue).
- **Settings Panel**: Provides options to change themes and configure auto-start behavior.
- **Window Management**: Supports minimize, maximize, and close functionalities.
- **Drag and Drop**: Allows moving the window around the screen.

## Installation

1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/clinton-mwachia/keyboard-lock-indicator.git
   ```

2. **Install Dependencies**:
   Ensure you have Python installed. Install the required packages using pip:
   ```bash
   pip install pynput
   ```

## Packaging with PyInstaller

To package the application into a standalone executable using PyInstaller:

1. **Install PyInstaller**:
   Install PyInstaller using pip:
   ```bash
   pip install pyinstaller
   ```

2. **Create the Executable**:
   Navigate to the project directory and run PyInstaller to generate the executable:
   ```bash
   pyinstaller --onefile --noconsole app.py
   ```

   - `--onefile`: Packages everything into a single executable file.
   - `--noconsole`: Hides the console window (useful for GUI applications).

3. **Locate the Executable**:
   After running PyInstaller, the executable will be located in the `dist` directory within your project folder.

## Usage

1. **Run the Application**:
   - If you’re using the Python script, navigate to the project directory and run:
     ```bash
     python app.py
     ```
   - If you’ve created an executable with PyInstaller, simply run the generated `.exe` file from the `dist` directory.

2. **Interacting with the Application**:
   - **Settings Button**: Click the "Settings" button to open the settings panel where you can choose themes and toggle auto-start.
   - **Window Controls**: Use the minimize, maximize, and close buttons to manage the window.

## Configuration

- **Themes**: Change the theme via the settings panel. Available options are Light, Dark, and Blue.
- **Auto-Start**: Enable or disable auto-start with Windows from the settings panel.

## Notes

- Window positions are saved and restored automatically upon restart.

## Troubleshooting

- **Window Minimization Issue**: If the window does not minimize or maximize properly, ensure you are not using any additional window management tools that might interfere.
- **Executable Issues**: If the executable fails to run, ensure all dependencies are included and verify if there are any missing files in the `dist` directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Contact

For any questions or feedback, please contact [clintonmwachia9@gmail.com](mailto:clintonmwachia9@gmail.com).
