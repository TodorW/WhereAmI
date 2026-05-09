# 🔍 WhereAmI - Digital Footprint Analyzer

*"Because sometimes you forget where you've been on the internet"*

## 📖 Overview

**WhereAmI** is a powerful Python-based OSINT (Open Source Intelligence) tool designed for educational and security research purposes. It helps you discover which online services and platforms have accounts associated with your email address, giving you visibility into your digital footprint across the web.

## ⚠️ Disclaimer

**THIS TOOL IS FOR EDUCATIONAL AND PERSONAL SECURITY AUDITING PURPOSES ONLY**

- ✅ **Allowed**: Checking your own email addresses
- ✅ **Allowed**: Security research with proper authorization
- ✅ **Allowed**: Learning about web scraping and API integration
- ❌ **Not Allowed**: Checking others' emails without permission
- ❌ **Not Allowed**: Malicious or harassing activities
- ❌ **Not Allowed**: Violating websites' terms of service

By using this tool, you agree to use it responsibly and legally.

## 🚀 Features

- **🔍 100+ Site Coverage**: Checks accounts across social media, professional networks, gaming platforms, and more
- **📊 Categorized Results**: Organized output by platform type (Social Media, Professional, Gaming, etc.)
- **⚡ Smart Detection**: Uses multiple HTTP methods and status code analysis
- **🎯 Progress Tracking**: Real-time progress with site count and status
- **📈 Summary Report**: Comprehensive results breakdown at completion
- **🛡️ Rate Limiting**: Built-in delays to respect server resources
- **❌ Error Handling**: Robust error management with descriptive status codes

## 📦 Installation

### Prerequisites
- Python 3.6+
- pip package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/TodorW/WhereAmI.git
cd WhereAmI

# Install dependencies
pip install -r requirements.txt
```

### Dependencies
The `requirements.txt` contains:
```txt
requests>=2.25.1
```

## 🎯 Usage

### Basic Usage
```bash
python whereami.py
```

### Interactive Mode
1. Run the script
2. Enter your email when prompted
3. Watch real-time progress across 100+ sites
4. Review the comprehensive summary report

### Example Output
```
🔍 Checking: example@email.com
========================================

🔐 Social Media
----------------------------------------
[1/100] Facebook                    ✓ Possible account exists
[2/100] Twitter/X                   ✗ No account found
[3/100] Instagram                   ? Status: 302

📊 SUMMARY
========================================
✅ Possible accounts: 15
❓ Uncertain: 23  
❌ Failed checks: 62
📧 Total sites checked: 100
```

## 🏗️ Architecture

### Core Components
- **Site Database**: Curated list of 100+ popular websites
- **HTTP Engine**: Intelligent request handling with proper headers
- **Analysis Module**: Status code interpretation and pattern matching
- **Reporting System**: Categorized results with summary statistics

### Detection Methods
- **HTTP Status Codes**: 200 (exists), 404 (not found), others (uncertain)
- **Response Analysis**: Redirect patterns and error pages
- **Rate Limiting**: 300ms delays between requests
- **Error Resilience**: Timeout and connection error handling

## 📋 Supported Platforms

### Categories Include:
- **Social Media** (Facebook, Twitter, Instagram, LinkedIn, etc.)
- **Professional** (GitHub, StackOverflow, Behance, etc.)
- **Gaming** (Steam, Epic Games, Xbox, PlayStation, etc.)
- **E-commerce** (Amazon, eBay, Etsy, etc.)
- **Streaming** (YouTube, Twitch, Netflix, Spotify, etc.)
- **Finance** (PayPal, Venmo, Robinhood, etc.)
- **Development** (npm, Docker Hub, PyPI, etc.)
- **And many more...**

## 🔧 Technical Details

### HTTP Methods
- **GET Requests**: Primary detection method
- **HEAD Requests**: Alternative for some sites
- **Custom Headers**: Realistic User-Agent strings
- **Timeout Handling**: 8-second request timeouts

### Status Interpretation
- **✓ Possible account exists** (200 status)
- **✗ No account found** (404 status)  
- **? Status: XXX** (Other HTTP status codes)
- **⏰ Timeout** (Request timed out)
- **🔌 Connection failed** (Network issues)
- **❌ Request failed** (General failure)

## 🛡️ Privacy & Security

### Data Handling
- Your email is never stored or transmitted to our servers
- All checks happen locally on your machine
- No persistent logging of results
- Temporary memory-only processing

### Ethical Considerations
- Built for personal security auditing
- Encourages digital footprint awareness
- Promotes account cleanup and security hygiene
- Educational tool for cybersecurity students

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Adding New Sites
1. Fork the repository
2. Add site to the appropriate category in `sites` dictionary
3. Test the detection method
4. Submit a pull request

### Categories Needed:
- Regional platforms (country-specific sites)
- Niche community forums
- Emerging social platforms
- Specialized professional networks

### Reporting Issues
- Create GitHub issues for bug reports
- Suggest new features or improvements
- Share your testing results

## 📊 Real-World Applications

### Personal Use
- **Digital Spring Cleaning**: Identify old accounts to delete
- **Security Auditing**: Discover potential breach exposure
- **Account Recovery**: Find forgotten service registrations

### Educational Use
- **Cybersecurity Courses**: OSINT methodology demonstration
- **Web Scraping Lessons**: HTTP request/response analysis
- **Privacy Workshops**: Digital footprint awareness

### Professional Use
- **Security Research**: Account enumeration studies
- **Penetration Testing**: Authorized client assessments
- **Digital Forensics**: Incident response investigations

## 🚨 Limitations & Accuracy

### Technical Limitations
- Many sites block automated requests
- Rate limiting may cause false negatives
- CAPTCHA-protected sites cannot be checked
- Private profiles may not be detectable

### Accuracy Notes
- **False Positives**: Possible due to similar usernames
- **False Negatives**: Common with anti-bot measures
- **Estimated Accuracy**: ~40-60% for detectable sites
- **Results are indicative, not definitive**

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Inspired by OSINT community tools
- Built for educational purposes
- Thanks to all contributors and testers

---

**Remember**: With great power comes great responsibility. Use WhereAmI to improve your digital hygiene, not to invade others' privacy.

**⭐ If you find this useful, please give it a star on GitHub!**