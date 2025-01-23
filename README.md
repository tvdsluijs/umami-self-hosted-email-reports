# 📊 Umami Self-Hosted Email Reports

## 🌟 Overview

A Python script for generating and sending analytics reports from self-hosted Umami installations.
While Umami's Pro version includes email reporting, this script provides similar functionality for free.
Perfect for users who want automated analytics reports from their self-hosted Umami instance.

Key benefits:
- 🆓 Free alternative to Umami Pro email reports
- 📧 Automated email delivery of analytics data
- 🎨 Customizable report styling
- 🌍 Multi-language support
- ⚙️ Flexible configuration options

![Email Report](email_report.jpg)

## 🎯 Features

- **📊 Comprehensive Analytics**
  - Views, visits, visitors statistics
  - Bounce rates and session durations
  - URL performance tracking
  - Referrer analysis
  - Browser and OS statistics
  - Device usage metrics
  - Geographic data

- **⚙️ Flexible Reporting**
  - Daily reports
  - Weekly summaries
  - Monthly overviews
  - Quarterly analysis
  - Yearly reports

- **🎨 Customization Options**
  - Custom email templates
  - CSS styling support
  - Configurable metrics
  - Multiple recipient support

## 🛠️ Prerequisites

### System Requirements
- Python 3.8 or higher
- SMTP server access
- Self-hosted Umami installation

### Required Python Packages
- requests
- jinja2
- weasyprint
- python-dateutil

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone git@github.com:tvdsluijs/umami-self-hosted-email-reports.git
   cd umami-email-reports
   ```

2. **Install Dependencies**

   Using pixi:
   ```bash
   pixi run report
   ```

   Using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Settings**
   - Copy and modify `config.json.example` to `config.json`
   - Copy and modify `websites_config.json.example` to `websites_config.json`

## ⚙️ Configuration

### config.json
```json
{
    "umami": {
        "api_url": "https://your-umami-url/api/websites",
        "username": "your-username",
        "password": "your-password"
    },
    "company": {
        "name": "Your Company",
        "url": "https://example.com",
        "email": "info@example.com",
        "logo": "https://your-logo-url.jpg"
    },
    "smtp": {
        "host": "smtp.example.com",
        "port": 587,
        "username": "your-email@example.com",
        "password": "your-password",
        "from_email": "your-email@example.com",
        "from_name": "Analytics Report"
    }
}
```

### websites_config.json
```json
[
    {
        "website_id": "website-id-1",
        "name": "website 1 name",
        "frequency": "week",
        "lang": "en",
        "send_day": [],
        "top": 5,
        "emails": ["recipient1@example.com", "recipient2@example.com"],
        "what_stats": ["stats", "event", "url", "referrer", "browser", "os", "device", "country"],
        "email_template": "email_template.html",
        "email_time": "08:00",
        "send_login_url": "https://url.to.your.umami.com",
        "send_pdf": true
    },
]
```

## 🌍 Supported Languages

Currently supports 25+ languages including:
- English (en)
- Dutch (nl)
- German (de)
- French (fr)
- Spanish (es)
- Italian (it)
- Portuguese (pt)
- And many more!

See the `locale` directory for all available languages.

### 🔍 Language Note
While Dutch, English, and German translations are manually verified, other languages use AI-assisted translations. Contributions for improving translations are welcome!

## 🚀 Usage

### Running the Script
Using pixi:
```bash
pixi run report
```

Using Python directly:
```bash
python umami_report.py
```

### Cron Job Setup
For automated daily execution at 7 AM:

Using pixi:
```bash
0 7 * * * cd /path/to/project && pixi run report
```

Using Python:
```bash
0 7 * * * /path/to/python /path/to/project/umami_report.py
```

## 🔧 Troubleshooting

Common issues and solutions:
1. **Authentication Failures**
   - Verify Umami credentials in config.json
   - Check API URL accessibility

2. **SMTP Errors**
   - Confirm SMTP server settings
   - Verify email credentials
   - Check firewall settings

3. **Missing Reports**
   - Validate website IDs
   - Check scheduling configuration
   - Verify email addresses

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 👥 Author

**Theo van der Sluijs**
- [GitHub](https://github.com/tvdsluijs)
- [Email](mailto:theo@vandersluijs.nl)
- [Website](https://itheo.tech)

## 💝 Support the Project

If you find this tool useful, consider supporting its development:
- [GitHub Sponsors](https://github.com/sponsors/tvdsluijs)
- [Buy Me a Coffee](https://buymeacoffee.com/itheo)

Your support helps maintain and improve this project! 🙏
