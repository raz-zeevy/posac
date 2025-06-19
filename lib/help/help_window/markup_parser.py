"""
Simple markup parser for help content
"""
import re
from typing import List, Tuple, Dict, Any

class MarkupParser:
    def __init__(self):
        self.tag_patterns = {
            'h1': r'<h1>(.*?)</h1>',
            'h2': r'<h2>(.*?)</h2>',
            'p': r'<p>(.*?)</p>',
            'txt': r'<txt>(.*?)</txt>',
            'strong': r'<strong>(.*?)</strong>',
            'bullet': r'<bullet>(.*?)</bullet>',
            'link': r'<link target="([^"]+)">(.*?)</link>',
            'br': r'<br\s*/>',
            'row': r'<row\s+([^>]+)\s*/>',
        }

    def parse(self, content: str) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Parse markup content and return a list of (element_type, attributes) tuples
        """
        elements = []
        remaining_content = content.strip()

        while remaining_content:
            found_match = False
            earliest_match = None
            earliest_pos = len(remaining_content)
            earliest_tag = None

            # Find the earliest tag in the remaining content
            for tag, pattern in self.tag_patterns.items():
                match = re.search(pattern, remaining_content, re.DOTALL)
                if match and match.start() < earliest_pos:
                    earliest_pos = match.start()
                    earliest_match = match
                    earliest_tag = tag

            if earliest_match and earliest_pos == 0:
                # Process the tag at the beginning
                if earliest_tag == 'h1':
                    elements.append(('heading', {'text': earliest_match.group(1).strip(), 'tag': 'h1'}))
                elif earliest_tag == 'h2':
                    elements.append(('heading', {'text': earliest_match.group(1).strip(), 'tag': 'h2'}))
                elif earliest_tag == 'p':
                    elements.append(('paragraph', {'text': earliest_match.group(1).strip()}))
                elif earliest_tag == 'txt':
                    elements.append(('text', {'text': earliest_match.group(1)}))
                elif earliest_tag == 'strong':
                    elements.append(('strong', {'text': earliest_match.group(1).strip()}))
                elif earliest_tag == 'bullet':
                    elements.append(('bullet', {'text': earliest_match.group(1).strip()}))
                elif earliest_tag == 'link':
                    elements.append(('link', {'text': earliest_match.group(2).strip(), 'target': earliest_match.group(1)}))
                elif earliest_tag == 'br':
                    elements.append(('line_break', {}))
                elif earliest_tag == 'row':
                    row_attrs = self._parse_row_attributes(earliest_match.group(1))
                    elements.append(('row', row_attrs))

                remaining_content = remaining_content[earliest_match.end():].strip()
                found_match = True

            elif earliest_match and earliest_pos > 0:
                # There's plain text before the next tag
                plain_text = remaining_content[:earliest_pos].strip()
                if plain_text:
                    elements.append(('text', {'text': plain_text}))
                remaining_content = remaining_content[earliest_pos:]
                found_match = True

            else:
                # No more tags, add remaining content as plain text
                if remaining_content.strip():
                    elements.append(('text', {'text': remaining_content.strip()}))
                break

        return elements

    def _parse_row_attributes(self, attr_string: str) -> Dict[str, Any]:
        """Parse row tag attributes like left="..." right="..." link="..." offset="..." """
        attrs = {}

        # Parse attributes using regex
        attr_pattern = r'(\w+)="([^"]*)"'
        matches = re.findall(attr_pattern, attr_string)

        for attr_name, attr_value in matches:
            if attr_name == 'offset':
                try:
                    attrs[attr_name] = int(attr_value)
                except ValueError:
                    attrs[attr_name] = 0
            else:
                attrs[attr_name] = attr_value

        return attrs

    def strip_markup(self, content: str) -> str:
        """Remove all markup tags and return plain text (for F1 functionality)"""
        # Remove all tags but preserve their content
        for tag, pattern in self.tag_patterns.items():
            if tag in ['h1', 'h2', 'p', 'txt', 'strong', 'bullet', 'link']:
                # For content tags, extract the text content
                if tag == 'link':
                    content = re.sub(pattern, r'\2', content, flags=re.DOTALL)
                elif tag == 'bullet':
                    content = re.sub(pattern, r'• \1', content, flags=re.DOTALL)
                else:
                    content = re.sub(pattern, r'\1', content, flags=re.DOTALL)
            elif tag in ['br', 'row']:
                # For structural tags, replace with appropriate text
                if tag == 'br':
                    content = re.sub(pattern, '\n', content, flags=re.DOTALL)
                elif tag == 'row':
                    # For rows, try to extract left and right content
                    def row_replacer(match):
                        attrs = self._parse_row_attributes(match.group(1))
                        left = attrs.get('left', '')
                        right = attrs.get('right', '')
                        return f"{left}: {right}\n"
                    content = re.sub(pattern, row_replacer, content, flags=re.DOTALL)

        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        return content.strip()

    def has_markup(self, content: str) -> bool:
        """Check if content contains markup tags"""
        for pattern in self.tag_patterns.values():
            if re.search(pattern, content, re.DOTALL):
                return True
        return False