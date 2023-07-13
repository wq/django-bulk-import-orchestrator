from rest_framework.test import APITestCase
import unittest
from . import settings


class WQTestCase(APITestCase):
    @unittest.skipUnless(settings.WITH_WQDB, "requires wq.db")
    def test_config(self):
        config = self.client.get("/config.json").data
        for name, conf in config["pages"].items():
            if name == "run":
                run_conf = conf

        for key in ("form", "postsave", "ordering"):
            run_conf.pop(key)

        expected_conf = {
            "name": "run",
            "verbose_name": "data wizard run",
            "verbose_name_plural": "data wizard runs",
            "url": "datawizard",
            "list": True,
            "background_sync": False,
            "cache": "none",
            "modes": [
                "list",
                "detail",
                "edit",
                "auto",
                "confirm",  # Custom
                "finalize",  # Custom
                "data",
                "serializers",
                "columns",
                "ids",
                "records",
                "validate",  # Custom
            ],
            "show_in_index": "can_change",
            "section": "Data Wizard",
            "icon": "list",
            "order": 210,
        }

        self.assertEqual(expected_conf, run_conf)
