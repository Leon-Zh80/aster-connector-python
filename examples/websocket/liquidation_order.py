#!/usr/bin/env python3

import time
import logging
from typing import Callable, Any
# Assuming 'aster' is a library for a specific exchange/protocol
from aster.lib.utils import config_logging
from aster.websocket.client.stream import WebsocketClient as Client

# Define the log level for the script. DEBUG is verbose, suitable for development.
LOG_LEVEL = logging.DEBUG

def setup_logging():
    """Configures the logging system for the application."""
    # NOTE: The original config_logging signature (logging, logging.DEBUG) suggests
    # the utility might expect the logging module itself. We maintain the original call 
    # but use the constant LOG_LEVEL for clarity.
    config_logging(logging, LOG_LEVEL)

def message_handler(message: Any) -> None:
    """
    Callback function executed when a message (e.g., liquidation order) is received.
    For production, this would contain logic to process the data, not just print it.
    """
    # Assuming the message is already deserialized (e.g., dict or JSON object)
    print(f"WS MESSAGE RECEIVED: {message}")

def main():
    """
    Initializes the WebSocket client, starts the connection, subscribes, 
    and manages the connection lifecycle.
    """
    # Configure logging before client initiation
    setup_logging()

    # Instantiate the WebSocket client
    my_client = Client()

    try:
        logging.info("Starting WebSocket client connection...")
        # Start the client thread/process
        my_client.start()
        
        # Subscribe to the liquidation order stream
        logging.info("Subscribing to liquidation_order stream (ID: 13)...")
        my_client.liquidation_order(
            id=13,
            callback=message_handler,
        )

        # HACK: Use sleep to keep the main thread alive while the WS thread runs.
        # In a real application, consider using `asyncio` or a proper signaling 
        # mechanism (like threading.Event) to wait indefinitely or until a condition is met.
        logging.info("Connection running. Waiting for 5 seconds to receive messages...")
        time.sleep(5) 
        
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
    
    finally:
        # Gracefully stop the client connection
        logging.info("Stopping WebSocket client connection.")
        my_client.stop()
        logging.info("Client stopped. Program exiting.")

if __name__ == '__main__':
    main()
