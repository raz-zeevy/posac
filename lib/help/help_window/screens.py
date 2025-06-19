from lib.__version__ import VERSION
from lib.help.posac_help import PosacHelp, Help
from lib.help.help_window.style import *
from lib.help.help_window.markup_parser import MarkupParser
import inspect

###################################
############ SECTIONS #############
###################################

# Main sections
s_CONTENTS = 'contents'

# Dynamic section mapping from Help class attributes
def get_help_section_mapping():
    """Create a mapping from section names to Help class attributes"""
    mapping = {}

    # Get all Help class attributes that are HelpProperty instances
    for attr_name in dir(Help):
        if not attr_name.startswith('_'):
            attr = getattr(Help, attr_name)
            if hasattr(attr, 'help_text'):
                # Convert attribute name to section name (lowercase with underscores)
                section_name = attr_name.lower()
                mapping[section_name] = attr.help_text

    return mapping

# Create the mapping
HELP_SECTIONS = get_help_section_mapping()

###################################
############ PARSER ###############
###################################

class ScreensGenerator:
    def __init__(self, master):
        self.master = master
        self.parser = MarkupParser()

    def section(self, section_name):
        """Switch to the specified section"""
        method_name = SECTION_FUNC_PREFIX + section_name
        method = getattr(self, method_name, None)

        if method:
            method()
        else:
            # Try to find it in POSAC help sections
            self._render_posac_section(section_name)

    def _render_posac_section(self, section_name):
        """Render a section from POSAC help content"""

        # Try to find the section in our mapping
        help_text_key = HELP_SECTIONS.get(section_name)

        if not help_text_key:
            # Try direct lookup in PosacHelp
            all_sections = PosacHelp.get_all_sections()
            # Try to find by exact match or partial match
            matching_sections = [s for s in all_sections if s.lower().replace(' ', '_') == section_name]
            if matching_sections:
                help_text_key = matching_sections[0]
            else:
                # Try to find section by converting underscores back to spaces and title case
                display_name = section_name.replace('_', ' ').title()
                if display_name in all_sections:
                    help_text_key = display_name

        if help_text_key:
            help_content = PosacHelp.get(help_text_key, return_dict=False)
            self._render_content(help_text_key, help_content)
        else:
            # Section not found
            self.master.add_heading(f"Section '{section_name}' not found", H1)
            self.master.add_paragraph("The requested help section could not be found.")
            self.master.add_link("Return to Contents", s_CONTENTS)

    def _render_content(self, title, content):
        """Render content with enhanced markup parsing"""
        # Add the title with better spacing
        self.master.add_heading(title, H1)

        # Check if content contains markup
        if '<' in content and '>' in content:
            # Parse and render markup
            elements = self.parser.parse(content)
            self._render_elements(elements)
        else:
            # Render as plain text with better formatting
            paragraphs = content.split('\n\n')
            for i, paragraph in enumerate(paragraphs):
                if paragraph.strip():
                    self.master.add_paragraph(paragraph.strip())

    def _render_elements(self, elements):
        """Render parsed markup elements with enhanced spacing"""
        for i, (element_type, attrs) in enumerate(elements):
            if element_type == 'heading':
                # Add space before headings (except the first one)
                if i > 0 and attrs.get('tag') == H2:
                    self.master.add_line_break()
                self.master.add_heading(attrs['text'], attrs.get('tag', H1))
            elif element_type == 'paragraph':
                self.master.add_paragraph(attrs['text'], attrs.get('tag', TEXT))
            elif element_type == 'text':
                self.master.add_txt(attrs['text'])

            elif element_type == 'strong':
                self.master.add_strong(attrs['text'])

            elif element_type == 'bullet':
                self.master.add_bullet(attrs['text'])

            elif element_type == 'link':
                self.master.add_link(attrs['text'], attrs['target'])

            elif element_type == 'line_break':
                self.master.add_line_break()

            elif element_type == 'row':
                left = attrs.get('left', '')
                right = attrs.get('right', '')
                left_link = attrs.get('link')
                offset = attrs.get('offset', 0)
                self.master.add_row(left, right, left_link, offset)

    def section_contents(self):
        """Generate the main contents page with enhanced formatting"""
        self.master.add_heading(f"POSAC for Windows ({VERSION}) Help", H1)
        self.master.add_paragraph("Welcome to the POSAC help system. Select a topic below to learn more.")

        # Get all available sections from PosacHelp
        all_sections = PosacHelp.get_all_sections()

        # Enhanced categorization based on user's structure
        categories = {
            "Main Options": [],
            "Data Input & Variables": [],
            "Commands & Navigation": [],
            "Ranges": [],
            "External Traits": [],
            "Options": [],
            "POSACSEP": [],
            "Results": []
        }

        for section in sorted(all_sections):
            section_lower = section.lower()
            if any(word in section_lower for word in ['welcome']):
                categories["Main Options"].append(section)
            elif any(word in section_lower for word in ['name of the job', 'input data file', 'number of records', 'number of internal variables', 'number of external variables', 'item diagrams', 'external diagrams', 'frequency', 'structural posac', 'data subjects', 'missing value']):
                categories["Data Input & Variables"].append(section)
            elif any(word in section_lower for word in ['internal variables', 'external variables']) and 'ranges' not in section_lower and 'traits' not in section_lower:
                categories["Commands & Navigation"].append(section)
            elif 'external variables ranges' in section_lower:
                categories["Ranges"].append(section)
            elif 'external traits' in section_lower:
                categories["External Traits"].append(section)
            elif any(word in section_lower for word in ['posac axes', 'ascii', 'technical']):
                categories["Options"].append(section)
            elif 'posacsep' in section_lower:
                categories["POSACSEP"].append(section)
            elif any(word in section_lower for word in ['viewing results', 'handling result files']):
                categories["Results"].append(section)
            else:
                # Default fallback
                categories["Main Options"].append(section)

        # Render categories with enhanced formatting
        for category_name, sections in categories.items():
            if sections:  # Only show categories that have content
                self.master.add_heading(category_name, H2)
                for section in sections:
                    section_id = section.lower().replace(' ', '_')
                    self.master.add_txt("  • ")
                    self.master.add_link(section, section_id)
                    self.master.add_line_break()  # Line break after each item

    # Keep any existing specific sections that might be needed
    def section_welcome_to_the_posac_program(self):
        """Special handling for the welcome section"""
        self._render_posac_section("welcome_to_the_posac_program")
        self.master.add_line_break()
        self.master.add_link("View all help topics", s_CONTENTS)

if __name__ == '__main__':
    from lib.help.help_window.help_window import HelpWindow
    import tkinter as tk
    from lib.help.help_compiler import compile_help_file
    compile_help_file()
    root = tk.Tk()
    help_window = HelpWindow(root, "contents")
    root.mainloop()