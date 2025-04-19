# Pokemon Detection CNN - Pokedex UI

This project provides a Pokedex application with a modern graphical user interface (GUI) built using CustomTkinter. It displays detailed information about Pokemon, including stats, types, images, and Pokedex entries, sourced from a CSV dataset.

![image](https://github.com/user-attachments/assets/def1167e-20ba-4dc2-93c9-e0ea8926d485)
![image](https://github.com/user-attachments/assets/590d28a6-7dcc-4c54-8347-34e3114cd2f9)
![image](https://github.com/user-attachments/assets/86bf9837-556b-4c04-8aa0-0dfdeb194a71)

## Features

- Search and browse Pokemon by name with autocomplete.
- View Pokemon images and type icons.
- Display key stats with color-coded bars.
- Show Pokedex entries, height, weight, and catch rate.
- Modern, dark-themed UI using CustomTkinter for an enhanced user experience.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/pokemon_detection_cnn.git
cd pokemon_detection_cnn
```

2. Create and activate a Python virtual environment (optional but recommended):

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the modern Pokedex UI application:

```bash
python modelv3_customtkinter.py
```

This will launch the Pokedex window where you can search for Pokemon, navigate through them, and view detailed information.

## File Structure

- `modelv3_customtkinter.py`: Main application with CustomTkinter UI.
- `pokedata.csv`: Dataset containing Pokemon information.
- `Pokemon Pictures/`: Folder containing Pokemon images.
- `Type Pictures/`: Folder containing type icons.
- `requirements.txt`: Python dependencies.

## Dependencies

- Python 3.7+
- pandas
- numpy
- Pillow
- customtkinter

## Notes

- Ensure the `Pokemon Pictures` and `Type Pictures` directories contain the appropriate images for the application to display.
- The UI is designed for a 1200x700 window but is resizable.

## License

This project is licensed under the MIT License.

## Author

Your Name - [GitHub Profile](https://github.com/yourusername)
