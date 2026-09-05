import os

html_files = [
    "analysis.html",
    "chat.html",
    "compare.html",
    "dashboard.html",
    "deadlines.html",
    "settings.html",
    "upload.html"
]

search_str = """        <div class="container-fluid">
            <button class="navbar-toggler\""""

replace_str = """        <div class="container-fluid">
            <a class="navbar-brand fw-bold" style="color: var(--primary-color);" href="dashboard.html">ContractGuard</a>
            <button class="navbar-toggler\""""

for file in html_files:
    path = os.path.join("d:\\ContractGuard\\frontend", file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "navbar-brand" not in content:
        content = content.replace(search_str, replace_str)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

print("Added ContractGuard logo to the top navbar.")
