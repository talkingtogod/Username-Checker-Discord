# Discord Username Checker

A modern, asynchronous Discord username availability checker with JSON configuration and advanced features.

## Description

Discord Username Checker is a Python application that validates the availability of Discord usernames using Discord's API. It features an async implementation for improved performance, JSON-based configuration, multi-token support, webhook notifications, and a visually enhanced CLI interface.

## Features

- **Asynchronous Processing**: Built with asyncio and aiohttp for fast, concurrent requests
- **Multiple Operation Modes**: Generate random usernames or check from file
- **Multi-Token Support**: Rotate between multiple tokens to avoid rate limits
- **Webhook Notifications**: Get real-time notifications when available usernames are found
- **JSON Configuration**: Modern configuration management with interactive setup
- **Visual Interface**: ASCII art, progress bars, and colored output
- **Flexible Character Sets**: Configure letters, numbers, and symbols independently
- **Rate Limit Handling**: Intelligent rate limit management and token rotation
- **Result Management**: Automatic saving of available usernames to file

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Dependencies

Install the required packages:

```bash
pip install aiohttp aiofiles colorama
```

### Clone Repository

```bash
git clone https://github.com/yourusername/discord-username-checker.git
cd discord-username-checker
```

## Configuration

On first run, the application will guide you through an interactive configuration setup:

### Configuration Options

- **Discord Token**: Your Discord account token (required)
- **Request Delay**: Delay between API requests in seconds (default: 1.0)
- **Character Sets**: Enable/disable letters, numbers, and symbols
- **Webhook URL**: Optional Discord webhook for notifications
- **Multi-Token Mode**: Enable token rotation for rate limit avoidance

### Configuration File

The application creates a `config.json` file with the following structure:

```json
{
  "discord_token": "your_token_here",
  "request_delay": 1.0,
  "enable_letters": true,
  "enable_numbers": true,
  "enable_symbols": false,
  "webhook_url": "",
  "multi_token_mode": false
}
```

### Multi-Token Setup

For multi-token mode, create a `tokens.txt` file with one token per line:

```
token1_here
token2_here
token3_here
```

## Usage

### Running the Application

```bash
python discord_checker.py
```

### Menu Options

1. **Generate and check random usernames**: Creates random usernames and checks availability
2. **Check usernames from file**: Validates usernames from `usernames.txt`
3. **Show current configuration**: Displays current settings
4. **Reconfigure settings**: Update configuration interactively
5. **Exit application**: Close the program

### Generate Mode

When using generate mode, you'll be prompted for:
- Username length (2-32 characters)
- Number of usernames to generate

### File Mode

Create a `usernames.txt` file with one username per line:

```
username1
username2
username3
```

## File Structure

```
discord-username-checker/
├── discord_checker.py          # Main application file
├── config.json                 # Configuration file (created on first run)
├── tokens.txt                  # Multi-token file (optional)
├── usernames.txt              # Input file for file mode (optional)
├── available_usernames.txt    # Output file for available usernames
└── README.md                  # This file
```

## Output

### Available Usernames

All available usernames are saved to `available_usernames.txt` with timestamps.

### Console Output

The application provides real-time feedback including:
- Connection status and current user information
- Progress bars during checking
- Colored status messages
- Rate limit handling notifications
- Final statistics and results

### Webhook Notifications

When configured, webhooks send Discord embeds containing:
- Available username
- Timestamp
- Application branding

## Error Handling

The application handles various error scenarios:
- Invalid or expired Discord tokens
- Network connectivity issues
- Rate limiting with automatic retry
- File access permissions
- Invalid configuration values

## Rate Limiting

Discord API rate limits are handled through:
- Automatic retry with exponential backoff
- Token rotation in multi-token mode
- Configurable request delays
- Real-time rate limit status updates

## Security Considerations

- **Token Security**: Keep your Discord tokens secure and never share them
- **Rate Limits**: Respect Discord's API rate limits to avoid account restrictions
- **Terms of Service**: Ensure compliance with Discord's Terms of Service
- **Responsible Usage**: Use the tool responsibly and ethically

## API Endpoints

The application uses the following Discord API endpoints:
- `GET /users/@me` - User information retrieval
- `POST /users/@me/pomelo-attempt` - Username availability checking

## Troubleshooting

### Common Issues

**Invalid Token Error**
- Verify your Discord token is correct and hasn't expired
- Ensure the token has necessary permissions

**Rate Limiting**
- Increase request delay in configuration
- Consider using multi-token mode
- Check if your IP is temporarily restricted

**File Not Found**
- Ensure `usernames.txt` exists for file mode
- Check file permissions and directory access

**Configuration Issues**
- Delete `config.json` to trigger reconfiguration
- Verify JSON syntax if manually editing configuration

## Performance

### Optimization Features

- Asynchronous HTTP requests for concurrent processing
- Efficient memory usage with generators
- Minimal API calls through intelligent caching
- Progress tracking without performance impact

### Benchmarks

Typical performance on modern hardware:
- Single token: 60-120 checks per minute
- Multi-token: 200-500 checks per minute (depends on token count)
- Memory usage: < 50MB during normal operation

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make your changes
5. Test thoroughly
6. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Document functions and classes
- Maintain async/await patterns

### Reporting Issues

When reporting bugs, include:
- Python version
- Operating system
- Error messages and stack traces
- Steps to reproduce
- Configuration details (without sensitive data)

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer

This tool is for educational and legitimate purposes only. Users are responsible for:
- Complying with Discord's Terms of Service
- Respecting API rate limits
- Using the tool ethically and legally
- Securing their authentication tokens

The developers are not responsible for any misuse of this software or consequences resulting from its use.

## Version History

### v2.0
- Complete rewrite with async implementation
- JSON configuration system
- Enhanced visual interface
- Multi-token support
- Webhook notifications
- Improved error handling

### v1.x
- Initial release
- Basic username checking
- INI configuration
- Single-token operation

## Support

For support, issues, or feature requests:
- Open an issue on GitHub
- Check existing issues for similar problems
- Provide detailed information when reporting bugs

## Acknowledgments

- Discord API documentation and community
- Python async/await ecosystem
- Colorama library for cross-platform colored output
- aiohttp and aiofiles for async operations
