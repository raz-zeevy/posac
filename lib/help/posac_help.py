import pickle

class PosacHelp:
    _sections = None
    _metadata = None

    @classmethod
    def _initialize(cls, filename="posac_help.bin"):
        """Load help data and metadata once and store them at the class level."""
        if cls._sections is None or cls._metadata is None:
            with open(filename, "rb") as file:
                data = pickle.load(file)
                cls._sections = data["sections"]
                cls._metadata = data["metadata"]

    @classmethod
    def get(cls, section_name):
        """Fetch help text by section name."""
        cls._initialize()  # Ensure data is loaded
        return cls._sections.get(section_name, "Section not found.")

    @classmethod
    def get_all_sections(cls):
        """Return a list of all section names."""
        cls._initialize()
        return list(cls._sections.keys())

if __name__ == "__main__":
    print(PosacHelp.get("Technical options"))
    print(PosacHelp.find_by_keyword("posac"))
    print(PosacHelp.get_formatted("Technical options"))