import json
import unittest
from datetime import date, datetime, timezone

from scripts.update_data import (build_snapshot, parse_alsi, parse_eia_spot, parse_fred, parse_norway,
                                 parse_gie, parse_oil_flows, parse_wasde, parse_rte_power,
                                 parse_entsoe_forecast,
                                 verified_calendar)


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
        with self.assertRaisesRegex(ValueError, 'EU aggregate'):
            parse_gie(json.dumps({'data': rows}).encode())

    def test_gie_country_aggregate_and_lng_units(self):
        storage = {'data': [
            {'code':'FR', 'gasDayStart':'2026-09-24', 'full':'82.5',
             'gasInStorage':'118.4', 'netWithdrawal':'-62.3', 'status':'C'},
            {'code':'FR', 'gasDayStart':'2026-09-23', 'full':'82.0',
             'gasInStorage':'117.8', 'status':'C'}]}
        result = parse_gie(json.dumps(storage).encode(), 'fr')
        by_id = {item['id']: item for item in result['metrics']}
        self.assertEqual(by_id['gas_fr']['change'], 0.5)
        self.assertEqual(by_id['gas_fr_twh']['unit'], 'TWh')
        self.assertEqual(by_id['gas_fr_net']['value'], -62.3)
        lng = {'data':[{'code':'FR','gasDayStart':'2026-09-24','inventory':'465.2',
                         'sendOut':'245.7','status':'C'},
                       {'code':'FR','gasDayStart':'2026-09-23','inventory':'455.2',
                         'sendOut':'203.7','status':'C'}]}
        gas = {item['id']: item for item in parse_alsi(json.dumps(lng).encode(), 'fr')['metrics']}
        self.assertEqual(gas['lng_fr_inventory']['unit'], '10³ m³ GNL')
        self.assertEqual(gas['lng_fr_sendout']['change'], 42)

    def test_alsi_skips_incomplete_publication_without_undating_it(self):
        lng = {'data': [
            {'code': 'FR', 'gasDayStart': '2026-09-25', 'inventory': None,
             'sendOut': '246.2', 'status': 'C'},
            {'code': 'FR', 'gasDayStart': '2026-09-24', 'inventory': '465.2',
             'sendOut': '245.7', 'status': 'C'},
            {'code': 'FR', 'gasDayStart': '2026-09-23', 'inventory': '455.2',
             'sendOut': '203.7', 'status': 'C'}]}
        result = parse_alsi(json.dumps(lng).encode(), 'fr', date(2026, 9, 25))
        self.assertEqual(result['as_of'], '2026-09-24')
        self.assertEqual(result['metrics'][1]['change'], 42)
        with self.assertRaisesRegex(ValueError, 'stale'):
            parse_alsi(json.dumps(lng).encode(), 'fr', date(2026, 10, 3))

    def test_removed_gie_key_removes_previously_published_european_metrics(self):
        previous = {'metrics': [{'id':'gas_eu','value':80,'sector':'gas'},
                                {'id':'lng_fr_sendout','value':120,'sector':'gas'}],
                    'sources': {}, 'stories': [], 'history': {}}
        result = build_snapshot(previous, {}, datetime(2026, 9, 25, tzinfo=timezone.utc))
        self.assertFalse(any(item['id'] in ('gas_eu','lng_fr_sendout')
                             for item in result['metrics']))
        self.assertEqual(result['sources']['alsi_fr']['status'], 'needs_key')

    def test_rte_power_uses_last_real_observation_and_correct_export_sign(self):
        rows = []
        for index in range(8):
            rows.append({'date_heure':f'2026-09-25T{9 + index // 4:02d}:{index % 4 * 15:02d}:00+00:00',
                         'consommation':52000 + index * 100,
                         'prevision_j':52000,
                         'gaz':2500, 'eolien':4600, 'solaire':3200,
                         'nucleaire':38000, 'ech_physiques':-4300})
        rows.append({'date_heure':'2026-09-25T12:45:00+00:00',
                     'consommation':99999, 'gaz':99999})  # future measurement
        result = parse_rte_power(json.dumps({'results':rows}).encode(),
                                 datetime(2026, 9, 25, 12, tzinfo=timezone.utc))
        by_id = {item['id']:item for item in result['metrics']}
        self.assertEqual(result['points'][-1]['at'], '2026-09-25T10:45:00+00:00')
        self.assertEqual(by_id['power_load']['value'], 52700)
        self.assertEqual(by_id['power_residual']['value'], 44900)
        self.assertEqual(by_id['power_load_gap']['value'], 700)
        self.assertEqual(by_id['power_exchange']['value'], -4300)
        self.assertFalse(any('price' in item['id'] for item in result['metrics']))
        with self.assertRaisesRegex(ValueError, 'too old'):
            parse_rte_power(json.dumps({'results':rows[:-1]}).encode(),
                            datetime(2026, 9, 28, tzinfo=timezone.utc))

    def test_entsoe_forecast_only_publishes_actual_day_ahead_load(self):
        example = b'''<GL_MarketDocument xmlns="urn:iec:62325.351:tc57wg16:451-6:loadpublishdocument:3:0">
          <type>A65</type><process.processType>A01</process.processType>
          <TimeSeries><businessType>A04</businessType><quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
            <Period><timeInterval><start>2026-09-25T12:00Z</start><end>2026-09-25T13:00Z</end></timeInterval>
              <resolution>PT15M</resolution>
              <Point><position>1</position><quantity>51000</quantity></Point>
              <Point><position>2</position><quantity>52000</quantity></Point>
              <Point><position>3</position><quantity>54000</quantity></Point>
              <Point><position>4</position><quantity>53000</quantity></Point>
            </Period></TimeSeries></GL_MarketDocument>'''
        example = example.replace(b'</TimeSeries>',
            b'<Period><timeInterval><start>2026-09-26T13:00Z</start><end>2026-09-26T14:00Z</end>'
            b'</timeInterval><resolution>PT60M</resolution><Point><position>1</position>'
            b'<quantity>99999</quantity></Point></Period></TimeSeries>')
        result = parse_entsoe_forecast(example, 'fr',
                                       datetime(2026, 9, 25, 11, tzinfo=timezone.utc))
        self.assertEqual(result['metrics'][0]['value'], 54000)
        self.assertEqual(result['as_of'], '2026-09-25T12:30:00+00:00')
        with self.assertRaisesRegex(ValueError, 'different data item'):
            parse_entsoe_forecast(example.replace(b'<type>A65</type>', b'<type>A44</type>'), 'fr',
                                  datetime(2026, 9, 25, 11, tzinfo=timezone.utc))

    def test_missing_entsoe_token_clears_forecast_but_keeps_rte_power(self):
        previous = {'metrics':[{'id':'power_forecast_fr','sector':'power','value':58000},
                               {'id':'power_load','sector':'power','value':52000}],
                    'sources':{'entsoe_fr':{'status':'ok'}},'stories':[], 'history':{}}
        result = build_snapshot(previous, {}, datetime(2026, 9, 25, tzinfo=timezone.utc))
        self.assertEqual(result['sources']['entsoe_fr']['status'], 'needs_key')
        self.assertEqual([m['id'] for m in result['metrics'] if m['sector']=='power'], ['power_load'])

    def test_fred_ignores_missing_observation_and_rejects_stale_prices(self):
        raw = b'DATE,DCOILBRENTEU\n2026-09-21,116.15\n2026-09-22,.\n2026-09-23,114.89\n'
        result = parse_fred(raw, 'DCOILBRENTEU', date(2026, 9, 25))
        item = result['metrics'][0]
        self.assertEqual(item['value'], 114.89)
        self.assertEqual(item['change'], -1.26)
        self.assertEqual(item['as_of'], '2026-09-23')
        with self.assertRaisesRegex(ValueError, 'more than 30 days'):
            parse_fred(raw, 'DCOILBRENTEU', date(2026, 11, 1))

    def test_norwegian_production_includes_ngl_and_condensate(self):
        page = (b'<p>Production figures August 2026</p><p>9/22/2026 Preliminary production figures for '
                b'August 2026 show an average daily production of 2 073 000 barrels of oil, '
                b'NGL and condensate.</p><p>Production figures July 2026</p><p>8/20/2026 '
                b'Preliminary production figures for July 2026 show an average daily production '
                b'of 1 976 000 barrels of oil, NGL and condensate.</p>')
        row = parse_norway(page, date(2026, 9, 25))['metrics'][0]
        self.assertEqual(row['value'], 2.073)
        self.assertEqual(row['change'], 0.097)
        self.assertIn('LGN + condensats', row['detail'])

    def test_eia_spot_price_rows_match_each_header_date(self):
        page = (b'<table><tr><td>Product by Area</td><td>09/15/26</td><td>09/16/26</td>'
                b'<td>09/17/26</td><td>09/18/26</td><td>09/21/26</td><td>09/22/26</td></tr>'
                b'<tr><td>Crude Oil</td></tr><tr><td>WTI - Cushing, Oklahoma</td>'
                b'<td>107.02</td><td>103.620</td><td>103.21</td><td>101.44</td>'
                b'<td>96.97</td><td>96.41</td><td>1986-2026</td></tr>'
                b'<tr><td>Brent - Europe</td><td>130.80</td><td>127.840</td>'
                b'<td>121.18</td><td>119.66</td><td>116.15</td><td>114.89</td></tr>'
                b'<tr><td>Conventional Gasoline</td></tr></table>')
        brent = parse_eia_spot(page, 'brent', date(2026, 9, 25))['metrics'][0]
        wti = parse_eia_spot(page, 'wti', date(2026, 9, 25))['metrics'][0]
        self.assertEqual((brent['value'], brent['as_of']), (114.89, '2026-09-22'))
        self.assertEqual((wti['value'], wti['change']), (96.41, -0.56))
        with self.assertRaisesRegex(ValueError, 'columns mismatch'):
            parse_eia_spot(page.replace(b'<td>119.66</td>', b''), 'brent', date(2026, 9, 25))

    def test_agenda_uses_agency_holiday_exceptions_and_paris_dst(self):
        events = verified_calendar(date(2026, 9, 25))
        oil_sep = next(e for e in events if e['title'].startswith('EIA · stocks')
                       and e['at'].startswith('2026-09-30'))
        self.assertEqual(oil_sep['at'], '2026-09-30T14:30:00+00:00')
        oil_oct = [e for e in events if e['title'].startswith('EIA · stocks')
                   and e['at'].startswith('2026-10-15')]
        self.assertEqual(oil_oct[0]['at'], '2026-10-15T16:00:00+00:00')
        self.assertFalse(any(e['at'].startswith('2026-10-14') for e in events))
        self.assertTrue(any(e['title'].startswith('USDA') and
                            e['at'] == '2026-10-09T16:00:00+00:00' for e in events))


if __name__ == '__main__':
    unittest.main()
