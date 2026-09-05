import os
import re

html_files = [
    "analysis.html",
    "chat.html",
    "compare.html",
    "dashboard.html",
    "deadlines.html",
    "settings.html",
    "upload.html"
]

bootstrap_css = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">'
bootstrap_js = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>'

navbar_html = """
    <!-- Top Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#topNavbar" aria-controls="topNavbar" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="topNavbar">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="settings.html">Settings</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#" id="logout-btn">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
"""

for file in html_files:
    path = os.path.join("d:\\ContractGuard\\frontend", file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add Bootstrap CSS
    if "bootstrap.min.css" not in content:
        content = content.replace("</head>", f"    {bootstrap_css}\n</head>")

    # 2. Add Bootstrap JS
    if "bootstrap.bundle.min.js" not in content:
        content = content.replace("</body>", f"    {bootstrap_js}\n</body>")

    # 3. Add Navbar after <body>
    if "<!-- Top Navbar -->" not in content:
        content = content.replace("<body>", f"<body>\n{navbar_html}")

    # 4. Remove Settings and Logout from sidebar (handle different variations if any)
    content = re.sub(r'<li><a href="settings\.html".*?>Settings</a></li>', '', content)
    content = re.sub(r'<li><a href="#" id="logout-btn".*?>Logout</a></li>', '', content)
    
    # 5. Fix duplicated id="logout-btn" if they had it in sidebar and navbar. 
    # Since we replaced the sidebar one, we only have one in navbar now. But if there's any logic relying on the sidebar, it's fine.

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Updated HTML files with Bootstrap navbar.")
