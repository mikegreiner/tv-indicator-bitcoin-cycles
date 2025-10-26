# Bitcoin Cycles Indicator

A TradingView indicator that tracks Bitcoin cycles across multiple timeframes, providing visual cycle analysis with dynamic labeling and comprehensive information display.

**🔗 TradingView Script**: [https://www.tradingview.com/script/1fHosDT9-Bitcoin-Cycles-Indicator/](https://www.tradingview.com/script/1fHosDT9-Bitcoin-Cycles-Indicator/)

## Overview

The Bitcoin Cycles Indicator is designed to identify and track cyclical patterns in Bitcoin price movements across Daily, Weekly, Monthly, and Custom timeframes. It provides real-time cycle analysis with visual labels, projection boxes, and detailed information displays to help traders understand market cycles and potential turning points.

### Key Features

- **Multi-Timeframe Support**: Optimized settings for Daily, Weekly, Monthly, and Custom timeframes
- **Dynamic Cycle Detection**: Automatically detects cycle lows and highs within configurable ranges
- **Visual Indicators**: Color-coded labels for potential and final cycle points
- **Failed Cycle Detection**: Identifies when cycles break down (lower lows)
- **Dynamic Projection Boxes**: Visual estimates of cycle end ranges using average cycle length
- **Comprehensive Info Box**: Real-time cycle information with theme-aware display
- **Strategy Integration**: Exposes cycle data for use in TradingView strategies

## Repository Structure

```
tv-indicator-bitcoin-cycles/
├── bitcoin-cycles-indicator.pine    # Main TradingView indicator script
├── docs/                            # Documentation and guides
│   ├── bitcoin-cycles-improvements.md
│   ├── bitcoin-cycles-manual-testing-guide.md
│   ├── bitcoin-cycles-testing-guide.md
│   ├── development-speed-guide.md
│   ├── README-testing.md
│   └── testing-checklist.md
├── tests/                           # Testing framework and validation
│   ├── bitcoin-cycles-test-framework.pine
│   ├── bitcoin-cycles-validation-strategy.pine
│   └── bitcoin-cycles-visual-verification.pine
├── tools/                           # Development and validation tools
│   ├── cycle-logic-validator.py
│   ├── dev-workflow.sh
│   ├── pine-syntax-checker.py
│   └── test-runner.sh
├── LICENSE                          # MIT License
└── README.md                        # This file
```

## Quick Start

1. **Installation**: Copy the `bitcoin-cycles-indicator.pine` script to TradingView
2. **Configuration**: Adjust cycle length settings for your preferred timeframe
3. **Analysis**: Watch for cycle labels and use the info box for detailed information

### Default Settings by Timeframe

| Timeframe | Min Cycle | Max Cycle | Notes |
|-----------|-----------|-----------|-------|
| Daily     | 40 days   | 70 days   | Most commonly used |
| Weekly    | 5 weeks   | 13 weeks  | Medium-term analysis |
| Monthly   | 40 months | 54 months | Long-term cycles |
| Custom    | 40 bars   | 70 bars   | User-defined timeframe |

## Usage

### Basic Operation

1. **Load the Indicator**: Add to any Bitcoin chart
2. **Select Timeframe**: Choose Daily, Weekly, or Monthly
3. **Configure Settings**: Adjust cycle lengths if needed
4. **Monitor Cycles**: Watch for potential and final cycle labels

### Understanding the Labels

- **🟢 Final Low**: Confirmed cycle low (green label)
- **🔴 Final High**: Confirmed cycle high (red label)  
- **🟠 Potential Low**: Current cycle low candidate (orange label)
- **🟣 Potential High**: Current cycle high candidate (purple label)
- **⚪ Current Day**: Cycle progress counter (gray label)

### Failed Cycle Detection

The indicator automatically detects failed cycles when the current cycle low falls below the previous cycle low, displaying a "Failed Cycle" warning.

### Dynamic Projection Boxes

The indicator now uses adaptive projection boxes that:
- **Track Average Cycle Length**: Calculates the average length of completed cycles
- **Dynamic Labels**: Show actual projection length (e.g., "13W End" instead of hardcoded values)
- **Improved Visibility**: Minimum box widths ensure proper visibility across all timeframes
- **Real-time Updates**: Projection boxes adjust as more cycles complete

## Development

### Testing Framework

The repository includes a comprehensive testing suite:

- **Test Framework**: Generates synthetic data for algorithm validation
- **Validation Strategy**: Strategy-based testing and validation
- **Visual Verification**: Manual testing tools and checklists

### Development Tools

- **Syntax Checker**: Validates Pine Script syntax
- **Cycle Validator**: Python tool for cycle logic validation
- **Test Runner**: Automated testing workflow
- **Dev Workflow**: Streamlined development process

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly using the provided testing framework
5. Submit a pull request

## Documentation

- **[Testing Guide](docs/bitcoin-cycles-testing-guide.md)**: Comprehensive testing procedures
- **[Improvements](docs/bitcoin-cycles-improvements.md)**: Planned enhancements and optimizations
- **[Manual Testing](docs/bitcoin-cycles-manual-testing-guide.md)**: Step-by-step manual testing
- **[Development Guide](docs/development-speed-guide.md)**: Development workflow and best practices

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Support

For questions, issues, or contributions:

1. Check the [TradingView script page](https://www.tradingview.com/script/1fHosDT9-Bitcoin-Cycles-Indicator/) for user discussions
2. Review the documentation in the `docs/` folder
3. Use the testing framework to validate behavior
4. Open an issue for bugs or feature requests

## Disclaimer

This indicator is for educational and analysis purposes only. It should not be considered as financial advice. Always conduct your own research and consider your risk tolerance before making trading decisions.

---

**Author**: dirtpupfc  
**Version**: 1.3  
**Last Updated**: 2025-01-27
