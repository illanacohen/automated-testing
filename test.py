import sys
import json
import logging

import argparse
import unittest

from driver import Driver
from constants import Elements


sys.path.insert(0, '.')

parser = argparse.ArgumentParser(description="Selenium automated testing")
parser.add_argument(
    '--braintree-scenarios',
    metavar='',
    type=str,
    help='json serializable str with service="braintree", scenarios=[<scenarios>] and type=[type in ("transaction", "subscription")]',
    dest='braintree_scenarios'
)
parser.add_argument(
    '--stripe-scenarios',
    metavar='',
    type=str,
    help='json serializable str with service="stripe", scenarios=[<scenarios>] and type=[type in ("transaction", "subscription", "subscription_with_trial")]',
    dest='stripe_scenarios'
)

if __name__ == "__main__":
    class ParametrizedTestCase(unittest.TestCase):
        """ TestCase classes that want to be parametrized should
            inherit from this class.
        """
        def __init__(self, methodName='runTest', scenarios=None):
            super(ParametrizedTestCase, self).__init__(methodName)
            self.service = scenarios.get('service')
            self.scenarios = scenarios.get('scenarios')
            self.types = scenarios.get('types')
            self.driver = Driver()


        @staticmethod
        def parametrize(testcase_klass, scenarios=None):
            """ Create a suite containing all tests taken from the given
                subclass, passing them the parameter 'scenarios'.
            """
            testloader = unittest.TestLoader()
            testnames = testloader.getTestCaseNames(testcase_klass)
            suite = unittest.TestSuite()
            for name in testnames:
                suite.addTest(testcase_klass(name, scenarios=scenarios))
            return suite


    class DemoShopTest(ParametrizedTestCase):
        def setUp(self):
            self.buttons = {
                'braintree': { 
                    'transaction': Elements.BRAINTREE_TRANSACTION_BUTTON,
                    'subscription': Elements.BRAINTREE_SUBSCRIPTION_BUTTON,
                },
                'stripe': {
                    'transaction': Elements.STRIPE_TRANSACTION_BUTTON,
                    'subscription_with_trial': Elements.STRIPE_SUBSCRIPTION_TRIAL_BUTTON,
                    'subscription': Elements.STRIPE_SUBSCRIPTION_BUTTON
                }
            }
            self.scenarios_results = {
                Elements.SCENARIO_SUCCESFUL_PAYMENT: Elements.MESSAGE_SUCCESFUL_PAYMENT,
                Elements.SCENARIO_DECLINED: Elements.MESSAGE_DECLINED,
                Elements.SCENARIO_APPROVED: Elements.MESSAGE_APPROVED
            }
   
        def purchase(self, product_type):
            results = self.driver.purchase(
                payment_method=self.buttons.get(self.service).get(product_type), scenarios=self.scenarios
            )
            expected =  [self.scenarios_results.get(result_message) for result_message in self.scenarios]
            self.assertEqual(results, expected)

        def test_transaction(self):
            if 'transaction' in self.types:
                logging.info('Buying simple transaction product')
                self.purchase(product_type='transaction')        

        def test_subscription_with_trial(self):
            if 'subscription_with_trial' in self.types:
                logging.info('Buying subscription with trial period product')
                self.purchase(product_type='subscription_with_trial')

        def test_subscription(self):
            if 'subscription' in self.types:
                logging.info('Buying subscription product')
                self.purchase(product_type='subscription')


    args = parser.parse_args()
    suite = unittest.TestSuite()

    all_scenarios = [
        Elements.SCENARIO_SUCCESFUL_PAYMENT,
        Elements.SCENARIO_DECLINED,
        Elements.SCENARIO_APPROVED
    ]
    suite.addTest(ParametrizedTestCase.parametrize(
        DemoShopTest,
        scenarios=json.loads(args.braintree_scenarios) if args.braintree_scenarios else {
            "service": "braintree", "scenarios": all_scenarios, "types": ["transaction", "subscription"]
            }
        )
    )
    suite.addTest(ParametrizedTestCase.parametrize(
        DemoShopTest,
        scenarios=json.loads(args.stripe_scenarios) if args.stripe_scenarios else {
            "service": "stripe", "scenarios": all_scenarios, "types": ["transaction", "subscription_with_trial"]
            }
        )
    )
    unittest.TextTestRunner(verbosity=2).run(suite)
