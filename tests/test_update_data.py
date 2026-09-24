import json
import unittest
from datetime import datetime, timezone

from scripts.update_data import build_snapshot, parse_gie, parse_oil_flows, parse_wasde


FLOW_SAMPLE = b'''"STUB_1","STUB_2","9/18/26","9/11/26","Difference","9/19/25"
"Crude Oil Supply ","(1)     Domestic Production","13,939","13,944","-5","13,501"
"Crude Oil Supply ","(8)        Imports","5,877","7,058","-1,181","6,495"
"Crude Oil Supply ","(12)        Exports","3,281","4,831","-1,550","4,484"
"Crude Oil Supply ","(17)   Crude Oil Input to Refineries","16,811","17,330","-519","16,476"
'''

WASDE_SAMPLE = b'''WASDE - 675 - 8 September 2026
World and U.S. Supply and Use for Grains  1/
World
Wheat
 2024/25 799 1069 210 808 260
 2025/26 (Est.) 843 1104 227 823 280
 2026/27 (Proj.)
  Aug 819.30 1099.52 212.71 826.27 273.25
  Sep 822.43 1103.04 211.77 826.75 276.29
Coarse Grains
 United States
U.S. Feed Grain and Corn Supply and Use
FEED GRAINS
Production 391 447 418 412
CORN
Production 14892 17021 16013 15800
Exports 2873 3425 3275 3275
Ending Stocks 1551 1922 1653 1567
Avg.FarmPrice ($/bu) 4.24 4.15 4.50 4.80
U.S. Sorghum, Barley, and Oats Supply and Use
U.S. Soybeans and Products Supply and Use (Domestic Measure)
SOYBEANS
Production 4374 4262 4519 4535
Exports 1892 1520 1660 1685
Ending Stocks 325 325 320 310
SOYBEAN OIL
Ending Stocks 1551 1747 1837 1837
U.S. Sugar Supply and Use
World Corn Supply and Use  1/  (Contd.)
2026/27 Proj.
World 3/
 Aug 298.83 1298.88 203.73 832.46 1323.05 210.48 274.66
 Sep 301.38 1290.95 203.11 827.40 1320.23 210.08 272.10
World Less China
WASDE - 675 - 24
'''


class PublicationParsingTest(unittest.TestCase):
    def test_eia_flow_rates_are_converted_from_thousand_barrels_per_day(self):
        result = parse_oil_flows(FLOW_SAMPLE)
        metrics = {row['id']: row for row in result['metrics']}
        self.assertEqual(metrics['oil_production']['value'], 13.939)
        self.assertEqual(metrics['oil_imports']['change'], -1.181)
        self.assertEqual(metrics['oil_refinery']['unit'], 'M bbl/j')
        self.assertEqual(metrics['oil_exports']['as_of'], '2026-09-18')

    def test_inconsistent_eia_change_rejected(self):
        bad = FLOW_SAMPLE.replace(b'"-1,181"', b'"-181"')
        with self.assertRaisesRegex(ValueError, 'mismatch'):
            parse_oil_flows(bad)

    def test_wasde_selects_corn_and_soybean_not_feed_grains_or_soy_oil(self):
        result = parse_wasde(WASDE_SAMPLE, 'https://www.usda.gov/example')
        metrics = {row['id']: row for row in result['metrics']}
        self.assertEqual(metrics['ag_corn_output']['value'], 15800)
        self.assertEqual(metrics['ag_soy_stocks']['value'], 310)
        self.assertEqual(metrics['ag_soy_exports']['change'], 25)
        self.assertEqual(metrics['ag_world_wheat']['value'], 276.29)
        self.assertEqual(metrics['ag_world_wheat_trade']['value'], 211.77)
        self.assertEqual(result['as_of'], '2026-09')

    def test_failed_feed_retains_dated_value_and_marks_error(self):
        previous = {'metrics': [{'id': 'oil_crude', 'value': 426.398, 'as_of': '2026-09-18'}],
                    'sources': {'oil': {'status': 'ok', 'as_of': '2026-09-18'}},
                    'stories': [], 'history': {}}
        snapshot = build_snapshot(previous, {'oil': ValueError('broken')},
                                  datetime(2026, 9, 24, tzinfo=timezone.utc))
        self.assertEqual(snapshot['sources']['oil']['status'], 'error')
        self.assertEqual(snapshot['metrics'][0]['value'], 426.398)
        self.assertEqual(snapshot['metrics'][0]['as_of'], '2026-09-18')

    def test_gie_does_not_confuse_country_with_european_aggregate(self):
        rows = [{'code': 'DE', 'name': 'Germany', 'gasDayStart': '2026-09-18',
                 'full': '90.1', 'gasInStorage': '200', 'status': 'C'}]
        with self.assertRaisesRegex(ValueError, 'EU storage'):
            parse_gie(json.dumps({'data': rows}).encode())


if __name__ == '__main__':
    unittest.main()
