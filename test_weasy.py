from weasyprint import HTML

html = HTML(source="<h1>Test</h1>")
html.write_pdf("test_output.pdf")

print("PDF generated successfully.")
