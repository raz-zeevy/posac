import pytest

def pytest_addoption(parser):
    """Add visual mode option"""
    parser.addoption(
        "--visual",
        action="store_true",
        default=False,
        help="Run in visual mode for manual inspection"
    )

@pytest.fixture(scope="session")
def visual_mode(request):
    """Fixture to check if we're in visual mode"""
    return request.config.getoption("--visual") 