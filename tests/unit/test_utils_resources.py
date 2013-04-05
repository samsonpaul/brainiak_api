from unittest import TestCase
from brainiak.utils.resources import decorate_with_resource_id


class ResourceUtilsTestCase(TestCase):

    def test_decorate_with_resource_id_with_single_dict(self):
        list_of_dicts = [{"@id": "http://a/b/c"}]
        decorate_with_resource_id(list_of_dicts)
        self.assertIn('resource_id', list_of_dicts[0])
        self.assertEquals(list_of_dicts[0].get('resource_id'), "c")

    def test_decorate_with_resource_id_with_multiple_dicts(self):
        list_of_dicts = [{"@id": "http://a/b/c"}, {"@id": "https://x/y/z"}]
        decorate_with_resource_id(list_of_dicts)
        self.assertEquals(list_of_dicts[0].get('resource_id'), "c")
        self.assertEquals(list_of_dicts[1].get('resource_id'), "z")

    def test_decorate_with_resource_id_with_curie(self):
        list_of_dicts = [{"@id": "person:Person"}]
        decorate_with_resource_id(list_of_dicts)
        self.assertEquals(list_of_dicts[0].get('resource_id'), "Person")