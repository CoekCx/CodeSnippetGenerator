import os

from models.benchmark_table import BenchmarkTable


class BenchmarkHtmlGenerator:
    @staticmethod
    def generate_benchmark_table_html(table: BenchmarkTable):
        """
        Generates HTML code for a benchmark table with proper styling and formatting.

        Args:
            table (BenchmarkTable): The benchmark table model to convert to HTML

        Returns:
            str: The generated HTML code
        """
        html = ['<table class="code-container">']
        html.append('    <thead>')
        html.append('        <tr>')
        for header in table.headers:
            html.append(f'            <th>{header}</th>')
        html.append('        </tr>')
        html.append('    </thead>')

        html.append('    <tbody>')
        for row in table.rows:
            html.append('        <tr>')

            for cell in row.sorted_cells(table.headers):
                if cell.is_method:
                    html.append(f'            <td class="method">{cell.print_cell()}</td>')
                else:
                    html.append(f'            <td>{cell.print_cell()}</td>')

            html.append('        </tr>')
        html.append('    </tbody>')
        html.append('</table>')

        return '\n'.join(html)

    @staticmethod
    def generate_benchmark_html(table: BenchmarkTable) -> str:
        table_html = BenchmarkHtmlGenerator.generate_benchmark_table_html(table)

        current_dir = os.getcwd()
        template_path = os.path.join(current_dir, "resources/benchmark_template.html").replace("\\", "/")

        with open(template_path, "r", encoding="utf-8") as file:
            html_code = file.read()

        return html_code.replace("{{TABLE_CODE}}", table_html)
