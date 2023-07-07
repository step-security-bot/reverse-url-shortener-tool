# Reverse URL Shortener Tool

This Python script is designed to find available short URLs using multiple domains. It generates random alphanumeric paths and checks if the formed short URL is available. It also generates variations of the path by replacing each character with a different one and checks their availability as well.

> Do you use URL shorteners? If so, you are at risk!

## Installation

1. Clone the repository:
```shell
git clone https://github.com/meyer-pidiache/Reverse_URL_Shortener
```
2. Navigate to the project directory:
```shell
cd Reverse_URL_Shortener
```

## Usage

1. Open the `old_main.py` file in a text editor.

2. Configure the `SHORTURL_DOMAINS` dictionary with the desired short URL domains and their corresponding path lengths. Uncomment the domains you want to use for searching short URLs.

4. Run the script:
```shell
python ./old_main.py
```

5. The script will search for available short URLs and print any found URLs to the console.

6. To stop the script, press `Ctrl+C`.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
