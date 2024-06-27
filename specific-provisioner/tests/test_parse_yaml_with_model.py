import unittest
from pathlib import Path

from pydantic import BaseModel

from src.models.api_models import ValidationError
from src.models.data_product_descriptor import DataProduct
from src.utility.parsing_pydantic_models import parse_yaml_with_model


class ModelA(BaseModel):
    name: str
    age: int


class ModelB(BaseModel):
    title: str
    description: str


class SubModelB(ModelB):
    additional_info: str


class TestParseYAMLWithModel(unittest.TestCase):
    def test_parse_yaml_with_model_success(self):
        # Test a success case with ModelA
        yaml_data_a = """
                    name: John Doe
                    age: 30
                    """
        result_a = parse_yaml_with_model(yaml_data_a, ModelA)
        self.assertIsNotNone(result_a)
        self.assertEqual(result_a.name, "John Doe")
        self.assertEqual(result_a.age, 30)

        # Test a success case with ModelB
        yaml_data_b = """
                title: Example
                description: This is an example
                """
        result_b = parse_yaml_with_model(yaml_data_b, ModelB)
        self.assertIsNotNone(result_b)
        self.assertEqual(result_b.title, "Example")
        self.assertEqual(result_b.description, "This is an example")

        # Test a success case with SubModelB
        yaml_data_sub_b = """
                title: Subclass
                description: This is a subclass example
                additional_info: Additional information
                """
        result_sub_b = parse_yaml_with_model(yaml_data_sub_b, SubModelB)
        self.assertIsNotNone(result_sub_b)
        self.assertEqual(result_sub_b.title, "Subclass")
        self.assertEqual(result_sub_b.description, "This is a subclass example")
        self.assertEqual(result_sub_b.additional_info, "Additional information")

    def test_parse_yaml_with_model_failure(self):
        # Test an error case with ModelA
        yaml_data_a_invalid = """
                name: John Doe
                """
        # The age key is missing

        result_a_invalid = parse_yaml_with_model(yaml_data_a_invalid, ModelA)
        self.assertIsInstance(result_a_invalid, ValidationError)

        # Test an error case with ModelB
        yaml_data_b_invalid = """
                title: Example
                """
        # The "description" key is missing

        result_b_invalid = parse_yaml_with_model(yaml_data_b_invalid, ModelB)
        self.assertIsInstance(result_b_invalid, ValidationError)

        # Test an error case with SubModelB
        yaml_data_sub_b_invalid = """
        title: Subclass
        description: This is a subclass example
        """
        result_sub_b_invalid = parse_yaml_with_model(yaml_data_sub_b_invalid, SubModelB)
        self.assertIsInstance(result_sub_b_invalid, ValidationError)


def test_parse_valid_data_product_yaml():
    descriptor_str = Path("tests/descriptors/data_product_valid.yaml").read_text()
    result = parse_yaml_with_model(descriptor_str, DataProduct)
    assert not isinstance(result, ValidationError)
    assert isinstance(result, DataProduct)


def test_parse_invalid_data_product_yaml():
    descriptor_str = Path("tests/descriptors/data_product_valid.yaml").read_text()
    # Modify the YAML data to make it invalid
    invalid_yaml_data = descriptor_str.replace(
        "name: Vaccinations", "invalid_field: Invalid Value"
    )

    result = parse_yaml_with_model(invalid_yaml_data, DataProduct)
    assert isinstance(result, ValidationError)
