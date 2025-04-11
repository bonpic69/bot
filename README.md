# Binance Futures Trading Bot

## Overview

The Binance Futures Trading Bot is a sophisticated Python-based application designed to automate trading on the Binance Futures platform. By integrating with the Binance API and Telegram for real-time signal processing, the bot executes trades based on predefined trading signals, manages positions, and implements risk management strategies such as stop-loss and take-profit orders. The bot is highly configurable, allowing users to customize leverage, position size, and other trading parameters through a configuration file.

## Features

- **Automated Trading**: Executes trades based on signals received via Telegram, supporting both long and short positions.
- **Binance Futures Integration**: Interacts with the Binance Futures API to manage positions, set leverage, and place orders.
- **Real-Time Signal Processing**: Monitors Telegram channels for trading signals and decodes them to extract critical information (e.g., symbol, entry/exit points, leverage).
- **Risk Management**:
  - Configurable stop-loss and take-profit levels.
  - Support for trailing stop-loss orders.
  - Moon bag strategy (optional retention of a portion of the position for potential further gains).
- **Position Synchronization**: Continuously monitors open positions and updates stop-loss/take-profit orders as needed.
- **Precision Handling**: Adjusts order quantities and prices to comply with Binance’s symbol-specific precision requirements.
- **Logging**: Records all trades, orders, and signals to text files for auditing and analysis.
- **Error Handling**: Robust error detection and logging to ensure reliable operation.

## Requirements

- **Python Version**: Python 3.8 or higher
- **Dependencies**:
  - `requests`
  - `pyfiglet`
  - `colorama`
  - `telethon`
  - Ensure all dependencies are installed using:
    ```bash
    pip install -r requirements.txt
    ```
- **Binance API Keys**: Obtain API keys from Binance with permissions for futures trading.
- **Telegram API Credentials**: Obtain API ID and hash from Telegram’s API development tools.
- **Configuration File**: A `config.ini` file with the required settings (see Configuration section).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/binance-futures-bot.git
   cd binance-futures-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Configuration**:
   Create a `config.ini` file in the project root with the following structure:
   ```ini
   [API]
   rgb_id = <Telegram API ID>
   rgb_id_app = <Telegram API Hash>
   rgb_id_cht = <Telegram Chat ID for Signals>
   bg_id = <Binance API Key>
   bg_id_k = <Binance API Secret>
   bs_pi = https://fapi.binance.com
   moon_bag = True
   pos_sz = 10
   sl_prc = 10
   lev = 10
   trailing_sl = True
   ```
   Replace placeholders with your credentials and preferences.

4. **Run the Bot**:
   ```bash
   python main.py
   ```

## Configuration

The bot’s behavior is controlled via the `config.ini` file. Key parameters include:

- **rgb_id**: Telegram API ID for connecting to the Telegram client.
- **rgb_id_app**: Telegram API hash.
- **rgb_id_cht**: Telegram chat ID where trading signals are received.
- **bg_id**: Binance API key.
- **bg_id_k**: Binance API secret key.
- **bs_pi**: Binance Futures API base URL (default: `https://fapi.binance.com`).
- **moon_bag**: Boolean (`True`/`False`) to enable/disable the moon bag strategy.
- **pos_sz**: Percentage of account balance to use per trade (e.g., `10` for 10%).
- **sl_prc**: Stop-loss percentage (e.g., `10` for 1% after scaling).
- **lev**: Leverage to apply to trades (e.g., `10` for 10x).
- **trailing_sl**: Boolean (`True`/`False`) to enable/disable trailing stop-loss.

## Usage

1. **Start the Bot**:
   Run the script to initialize the bot:
   ```bash
   python main.py
   ```
   The bot will connect to Binance, check the account balance, and start monitoring the specified Telegram channel for signals.

2. **Signal Format**:
   The bot expects Telegram messages with a specific structure, including:
   - Symbol (e.g., `BTCUSDT`)
   - Exchange (e.g., `Binance Futures`)
   - Trade type (e.g., `Long` or `Short`)
   - Leverage (e.g., `10x`)
   - Entry targets
   - Take-profit targets
   - Stop-loss targets

3. **Monitoring**:
   The bot logs all activities, including:
   - Decoded signals (`decoded_messages.txt`)
   - Placed orders and positions (`positions_and_orders.txt`)
   - Position updates (`positions.json`)

4. **Stopping the Bot**:
   Stop the bot gracefully using `Ctrl+C`. Ensure all open positions are monitored manually if the bot is stopped.

## Code Structure

- **Main Script** (`main.py`):
  - Initializes the bot, loads configuration, and starts the Telegram client and position synchronization.
- **Key Functions**:
  - `get_config_object()`: Loads and validates the configuration.
  - `place_position_and_orders_futures()`: Executes trades and sets stop-loss/take-profit orders.
  - `decode_message_pattern()`: Parses Telegram signals into actionable trade data.
  - `sync_positions()`: Monitors and updates open positions.
  - `send_signed_request()`: Handles authenticated API requests to Binance.
- **Utilities**:
  - Precision handling for order quantities and prices.
  - Logging and error reporting.
  - Thread-safe position management using `RLock`.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to your fork:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request with a detailed description of your changes.

Please ensure your code follows the existing style and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

Trading cryptocurrencies involves significant risk and can result in the loss of your capital. This bot is provided as-is, and users are responsible for configuring it correctly and monitoring its operation. Always test the bot in a demo environment before using it with real funds.
