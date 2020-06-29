import pytest
from solid_backend.glossary.models import GlossaryEntry


@pytest.fixture
def glossary_entry_model_class():
    return GlossaryEntry
