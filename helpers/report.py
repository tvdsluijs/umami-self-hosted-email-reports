from email.mime.text import MIMEText

def generate_table(title_col, value_col, data):
    """Generate an HTML table dynamically from provided data."""
    if not data:
        return ""  # Return empty string if no data is available
    rows = "".join([f"<tr><td>{item['label']}</td><td>{item['value']}</td></tr>" for item in data[:10]])
    return f"""
    <table class="table firstcolum">
        <tr>
            <th>{title_col}</th><th>{value_col}</th>
        </tr>
        {rows}
    </table>
    """

def get_styling(css_file_path="style.css"):
    """Read and inline CSS from a file or provide a fallback style."""
    try:
        with open(css_file_path, "r") as css_file:
            return css_file.read()
    except FileNotFoundError:
        print(f"Warning: CSS file '{css_file_path}' not found. Using default styling.")
        # Fallback CSS in case the file is missing
        return """
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; }
        .container { max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 8px;
            padding: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
        .logo { text-align: center; margin-bottom: 20px; }
        .header { font-size: 18px; font-weight: bold; text-align: center; margin-bottom: 20px; }
        .table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        .table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .table th { background-color: #f2f2f2; font-weight: bold; }
        .footer { text-align: center; font-size: 12px; color: #555; margin-top: 20px; }
        """

def generate_html_email(company, frequency, mystats, what_stats, css_file_path="style.css", website_name:str=""):
    """Generate an HTML email with dynamic metrics and styling."""
    # Company details with fallback to avoid KeyErrors
    comp_name = company.get('name', 'Unknown Company')
    comp_url = company.get('url', '#')
    comp_logo = company.get('logo', '')
    comp_email = company.get('email', 'support@example.com')

    # Inline CSS
    inline_css = get_styling(css_file_path)

    # Metrics table
    metrics_table = ""
    stats = mystats.get("stats", {})
    print(stats)
    current = stats.get("current", {})
    previous = stats.get("previous", {})

    if current or previous:
        metrics_table = f"""
        <table class="table">
            <tr>
                <th></th><th>Views</th><th>Visits</th><th>Visitors</th><th>Bounce Rate</th><th>Visit Duration</th>
            </tr>
            <tr>
                <td>Last {frequency}</td>
                <td>{current.get('pageviews', 0)}</td>
                <td>{current.get('visits', 0)}</td>
                <td>{current.get('visitors', 0)}</td>
                <td>{current.get('bounces', 0)}%</td>
                <td>{current.get('totaltime', 0)}s</td>
            </tr>
            <tr>
                <td>Previous {frequency}</td>
                <td>{previous.get('pageviews', 0)}</td>
                <td>{previous.get('visits', 0)}</td>
                <td>{previous.get('visitors', 0)}</td>
                <td>{previous.get('bounces', 0)}%</td>
                <td>{previous.get('totaltime', 0)}s</td>
            </tr>
        </table>
        """


    # Other tables for stats
    pages_tables = ""
    stat_type_mapping = {
        "urls": {"col1": "Pages", "col2": "Views"},
        "referrers": {"col1": "Referrers", "col2": "Views"},
        "browsers": {"col1": "Browsers", "col2": "Views"},
        "oses": {"col1": "Operating Systems", "col2": "Views"},
        "devices": {"col1": "Devices", "col2": "Views"},
        "countries": {"col1": "Countries", "col2": "Views"},
        "events": {"col1": "Events", "col2": "Views"}
    }

    for stat in what_stats or []:
        if stat == "stats":
            continue  # Skip 'stats' since it's handled separately
        if stat not in stat_type_mapping:
            print(f"Warning: Unsupported stat type '{stat}'. Skip for report.")
            continue

        stat_config = stat_type_mapping[stat]
        pages_tables += generate_table(
            stat_config["col1"],
            stat_config["col2"],
            mystats.get(stat, [])
        )

    # HTML content with inline CSS
    html_content = f"""
    <html>
    <head>
        <style>{inline_css}</style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <img src="{comp_logo}" alt="{comp_name}" style="max-width: 100%; height: auto;">
            </div>
            <div class="header">
                Welcome to your {frequency}ly website summary for {website_name}!<br>
                Here are your top metrics from last {frequency}!
            </div>
            {metrics_table}
            {pages_tables}
            <div class="footer">
                If you were not expecting this report, please contact support at <a href="mailto:{comp_email}>{comp_email}</a><br/>
                Copyrights <a href="{comp_url}">{comp_name}</a>
            </div>
        </div>
    </body>
    </html>
    """
    return MIMEText(html_content, "html")
