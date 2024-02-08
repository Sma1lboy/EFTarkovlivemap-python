# EFTarkovLiveMap-python

## Overview

`EFTarkovLiveMap-python` is an innovative tool designed for the gaming community of Escape From Tarkov (EFT). This Python-based project offers a dynamic live map feature that enhances players' situational awareness and strategic planning capabilities. With the latest addition of the modem UI, users can now experience an even more immersive and interactive map navigation.

## Features

- **Live Map Display**: Real-time updates of in-game events and locations.
- **Modem UI**: A newly introduced user interface that simulates a modem's functionality, adding to the immersive experience of the game.
- **Configurable Auto-refresh**: Ability to toggle auto-refresh feature for the live map through `config.json`, with default set to `false`.
- **Easy Setup**: Simple installation and setup process, powered by `pipenv`.

## Installation

1. **Clone the Repository**

```bash
git clone https://github.com/Sma1lboy/EFTarkovlivemap-python.git
```

1. **Install Dependencies**

Make sure you have `pipenv` installed. If not, install it via pip:

```bash
pip install pipenv
```

Then, navigate to the project directory and install the required packages:

```bash
cd EFTarkovlivemap-python
pipenv install
```

## Configuration

Edit the `config.json` file to set your preferences for the live map refresh rate and other settings. By default, `isAutoRefresh` is set to `false`.

```json
{
  "isAutoRefresh": false
}
```

## Usage

To launch the live map with the modem UI:

- Download the release or build by youself



## Contributing

We welcome contributions from the community! If you have suggestions, bug reports, or contributions, please submit them via GitHub issues or pull requests.

## License

This project is open-sourced under the MIT License. See the LICENSE file for more details.

## Acknowledgments

Thanks to all contributors and the Escape From Tarkov community for their feedback and support.